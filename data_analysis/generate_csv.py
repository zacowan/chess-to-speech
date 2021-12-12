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
from datetime import datetime

PROJECT_ID = "chess-master-andy-mhyo"
LOGGING_SUFFIX = "demo2"

USER_REQUEST_LOGS_BASE_COLLECTION = "user_request_logs"
ANDY_RESPONSE_LOGS_BASE_COLLECTION = "andy_response_logs"
ANDY_MOVE_LOGS_BASE_COLLECTION = "andy_move_logs"
HELP_RESPONSE_LOGS_BASE_COLLECTION = "help_response_logs"

ANDY_MOVE_LOGS_COLLECTION = f"{ANDY_MOVE_LOGS_BASE_COLLECTION}_{LOGGING_SUFFIX}"
USER_REQUEST_LOGS_COLLECTION = f"{USER_REQUEST_LOGS_BASE_COLLECTION}_{LOGGING_SUFFIX}"
ANDY_RESPONSE_LOGS_COLLECTION = f"{ANDY_RESPONSE_LOGS_BASE_COLLECTION}_{LOGGING_SUFFIX}"
HELP_RESPONSE_LOGS_COLLECTION = f"{HELP_RESPONSE_LOGS_BASE_COLLECTION}_{LOGGING_SUFFIX}"

REQUEST_LOG_OUTPUT_DIR = f"{LOGGING_SUFFIX}/logs_by_session_id"
COMPILED_LOGS_PATH = f"{LOGGING_SUFFIX}/compiled_logs_{LOGGING_SUFFIX}.csv"

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
    'played_chess_before': bool,
    'chess_familiarity_score': number,
    'chess_fun_score': number,
    'sus': number,
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
        self.played_chess_before = None
        self.chess_familiarity_score = None
        self.chess_fun_score = None
        self.sus = None

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "average_time_to_response_ms": self.sum_time_to_response / self.num_utterances if self.num_utterances != 0 else 0,
            "average_recording_time_ms": self.sum_recording_time / self.num_utterances if self.num_utterances != 0 else 0,
            "game_length_sec": self.game_length_sec,
            "num_utterances": self.num_utterances,
            "num_fallback": self.num_fallback,
            "num_fulfillment_success": self.num_fulfillment_success,
            "num_fulfillment_fail": self.num_fulfillment_fail,
            "played_chess_before": self.played_chess_before,
            "chess_familiarity_score": self.chess_familiarity_score,
            "chess_fun_score": self.chess_fun_score,
            "sus": self.sus
        }


def read_pre(loc: str, l: list[tuple[str, CompiledLog]]) -> list[CompiledLog]:
    """

    Name
    Played
    Knowledge
    Skill
    Enjoy

    """
    ret: list[CompiledLog] = []
    with open(loc, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row["Name"]
            played = True if row['Played'] == 'Yes' else False
            familiarity = int(row['Knowledge']) + int(row['Skill'])
            enjoy = int(row['Enjoy'])

            for n, cl in l:
                if n == name:
                    cl.played_chess_before = played
                    cl.chess_familiarity_score = familiarity
                    cl.chess_fun_score = enjoy
                    ret.append(cl)

    return ret


def read_post(loc: str) -> list[tuple[str, CompiledLog]]:
    """

    session_id
    Name
    Q1 (p)
    Q2 (n)
    Q3 (p)
    Q4 (n)
    Q5 (p)
    Q6 (n)
    Q7 (p)
    Q8 (n)
    Q9 (p)
    Q10 (n)

    """
    ret: list[tuple[str, CompiledLog]] = []
    with open(loc, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            session_id = row['session_id']
            name = row["Name"]
            odds = int(row['Q1']) - 1 + int(row['Q3']) - 1 + \
                int(row['Q5']) - 1 + int(row['Q7']) - 1 + int(row['Q9']) - 1
            evens = 5 - int(row['Q2']) + 5 - int(row['Q4']) + \
                5 - int(row['Q6']) + 5 - int(row['Q8']) + 5 - int(row['Q10'])

            l = CompiledLog(session_id)
            l.sus = (odds + evens) * 2.5
            ret.append((name, l))

    return ret


def generate_user_request_csv(ret: CompiledLog):
    try:
        session_id = ret.session_id
        db = firestore.Client(project=PROJECT_ID)
        docs = db.collection(USER_REQUEST_LOGS_COLLECTION).where(
            'session_id', '>=', session_id).limit(50).stream()

        with open(f'{REQUEST_LOG_OUTPUT_DIR}/user_requests_log_{session_id}.csv', 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'text', 'detected_fulfillment',
                          'fulfillment_success', 'recording_time_ms', 'time_to_response_ms', 'response_text', 'audio_name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            start_time: datetime = None
            end_time: datetime = None
            for doc in docs:
                req_dict = doc.to_dict()

                print(
                    f"Expected: {session_id} | Actual: {req_dict['session_id'][0:8]}")
                if req_dict['session_id'][0:8] != session_id:
                    break

                if not start_time:
                    start_time = req_dict['timestamp']
                    end_time = start_time

                end_time = max(end_time, req_dict['timestamp'])

                # Get Andy response information
                if len(req_dict['linked_logs']) > 0:
                    andy_response_doc = req_dict['linked_logs'][0].get(
                    ).to_dict()
                    req_dict['response_text'] = andy_response_doc['text']
                    req_dict['time_to_response_ms'] = req_dict['request_time_ms'] + \
                        andy_response_doc['request_time_ms']
                else:
                    req_dict['response_text'] = None
                    req_dict['time_to_response_ms'] = req_dict['request_time_ms']

                # Update compiled log
                ret.sum_time_to_response += req_dict['time_to_response_ms']
                ret.sum_recording_time += req_dict['recording_time_ms']
                ret.num_utterances += 1
                ret.num_fallback += 1 if req_dict['detected_fulfillment'] == 'FALLBACK' else 0
                if req_dict['fulfillment_success'] == True:
                    ret.num_fulfillment_success += 1
                else:
                    ret.num_fulfillment_fail += 1

                for k in USER_REQUEST_REMOVED_KEYS:
                    del req_dict[k]

                writer.writerow(req_dict)

            # Update game time
            if start_time and end_time:
                ret.game_length_sec = (end_time - start_time).total_seconds()

    except Exception:
        print("Error: %s", traceback.format_exc())
        exit(-1)


if __name__ == "__main__":
    # Read post-survey and pre-survey, construct CompiledLog for each
    l = read_post(f"{LOGGING_SUFFIX}/post_survey_{LOGGING_SUFFIX}.csv")
    compiled_logs: list[CompiledLog] = read_pre(
        f"{LOGGING_SUFFIX}/pre_survey_{LOGGING_SUFFIX}.csv", l)
    # Read GCP logs, update CompiledLog for each
    for cl in compiled_logs:
        generate_user_request_csv(cl)
    # Write CompiledLog to csv
    with open(COMPILED_LOGS_PATH, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, list(
            compiled_logs[0].to_dict().keys()))

        writer.writeheader()
        for cl in compiled_logs:
            writer.writerow(cl.to_dict())
