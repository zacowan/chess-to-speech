"""Manages the state for the API (session handling).

The filename of shelve shall correspond to the unique session_id.

Game State Dict:
    {
        "curr_log_id": str | None
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
