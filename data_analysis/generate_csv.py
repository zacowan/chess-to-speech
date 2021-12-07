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


def user_request_csv():
    pass
