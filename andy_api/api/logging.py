"""Handles logging information to Firestore.

User Request Log:
    {
        "session_id": str,
        "timestamp": datetime,

        "text": str,
        "audio_name": str,

        "detected_intent": str,

        "detected_fulfillment": str,
        "fulfillment_success": bool,
        "fulfillment_params": dict,

        "board_str_before": str,
        "board_str_after": str,

        "request_time_ms": number,
        "recording_time_ms": number,

        "errors_occurred": bool,
        "error_types": list(str),
        "error_desc": list(str),

        "linked_logs": list(reference),
    }

Andy Response Log:
    {
        "session_id": str,
        "timestamp": datetime,
        "user_request_log_id": str,

        "text": str,
        "audio_name": str,

        "request_time_ms": number,

        "errors_occurred": bool,
        "error_types": list(str),
        "error_desc": list(str),
    }

Andy Move Log:
    {
        "session_id": str,
        "timestamp": datetime,
        "user_request_log_id": str,

        "move_info": {
            "from": str,
            "to": str,
        },
        "board_str_before": str,
        "board_str_after": str,

        "request_time_ms": number,

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

from .state_manager import get_fulfillment_params, set_curr_log_id, get_curr_log_id, set_curr_errors, get_curr_errors
from .speech_text_processing import upload_audio_file

PROJECT_ID = "chess-master-andy-mhyo"
LOGGING_SUFFIX = os.environ['LOGGING_SUFFIX']
USER_REQUEST_LOGS_BASE_COLLECTION = "user_request_logs"
ANDY_RESPONSE_LOGS_BASE_COLLECTION = "andy_response_logs"
ANDY_MOVE_LOGS_BASE_COLLECTION = "andy_move_logs"
ANDY_MOVE_LOGS_COLLECTION = f"{ANDY_MOVE_LOGS_BASE_COLLECTION}_{LOGGING_SUFFIX}"
USER_REQUEST_LOGS_COLLECTION = f"{USER_REQUEST_LOGS_BASE_COLLECTION}_{LOGGING_SUFFIX}"
ANDY_RESPONSE_LOGS_COLLECTION = f"{ANDY_RESPONSE_LOGS_BASE_COLLECTION}_{LOGGING_SUFFIX}"

ERROR_TYPES = Enum(
    "ERROR_TYPES",
    "INTENT FULFILLMENT TTS LOGGING AUDIO_UPLOAD BEST_MOVE UNKNOWN"
)


def compute_request_time(start, end):
    """Returns the time (ms) between end and start."""
    return (end - start).total_seconds() * 1000


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
    # Get errors from state_manager
    error_types, error_desc = get_curr_errors(session_id)
    # Set all of the data in a log
    try:
        db = firestore.Client(project=PROJECT_ID)
        log_id = get_curr_log_id(session_id)
        doc_ref = db.collection(ANDY_MOVE_LOGS_COLLECTION).document()
        doc_ref.set({
            'session_id': session_id,
            'timestamp': datetime.now(),
            'user_request_log_id': log_id,
            'move_info': data.get('move_info', {}),
            'board_str_before': data.get('board_str_before', ''),
            'board_str_after': data.get('board_str_after', ''),
            'request_time_ms': compute_request_time(data.get('received_at', datetime.now()), data.get('response_at', datetime.now())),
            'errors_occurred': len(error_types) > 0,
            'error_types': error_types,
            'error_desc': error_desc
        })
        # Link to the request log
        req_doc_ref = db.collection(
            USER_REQUEST_LOGS_COLLECTION).document(log_id)
        req_doc_ref.set({
            'linked_logs': [doc_ref]
        }, merge=True)
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
        doc_ref = db.collection(ANDY_RESPONSE_LOGS_COLLECTION).document()
        doc_ref.set({
            'session_id': session_id,
            'timestamp': datetime.now(),
            'user_request_log_id': log_id,
            'text': data.get('text', ''),
            'audio_name': audio_name,
            'request_time_ms': compute_request_time(data.get('received_at', datetime.now()), data.get('response_at', datetime.now())),
            'errors_occurred': len(error_types) > 0,
            'error_types': error_types,
            'error_desc': error_desc
        })
        # Link to the request log
        req_doc_ref = db.collection(
            USER_REQUEST_LOGS_COLLECTION).document(log_id)
        req_doc_ref.set({
            'linked_logs': [doc_ref]
        }, merge=True)
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
            "detected_fulfillment": str,
            "fulfillment_success": bool,
            "board_str_before": str,
            "board_str_after": str,
            "received_at": datetime,
            "response_at": datetime,
            "recording_time_ms": float,
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
    # Get fulfillment params from state_manager
    fulfillment_params = get_fulfillment_params(session_id)
    # Set all of the data in a log
    try:
        db = firestore.Client(project=PROJECT_ID)
        doc_ref = db.collection(USER_REQUEST_LOGS_COLLECTION).document()
        doc_ref.set({
            'session_id': session_id,
            'timestamp': datetime.now(),
            'text': data.get('text', ''),
            'audio_name': audio_name,
            'detected_intent': data.get('detected_intent', ''),
            'detected_fulfillment': data.get('detected_fulfillment', ''),
            'fulfillment_success': data.get('fulfillment_success', False),
            'fulfillment_params': fulfillment_params,
            'board_str_before': data.get('board_str_before', ''),
            'board_str_after': data.get('board_str_after', ''),
            'request_time_ms': compute_request_time(data.get('received_at', datetime.now()), data.get('response_at', datetime.now())),
            'errors_occurred': len(error_types) > 0,
            'error_types': error_types,
            'error_desc': error_desc,
            'linked_logs': [],
            'recording_time_ms': data.get('recording_time_ms', -1)
        })
        # Set the current log_id for linking other responses
        set_curr_log_id(session_id, doc_ref.id)
    except Exception:
        err_msg = f"Error logging user's request: {traceback.format_exc()}"
        print_error(ERROR_TYPES.LOGGING, err_msg)
