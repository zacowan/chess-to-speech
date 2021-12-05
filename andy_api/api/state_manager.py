"""Manages the state for the API (session handling).

The filename of shelve shall correspond to the unique session_id.

Game State Dict:
    {
        "curr_log_id": str | None,
        "curr_err_type": list,
        "curr_err_desc": list,
        "fulfillment_params": dict,
        "game_started": bool | None,
        "chosen_side": str | None,
        "game_finished": bool | None
        "difficulty_selection:: str | None
    }

"""
import shelve

SHELVE_DIRECTORY = "./shelve"


def get_fulfillment_params(session_id):
    """Get the fulfillment params."""
    with shelve.open(get_shelve_file(session_id)) as db:
        params = db.get("fulfillment_params", {})
        return params


def set_fulfillment_params(session_id, params):
    """Set the fulfillment params."""
    with shelve.open(get_shelve_file(session_id)) as db:
        db["fulfillment_params"] = params


def get_curr_errors(session_id):
    """Gets the list of current errors."""
    with shelve.open(get_shelve_file(session_id)) as db:
        # Get current list
        err_types = db.get("curr_err_type", [])
        err_descs = db.get("curr_err_desc", [])

        # Reset list of errors
        db["curr_err_type"] = []
        db["curr_err_desc"] = []

        return err_types, err_descs


def set_curr_errors(session_id, err_type, err_desc):
    """Stores the error in the list of current errors."""
    with shelve.open(get_shelve_file(session_id)) as db:
        # Get current list
        err_types = db.get("curr_err_type", [])
        err_descs = db.get("curr_err_desc", [])

        # Update list
        err_types.append(err_type)
        err_descs.append(err_desc)

        # Update list in shelve
        db["curr_err_type"] = err_types
        db["curr_err_desc"] = err_descs


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
        return db.get('curr_log_id')


def get_game_state(session_id):
    """Returns the game state dictionary.

    Returns:
        {
            "game_started": bool | None,
            "chosen_side": str | None,
            "game_finished": bool | None,
            "board_stack": [] | None,
            "difficulty_selection": str | None
        }

    """
    with shelve.open(get_shelve_file(session_id)) as db:
        game_state = {
            "game_started": db.get("game_started"),
            "chosen_side": db.get("chosen_side"),
            "game_finished": db.get("game_finished"),
            "board_stack": db.get("board_stack"),
            "difficulty_selection": db.get("difficulty_selection")
        }
        return game_state


def set_game_started(session_id):
    """Sets game_started to True."""
    with shelve.open(get_shelve_file(session_id)) as db:
        db["game_started"] = True


def set_chosen_side(session_id, val):
    """Sets chosen_side to a new value."""
    with shelve.open(get_shelve_file(session_id)) as db:
        db["chosen_side"] = val


def set_difficulty_selection(session_id, val):
    """Sets difficulty_selection to a new value"""
    with shelve.open(get_shelve_file(session_id)) as db:
        db["difficulty_selection"] = val


def set_game_finished(session_id):
    """Sets game_finished to True."""
    with shelve.open(get_shelve_file(session_id)) as db:
        db["game_finished"] = True


def restart_game(session_id):
    """Resets game state to what it is before game has started."""
    with shelve.open(get_shelve_file(session_id)) as db:
        db["game_started"] = False
        db["chosen_side"] = None
        db["game_finished"] = False
        db["board_stack"] = []
        db["difficulty_selection"] = None
        


def get_board_stack(session_id):
    """Gets current board stack with board state before player's last move."""
    with shelve.open(get_shelve_file(session_id)) as db:
        if(db.get('board_stack') == None):
            return []
        else:
            return db.get('board_stack')


def set_board_stack(session_id, val):
    """Sets current board stack, should be called every time BEFORE player makes VALID move."""
    with shelve.open(get_shelve_file(session_id)) as db:
        db["board_stack"] = val
