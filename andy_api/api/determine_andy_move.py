"""This module will determine what Andy's move will be.

"""
from .intent_processing.utils import get_random_choice


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

    """
    static_choice = get_random_choice(HAPPY_PATH_RESPONSES)

    updated_board_str = board_str

    # TODO: determine move based on board_str, generate new board_str

    from_location = "E3"
    to_location = "E5"
    piece_name = "pawn"

    return static_choice.format(
        from_location=from_location,
        to_location=to_location,
        piece_name=piece_name), updated_board_str
