"""Handles logging information to Firestore.
"""
import os
from datetime import datetime
from enum import Enum
from google.cloud import firestore

from .state_manager import set_curr_log_id, get_curr_log_id
from .speech_text_processing import upload_audio_file

PROJECT_ID = "chess-master-andy-mhyo"
LOGGING_SUFFIX = os.environ['LOGGING_SUFFIX']
INTENT_LOGS_BASE_COLLECTION = "intent_logs"
ERROR_LOGS_BASE_COLLECTION = "error_logs"
INTENT_LOGS_COLLECTION = f"{INTENT_LOGS_BASE_COLLECTION}_{LOGGING_SUFFIX}"
ERROR_LOGS_COLLECTION = f"{ERROR_LOGS_BASE_COLLECTION}_{LOGGING_SUFFIX}"

ERROR_TYPES = Enum(
    "ERROR_TYPES",
    "STT INTENT FULFILLMENT TTS LOGGING UNKNOWN"
)


def check_intent_log_data(data):
    """Checks if the required keys in data are present.

    Args:
        data (dict): the data that the document should contain.

    Data Format:
        {
            "board_str_before": str,
            "board_str_after": str,
            "detected_intent": str,
            "intent_success": bool,
            "andy_response_text": str,
            "user_input_text": str,
            "user_input_audio_name": str
        }

    """
    return all(key in data for key in ('board_str_before', 'board_str_after',
                                       'detected_intent', 'intent_success',
                                       'andy_response_text', 'user_input_text',
                                       'user_input_audio_name'))


def create_intent_log(session_id, data):
    """Creates a log entry for an intent.

    Args:
        session_id (str): the session to associate the log with.
        data (dict): the data that the document should contain.

    Data Format:
        {
            "board_str_before": str,
            "board_str_after": str,
            "detected_intent": str,
            "intent_success": bool,
            "andy_response_text": str,
            "user_input_text": str,
            "user_input_audio_name": str
        }

    """
    # Check for required data
    if check_intent_log_data(data):
        try:
            db = firestore.Client(project=PROJECT_ID)
            doc_ref = db.collection(INTENT_LOGS_COLLECTION).document()
            doc_ref.set(data)
            doc_ref.set({
                'timestamp': datetime.now(),
                'session_id': session_id
            }, merge=True)

            # Set the current log_id for audio response logging
            set_curr_log_id(session_id, doc_ref.id)
        except Exception as e:
            err_msg = f"Error logging intent log: {e}"
            create_error_log(session_id, ERROR_TYPES.LOGGING, err_msg)
    else:
        create_error_log(session_id, ERROR_TYPES.LOGGING,
                         "Not all required parameters present.")
        raise Exception("Not all required parameters present.")


def update_intent_log_with_audio_response(session_id, audio_data):
    """Updates an existing log entry for an intent.

    Args:
        session_id (str): the session to associate the log with.
        audio_data (bytes): the Audio data to log.

    """
    # Upload the audio data
    try:
        andy_response_audio_location = upload_audio_file(audio_data)
        db = firestore.Client(project=PROJECT_ID)
        log_id = get_curr_log_id(session_id)
        doc_ref = db.collection(INTENT_LOGS_COLLECTION).document(log_id)
        doc_ref.set({
            "andy_response_audio_location": andy_response_audio_location
        }, merge=True)

        # Reset curr_log_id
        set_curr_log_id(session_id, None)
    except Exception as e:
        err_msg = f"Error logging audio response to intent log: {e}"
        create_error_log(session_id, ERROR_TYPES.LOGGING, err_msg)


def create_error_log(session_id, error_type, description):
    """Creates a log entry for an error.

    Args:
        session_id (str): the session to associate the log with.
        type (Enum): the error type, as an ERROR_TYPES Enum.
        description (str): a description of what happened.

    """
    print(description)
    try:
        db = firestore.Client(project=PROJECT_ID)
        doc_ref = db.collection(ERROR_LOGS_COLLECTION).document()
        doc_ref.set({
            'session_id': session_id,
            'type': error_type.name,
            'description': description,
            'timestamp': datetime.now()
        })
    except Exception as e:
        err_msg = f"Error logging error log for {error_type.name}: {e}"
        print(err_msg)
