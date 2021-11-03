"""Manages the state for the API (session handling).

The filename of shelve shall correspond to the unique session_id.

Game State Dict:
    {
        "curr_log_id": str | None,
        "game_started": bool | None,
        "chosen_side": bool | None,
        "curr_move_from": str | None,
        "game_finished": bool | None
    }

"""
import shelve

SHELVE_DIRECTORY = "./shelve"


def get_shelve_file(session_id):
    """Returns the name of the shelve file location."""
    return f"{SHELVE_DIRECTORY}/{session_id}"


def set_curr_log_id(session_id, log_id):
    """Sets the current log_id for a session."""
    with shelve.open(get_shelve_file(session_id)) as db:
        db['curr_log_id'] = log_id


def get_curr_log_id(session_id):
    """Gets the current log_id for a session."""
    with shelve.open(get_shelve_file(session_id)) as db:
        return db['curr_log_id']


def get_game_state(session_id):
    """Returns the game state dictionary."""
    with shelve.open(get_shelve_file(session_id)) as db:
        return db


def set_game_started(session_id):
    """Sets game_started to True."""
    with shelve.open(get_shelve_file(session_id)) as db:
        db["game_started"] = True


def set_chosen_side(session_id):
    """Sets chosen_side to True."""
    with shelve.open(get_shelve_file(session_id)) as db:
        db["chosen_side"] = True


def set_curr_move_from(session_id, val):
    """Sets curr_move_from to a new value"""
    with shelve.open(get_shelve_file(session_id)) as db:
        db["curr_move_from"] = val


def set_game_finished(session_id):
    """Sets game_finished to True."""
    with shelve.open(get_shelve_file(session_id)) as db:
        db["game_finished"] = True
