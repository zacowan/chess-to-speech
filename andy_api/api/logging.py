"""Handles logging information to Firestore.

General Log Format:
    {
        "session_id": str,
        "timestamp": datetime,

        "user_request_info": {
            "text": str,
            "audio_name": str,

            "detected_intent": str,
            "detected_params": dict,

            "detected_fulfillment": str,
            "fulfillment_success": bool,
            "fulfillment_params": dict,

            "board_str_before": str,
            "board_str_after": str,

            "received_at": datetime,
            "response_at": datetime,

            "error_types": list(str),
            "error_desc": list(str),
        }

        "andy_response_info": {
            "text": str,
            "audio_name": str,

            "received_at": datetime,
            "response_at": datetime,

            "error_types": list(str),
            "error_desc": list(str),
        }

        "andy_move_info": {
            "text": str,
            "audio_name": str,
            "move_info": {
                "from": str,
                "to": str,
            },
            "board_str_before": str,
            "board_str_after": str,

            "received_at": datetime,
            "response_at": datetime,

            "error_types": list(str),
            "error_desc": list(str),
        }

        "errors_occurred": bool,
        "error_types": list(str),
    }

Intent Log Format:

    {
        "board_str_before": str,
        "board_str_after": str,
        "detected_intent": str,
        "intent_success": bool,
        "andy_response_text": str,
        "user_input_text": str,
        "user_input_audio_name": str,
        "andy_response_audio_name": str,
        "timestamp": datetime,
        "session_id": str
    }

Error Log Format:

    {
        'session_id': str,
        'type': str,
        'description': str,
        'timestamp': datetime
    }

"""
import os
import traceback
from datetime import datetime
from enum import Enum
from google.cloud import firestore

from .state_manager import set_curr_log_id, get_curr_log_id
from .speech_text_processing import upload_audio_file

PROJECT_ID = "chess-master-andy-mhyo"
LOGGING_SUFFIX = os.environ['LOGGING_SUFFIX']
INTENT_LOGS_BASE_COLLECTION = "intent_logs"
ERROR_LOGS_BASE_COLLECTION = "error_logs"
GENERAL_LOGS_BASE_COLLECTION = "logs"
GENERAL_LOGS_COLLECTION = f"{GENERAL_LOGS_BASE_COLLECTION}_{LOGGING_SUFFIX}"
INTENT_LOGS_COLLECTION = f"{INTENT_LOGS_BASE_COLLECTION}_{LOGGING_SUFFIX}"
ERROR_LOGS_COLLECTION = f"{ERROR_LOGS_BASE_COLLECTION}_{LOGGING_SUFFIX}"

ERROR_TYPES = Enum(
    "ERROR_TYPES",
    "STT INTENT FULFILLMENT TTS LOGGING UNKNOWN"
)


def update_log_with_andy_response(session_id, data):
    """Updates the current log file with data.

    Args:
        session_id (str): the session_id to associate the log with.
        data (dict): the data to log.
    """
    # Try to upload andy audio data
    try:
        andy_response_audio_name = upload_audio_file(
            data.get("user_input_audio_data"))
    except Exception:
        andy_response_audio_name = ""
        data.set("error_occurred", True)
        data.set("error_type", data.get(
            "error_type", []).append(ERROR_TYPES.TTS.name))
        data.set("error_description", data.get("error_description", []).append(
            f"Failed to upload andy audio data: {traceback.format_exc()}"))
        print("Failed to upload andy audio data.")
    # Try to fill out data
    try:
        db = firestore.Client(project=PROJECT_ID)
        doc_ref = db.collection(GENERAL_LOGS_COLLECTION).document()
        doc_ref.set({
            'andy_response_text': data.get('andy_response_text', []),
            'andy_response_audio_name': [andy_response_audio_name],
            'board_str_before': data.get('board_str_before', []),
            'board_str_after': data.get('board_str_after', []),
            'request_received_at': data.get('request_received_at', datetime.now()),
            'error_occurred': data.get('error_occurred', False),
            'error_type': data.get('error_type', []),
            'error_description': data.get('error_description', [])
        }, merge=True)
        # Set the current log_id for audio response logging
        set_curr_log_id(session_id, doc_ref.id)
    except Exception:
        err_msg = f"Error logging: {traceback.format_exc()}"
        print(err_msg)


def create_log(session_id, data):
    """Creates a log file with data.

    Args:
        session_id (str): the session_id to associate the log with.
        data (dict): the data to log.
    """
    # Try to upload user audio data
    try:
        user_input_audio_name = upload_audio_file(
            data.get("user_input_audio_data"))
    except Exception:
        user_input_audio_name = ""
        data.set("error_occurred", True)
        data.set("error_type", data.get(
            "error_type", []).append(ERROR_TYPES.TTS.name))
        data.set("error_description", data.get("error_description", []).append(
            f"Failed to upload user audio data: {traceback.format_exc()}"))
        print("Failed to upload user audio data.")
    # Try to fill out data
    try:
        db = firestore.Client(project=PROJECT_ID)
        log_id = get_curr_log_id(session_id)
        doc_ref = db.collection(GENERAL_LOGS_COLLECTION).document(log_id)
        doc_ref.set({
            'session_id': data.get("session_id"),
            'timestamp': datetime.now(),
            'user_input_text': data.get('user_input_text', ''),
            'user_input_audio_name': user_input_audio_name,
            'detected_intent': data.get('detected_intent', ''),
            'detected_params': data.get('detected_params', []),
            'detected_fulfillment': data.get('detected_fulfillment', ''),
            'fulfillment_success': data.get('fulfillment_success', False),
            'andy_response_text': data.get('andy_response_text', []),
            'andy_response_audio_name': [],
            'board_str_before': data.get('board_str_before', ''),
            'board_str_after': data.get('board_str_after', ''),
            'request_received_at': data.get('request_received_at', datetime.now()),
            'error_occurred': data.get('error_occurred', False),
            'error_type': data.get('error_type', []),
            'error_description': data.get('error_description', [])
        })
        # Set the current log_id for audio response logging
        set_curr_log_id(session_id, doc_ref.id)
    except Exception:
        err_msg = f"Error logging: {traceback.format_exc()}"
        print(err_msg)


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
        }

    """
    return all(key in data for key in ('board_str_before', 'board_str_after',
                                       'detected_intent', 'intent_success',
                                       'andy_response_text', 'user_input_text'))


def create_intent_log(session_id, audio_data, data):
    """Creates a log entry for an intent.

    Args:
        session_id (str): the session to associate the log with.
        audio_data (bytes): the user's audio to log.
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
            user_input_audio_location = upload_audio_file(audio_data)
            db = firestore.Client(project=PROJECT_ID)
            doc_ref = db.collection(INTENT_LOGS_COLLECTION).document()
            doc_ref.set(data)
            doc_ref.set({
                'timestamp': datetime.now(),
                'session_id': session_id,
                'user_input_audio_name': user_input_audio_location
            }, merge=True)

            # Set the current log_id for audio response logging
            set_curr_log_id(session_id, doc_ref.id)
        except Exception:
            err_msg = f"Error logging intent log: {traceback.format_exc()}"
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
            "andy_response_audio_name": andy_response_audio_location
        }, merge=True)

        # Reset curr_log_id
        set_curr_log_id(session_id, None)
    except Exception:
        err_msg = f"Error logging audio response to intent log: {traceback.format_exc()}"
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
    except Exception:
        err_msg = f"Error logging error log for {error_type.name}: {traceback.format_exc()}"
        print(err_msg)
