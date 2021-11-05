"""Handles logging information to Firestore.

User Request Log:
    {
        "session_id": str,
        "timestamp": datetime,

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

        "errors_occurred": bool,
        "error_types": list(str),
        "error_desc": list(str),
    }

Andy Response Log:
    {
        "session_id": str,
        "timestamp": datetime,
        "user_request_log_id": str,

        "text": str,
        "audio_name": str,

        "received_at": datetime,
        "response_at": datetime,

        "errors_occurred": bool,
        "error_types": list(str),
        "error_desc": list(str),
    }

Andy Move Log:
    {
        "session_id": str,
        "timestamp": datetime,
        "user_request_log_id": str,

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

        "errors_occurred": bool,
        "error_types": list(str),
        "error_desc": list(str),
    }

"""
import os
import traceback
from datetime import datetime
from enum import Enum
from google.cloud import firestore

from .state_manager import set_curr_log_id, get_curr_log_id, set_curr_errors, get_curr_errors
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
    "INTENT FULFILLMENT TTS LOGGING AUDIO_UPLOAD UNKNOWN"
)


def print_error(err_type, err_desc):
    print("-"*20)
    print(f"[{err_type.name} Error]: {err_desc}")
    print("-"*20)


def log_error(session_id, err_type, err_desc):
    # Set the err_type and err_desc using state_manager
    set_curr_errors(session_id, err_type.name, err_desc)
    print_error(err_type, err_desc)


def log_andy_move(session_id, data):
    """Logs Andy's move.

    Args:
        session_id (str): the session_id provided by the client.
        data (dict): the data to upload.

    Data format:
        {
            "text": str,
            "audio_data": bytes,
            "move_info": {
                "from": str,
                "to": str,
            },
            "board_str_before": str,
            "board_str_after": str,
            "received_at": datetime,
            "response_at": datetime,
        }
    """
    # Upload audio_data and get name
    try:
        audio_name = upload_audio_file(
            data.get("audio_data"))
    except Exception:
        audio_name = ""
        err_msg = f"Failed to upload Andy's move audio: {traceback.format_exc()}"
        log_error(session_id, ERROR_TYPES.AUDIO_UPLOAD, err_msg)
    # Get errors from state_manager
    error_types, error_desc = get_curr_errors(session_id)
    # Set all of the data in a log
    try:
        db = firestore.Client(project=PROJECT_ID)
        log_id = get_curr_log_id(session_id)
        doc_ref = db.collection(GENERAL_LOGS_COLLECTION).document()
        doc_ref.set({
            'session_id': session_id,
            'timestamp': datetime.now(),
            'user_request_log_id': log_id,
            'text': data.get('text', ''),
            'audio_name': audio_name,
            'move_info': data.get('move_info', {}),
            'board_str_before': data.get('board_str_before', ''),
            'board_str_after': data.get('board_str_after', ''),
            'received_at': data.get('received_at', datetime.now()),
            'response_at': data.get('response_at', datetime.now()),
            'errors_occurred': len(error_types) > 0,
            'error_types': error_types,
            'error_desc': error_desc
        })
    except Exception:
        err_msg = f"Error logging Andy's move: {traceback.format_exc()}"
        print_error(ERROR_TYPES.LOGGING, err_msg)


def log_andy_response(session_id, data):
    """Logs Andy's response.

    Args:
        session_id (str): the session_id provided by the client.
        data (dict): the data to upload.

    Data format:
        {
            "text": str,
            "audio_data": bytes,
            "received_at": datetime,
            "response_at": datetime,
        }
    """
    # Upload audio_data and get name
    try:
        audio_name = upload_audio_file(
            data.get("audio_data"))
    except Exception:
        audio_name = ""
        err_msg = f"Failed to upload Andy's response audio: {traceback.format_exc()}"
        log_error(session_id, ERROR_TYPES.AUDIO_UPLOAD, err_msg)
    # Get errors from state_manager
    error_types, error_desc = get_curr_errors(session_id)
    # Set all of the data in a log
    try:
        db = firestore.Client(project=PROJECT_ID)
        log_id = get_curr_log_id(session_id)
        doc_ref = db.collection(GENERAL_LOGS_COLLECTION).document()
        doc_ref.set({
            'session_id': session_id,
            'timestamp': datetime.now(),
            'user_request_log_id': log_id,
            'text': data.get('text', ''),
            'audio_name': audio_name,
            'received_at': data.get('received_at', datetime.now()),
            'response_at': data.get('response_at', datetime.now()),
            'errors_occurred': len(error_types) > 0,
            'error_types': error_types,
            'error_desc': error_desc
        })
    except Exception:
        err_msg = f"Error logging Andy's response: {traceback.format_exc()}"
        print_error(ERROR_TYPES.LOGGING, err_msg)


def log_user_request(session_id, data):
    """Logs user request.

    Args:
        session_id (str): the session_id provided by the client.
        data (dict): the data to upload.

    Data format:
        {
            "text": str,
            "audio_data": bytes,
            "detected_intent": str,
            "detected_params": dict,
            "detected_fulfillment": str,
            "fulfillment_success": bool,
            "fulfillment_params": dict,
            "board_str_before": str,
            "board_str_after": str,
            "received_at": datetime,
            "response_at": datetime,
        }
    """
    # Upload audio_data and get name
    try:
        audio_name = upload_audio_file(
            data.get("audio_data"))
    except Exception:
        audio_name = ""
        err_msg = f"Failed to upload user's request audio: {traceback.format_exc()}"
        log_error(session_id, ERROR_TYPES.AUDIO_UPLOAD, err_msg)
    # Get errors from state_manager
    error_types, error_desc = get_curr_errors(session_id)
    # Set all of the data in a log
    try:
        db = firestore.Client(project=PROJECT_ID)
        doc_ref = db.collection(GENERAL_LOGS_COLLECTION).document()
        doc_ref.set({
            'session_id': session_id,
            'timestamp': datetime.now(),
            'text': data.get('text', ''),
            'audio_name': audio_name,
            'detected_intent': data.get('detected_intent', ''),
            'detected_params': data.get('detected_params', {}),
            'detected_fulfillment': data.get('detected_fulfillment', ''),
            'fulfillment_success': data.get('fulfillment_success', False),
            'fulfillment_params': data.get('fulfillment_params', {}),
            'board_str_before': data.get('board_str_before', ''),
            'board_str_after': data.get('board_str_after', ''),
            'received_at': data.get('received_at', datetime.now()),
            'response_at': data.get('response_at', datetime.now()),
            'errors_occurred': len(error_types) > 0,
            'error_types': error_types,
            'error_desc': error_desc
        })
        # Set the current log_id for linking other responses
        set_curr_log_id(session_id, doc_ref.id)
    except Exception:
        err_msg = f"Error logging user's request: {traceback.format_exc()}"
        print_error(ERROR_TYPES.LOGGING, err_msg)
