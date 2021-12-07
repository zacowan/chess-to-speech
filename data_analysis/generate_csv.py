"""

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

Help Response Log:
    {
        "session_id": str,
        "timestamp": datetime,

        "help_type": str,
        "text": str,
        "audio_name": str,

        "request_time_ms": number,

        "errors_occurred": bool,
        "error_types": list(str),
        "error_desc": list(str),
    }

Error Types:
    "INTENT FULFILLMENT TTS LOGGING AUDIO_UPLOAD BEST_MOVE UNKNOWN"

"""
from google.cloud import firestore
import traceback
import csv

PROJECT_ID = "chess-master-andy-mhyo"
LOGGING_SUFFIX = "development"

USER_REQUEST_LOGS_BASE_COLLECTION = "user_request_logs"
ANDY_RESPONSE_LOGS_BASE_COLLECTION = "andy_response_logs"
ANDY_MOVE_LOGS_BASE_COLLECTION = "andy_move_logs"
HELP_RESPONSE_LOGS_BASE_COLLECTION = "help_response_logs"

ANDY_MOVE_LOGS_COLLECTION = f"{ANDY_MOVE_LOGS_BASE_COLLECTION}_{LOGGING_SUFFIX}"
USER_REQUEST_LOGS_COLLECTION = f"{USER_REQUEST_LOGS_BASE_COLLECTION}_{LOGGING_SUFFIX}"
ANDY_RESPONSE_LOGS_COLLECTION = f"{ANDY_RESPONSE_LOGS_BASE_COLLECTION}_{LOGGING_SUFFIX}"
HELP_RESPONSE_LOGS_COLLECTION = f"{HELP_RESPONSE_LOGS_BASE_COLLECTION}_{LOGGING_SUFFIX}"

USER_REQUEST_REMOVED_KEYS = [
    'session_id',
    'detected_intent',
    'board_str_before',
    'board_str_after',
    'error_types',
    'error_desc',
    'linked_logs',
    'fulfillment_params',
    'request_time_ms',
    'errors_occurred'
]

"""

{
    'session_id': str,
    'average_time_to_response_ms': number,
    'average_recording_time_ms': number,
    'game_length_sec': number,
    'num_utterances': number,
    'num_fallback': number,
    'num_fulfillment_success': number,
    'num_fulfillment_fail': number,
}

"""
compiled_logs: list[dict] = []


class CompiledLog:
    def __init__(self, id) -> None:
        self.session_id = id
        self.sum_time_to_response = 0
        self.sum_recording_time = 0
        self.game_length_sec = 0
        self.num_utterances = 0
        self.num_fallback = 0
        self.num_fulfillment_success = 0
        self.num_fulfillment_fail = 0

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "average_time_to_response_ms": self.sum_time_to_response / self.num_utterances,
            "average_recording_time_ms": self.sum_recording_time / self.num_utterances,
            "game_length_sec": self.game_length_sec,
            "num_utterances": self.num_utterances,
            "num_fallback": self.num_fallback,
            "num_fulfillment_success": self.num_fulfillment_success,
            "num_fulfillment_fail": self.num_fulfillment_fail
        }


def user_request_csv():
    try:
        session_id = '9b3594bb-c5ba-4357-85ae-e54b6cc72411'
        db = firestore.Client(project=PROJECT_ID)
        docs = db.collection(USER_REQUEST_LOGS_COLLECTION).where(
            'session_id', '==', '9b3594bb-c5ba-4357-85ae-e54b6cc72411').order_by('timestamp').stream()

        with open(f'user_request_logs_{session_id[0:8]}.csv', 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'text', 'detected_fulfillment',
                          'fulfillment_success', 'recording_time_ms', 'time_to_response_ms', 'response_text', 'audio_name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for doc in docs:
                req_dict = doc.to_dict()

                # Get Andy response information
                andy_response_doc = req_dict['linked_logs'][0].get().to_dict()
                req_dict['response_text'] = andy_response_doc['text']
                req_dict['time_to_response_ms'] = req_dict['request_time_ms'] + \
                    andy_response_doc['request_time_ms']

                for k in USER_REQUEST_REMOVED_KEYS:
                    del req_dict[k]

                writer.writerow(req_dict)

    except Exception:
        print("Error: %s", traceback.format_exc())


if __name__ == "__main__":
    user_request_csv()
