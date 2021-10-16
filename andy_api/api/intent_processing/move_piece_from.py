"""This module handles intent processing for MOVE_PIECE.

Attributes:
    HAPPY_PATH_RESPONSES (list): a list of happy-path responses.
    ERROR_RESPONSES (list): a list of responses for errors.

"""
from .utils import get_random_choice


HAPPY_PATH_RESPONSES = [
    "Okay, and where would you like to move to?",
    "And where to?"
]

ERROR_RESPONSES = [
    "Sorry, the piece at where?",
    "Sorry, the piece at which location?"
]


def handle(intent_model):
    """Handles choosing a response for the MOVE_PIECE intent.

    Args:
        intent_model: the intent model to parse.

    Returns:
        str: the response that should be given, as text.

    """
    # TODO: add a check for if a game has started
    # TODO: add a check if player has chosen a side
    if intent_model.all_required_params_present is True:
        static_choice = get_random_choice(HAPPY_PATH_RESPONSES)

        # TODO: add check that the move is valid

        return static_choice
    else:
        static_choice = get_random_choice(ERROR_RESPONSES)

        return static_choice
