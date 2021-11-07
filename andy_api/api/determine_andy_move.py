"""This module will determine what Andy's move will be.

"""
from .intent_processing.utils import get_random_choice
from .chess_logic import (
    make_move,
    get_best_move,
    check_if_check,
    check_if_checkmate,
    get_piece_name_at
)


HAPPY_PATH_RESPONSES = [
    "I'll move my {piece_name} at {from_location} to {to_location}",
    "Let me move my {piece_name} from {from_location} to {to_location}"
]


def determine_andy_move(board_str):
    """Handles determining a text response for Andy's move.

    Args:
        board_str: the state of the board, as text.

    Returns:
        str: the response that should be given, as text.
        str: the updated board_str that should be given.
        dict: the move_info to log.

    """
    static_choice = get_random_choice(HAPPY_PATH_RESPONSES)

    # Get the best move
    move = get_best_move(board_str)

    # Get logging information
    from_location = move[0:2]
    to_location = move[2:4]
    piece_name = get_piece_name_at(board_str, from_location)
    move_info = {
        "from": from_location,
        "to": to_location
    }

    # Make the best move
    updated_board_str = make_move(board_str, move)

    if check_if_check(updated_board_str):
        return static_choice.format(
            from_location=from_location,
            to_location=to_location,
            piece_name=piece_name) + ', which puts you in check', updated_board_str, move_info

    if check_if_checkmate(updated_board_str):
        return static_choice.format(
            from_location=from_location,
            to_location=to_location,
            piece_name=piece_name) + ", and that's checkmate, I win!", updated_board_str, move_info

    return static_choice.format(
        from_location=from_location,
        to_location=to_location,
        piece_name=piece_name), updated_board_str, move_info
