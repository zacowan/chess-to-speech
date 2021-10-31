"""Handles logging information to Firestore.
"""

from datetime import datetime
from google.cloud import firestore

from .state_manager import set_curr_log_id, get_curr_log_id

PROJECT_ID = "chess-master-andy-mhyo"
INTENT_LOGS_COLLECTION = "intent_logs_staging"
ERROR_LOGS_COLLECTION = "error_logs_staging"

db = firestore.Client(project=PROJECT_ID)


def create_intent_log(data):
    """Creates a log entry for an intent.

    Args:
        data (dict): the data that the document should contain.

    Data Format:
        {
            "session_id": str,
            "board_str_before": str,
            "board_str_after": str,
            "detected_intent": str,
            "intent_success": bool,
            "andy_response_text": str,
            "user_input_text": str,
            "user_input_audio_name": str
        }

    """
    doc_ref = db.collection(INTENT_LOGS_COLLECTION).document()
    doc_ref.set(data)
    doc_ref.set({'timestamp': datetime.now()}, merge=True)
    set_curr_log_id(data['session_id'], doc_ref.id)


def update_intent_log_with_audio_response(session_id, andy_response_audio_location):
    """Updates an existing log entry for an intent.

    Args:
        log_id (str): the ID of the intent log entry to update.
        andy_response_audio_location (str): the location of Andy's response.

    """
    log_id = get_curr_log_id(session_id)
    doc_ref = db.collection(INTENT_LOGS_COLLECTION).document(log_id)
    doc_ref.set(
        {"andy_response_audio_location": andy_response_audio_location}, merge=True)
    # Reset curr_log_id
    set_curr_log_id(session_id, None)
