"""
TODO add info about intent
"""
import traceback
from api.logging import log_error, ERROR_TYPES
from api.chess_logic import get_best_move, get_piece_name_at
from .utils import get_random_choice
from api.state_manager import set_fulfillment_params

HAPPY_PATH_RESPONSES = [
    "According to my calculations, you should move your {piece_name} from {from_location} to {to_location}.",
    "Your best move is {from_location} to {to_location}."
]


ERROR_RESPONSES = [
    "Sorry, I'm not sure what your best move is.",
    "Sorry, I don't know what you should do next."
]


def handle(session_id, board_str):
    """TODO add details about method
    """
    static_choice = get_random_choice(HAPPY_PATH_RESPONSES)
    try:
        best_move = get_best_move(board_str)

        from_location = best_move[0:2]
        to_location = best_move[2:4]
        piece_name = get_piece_name_at(board_str, from_location)

        set_fulfillment_params(session_id, params={
            "from_location": from_location,
            "to_location": to_location,
            "piece_name": piece_name,
        })

        return static_choice.format(
            piece_name=piece_name,
            from_location=from_location,
            to_location=to_location
        ), True
    except Exception:
        err_msg = f"Error with calculating best move for user: {traceback.format_exc()}"
        log_error(session_id, ERROR_TYPES.BEST_MOVE, err_msg)
        static_choice = get_random_choice(ERROR_RESPONSES)
        return static_choice, False
