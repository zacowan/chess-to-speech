"""Handles logging information to Firestore.
"""

from datetime import datetime
from google.cloud import firestore

PROJECT_ID = "chess-master-andy-mhyo"
INTENT_LOGS_COLLECTION = "intent_logs"
ERROR_LOGS_COLLECTION = "error_logs"

db = firestore.Client(project=PROJECT_ID)


def create_intent_log(session_id):
    """Creates a log entry for an intent.

    Args:
        session_id (str): the session_id for the intent.

    Returns:
        str: the ID of the log entry.

    """
    doc_ref = db.collection(INTENT_LOGS_COLLECTION).document()
    doc_ref.set({
        'session_id': session_id,
        'timestamp': datetime.now()
    })
    return doc_ref.id


def update_intent_log(log_id, data):
    """Updates an existing log entry for an intent.

    Args:
        log_id (str): the ID of the intent log entry to update.
        data (dict): the data to merge with the log entry.

    """
    doc_ref = db.collection(INTENT_LOGS_COLLECTION).document(log_id)
    doc_ref.set(data, merge=True)
