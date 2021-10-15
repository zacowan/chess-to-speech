"""This module handles intent processing for MOVE_PIECE.

Attributes:
    HAPPY_PATH_RESPONSES (list): a list of happy-path responses.
    ERROR_RESPONSES (list): a list of responses for errors.

"""
from .utils import get_random_choice


HAPPY_PATH_RESPONSES = [
    "Okay, moving {from_location} to {to_location}.",
    "Great, {from_location} will go to {to_location}."
]

ERROR_RESPONSES_FROM = [
    "Sorry, you want to move to {to_location} from where?",
    "Sorry, which piece did you want to move?"
]

ERROR_RESPONSES_TO = [
    "Sorry, you want to move to where?",
    "Sorry, you want to move from {from_location} to where?"
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
        from_location = intent_model.parameters["fromLocation"]
        to_location = intent_model.parameters["toLocation"]

        # TODO: add check that the move is valid

        return static_choice.format(from_location=from_location, to_location=to_location)
    elif not intent_model.parameters["fromLocation"]:
        static_choice = get_random_choice(ERROR_RESPONSES_FROM)
        to_location = intent_model.parameters["toLocation"]

        return static_choice.format(to_location=to_location)
    else:
        static_choice = get_random_choice(ERROR_RESPONSES_TO)
        from_location = intent_model.parameters["fromLocation"]

        return static_choice.format(from_location=from_location)
