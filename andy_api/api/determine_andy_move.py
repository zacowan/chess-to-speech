"""This module will determine what Andy's move will be.

"""
from .intent_processing.utils import get_random_choice
from .state_manager import set_game_finished
from .chess_logic import (
    get_board_str_with_move,
    get_best_move,
    check_if_check,
    check_if_checkmate,
    get_piece_name_at
)
from .intent_processing.choose_side import STARTING_BOARD_STR


HAPPY_PATH_RESPONSES = [
    "Now I'll move my {piece_name} to {to_location}",
    "Let me move my {piece_name} to {to_location}",
    "For my turn, I'll move my {piece_name} at {from_location} to {to_location}"
]

PROMPT_PLAYER_TURN_GAME_START_SUFFIXES = [
    ". Whenever you're ready, I can make a move for you or tell you what else you can do.",
    ". I can make your move or tell you what else you can do whenver you are ready."
]


CHECK_SUFFIXES = [
    ", which puts you in check.",
    ", and that means you're in check."
]

CHECKMATE_SUFFIXES = [
    ", which is checkmate. I win!",
    ", and that's checkmate. I'm the winner!"
]


def get_suffix(original_board_str):
    if original_board_str == STARTING_BOARD_STR:
        return " " + get_random_choice(PROMPT_PLAYER_TURN_GAME_START_SUFFIXES)
    else:
        return ""


def determine_andy_move(session_id, board_str):
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
    updated_board_str = get_board_str_with_move(board_str, move)

    if check_if_checkmate(updated_board_str):
        set_game_finished(session_id)
        suffix = get_random_choice(CHECKMATE_SUFFIXES)
        return static_choice.format(
            from_location=from_location,
            to_location=to_location,
            piece_name=piece_name) + suffix, updated_board_str, move_info
    elif check_if_check(updated_board_str):
        suffix = get_random_choice(CHECK_SUFFIXES)
        return static_choice.format(
            from_location=from_location,
            to_location=to_location,
            piece_name=piece_name) + suffix, updated_board_str, move_info

    # Get suffix
    suffix = get_suffix(board_str)

    return static_choice.format(
        from_location=from_location,
        to_location=to_location,
        piece_name=piece_name) + suffix, updated_board_str, move_info
