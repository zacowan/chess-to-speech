"""This module handles intent processing for CHOOSE_SIDE.

Attributes:
    HAPPY_PATH_RESPONSES (list): a list of happy-path responses.
    ERROR_RESPONSES (list): a list of responses for errors.

"""
from .utils import get_random_choice


HAPPY_PATH_RESPONSES = [
    "Great, since you're on {user_side} side, you'll go {user_position}.",
    "Good choice, that means you'll go {user_position}.",
    "Sweet, that means I'll go {andy_position} and you'll go {user_position}.",
    "That leaves me {andy_side}, meaning you'll go {user_position}."
]

ERROR_RESPONSES = [
    "Sorry, you can only choose between black or white. Which side do you choose?",
    "Oh, you should choose between black or white. What'll it be?"
]


def handle(intent_model):
    """Handles choosing a response for the CHOOSE_SIDE intent.

    Args:
        intent_model: the intent model to parse.

    Returns:
        str: the response that should be given, as text.
        boolean: whether or not the intent was handled successfully.

    """
    # TODO: add a check for if a game has started
    # TODO: add a check if player has already chosen a side

    if intent_model.all_required_params_present is True:
        static_choice = get_random_choice(HAPPY_PATH_RESPONSES)
        board_side = intent_model.parameters["BoardSide"]

        black_side = "black"
        white_side = "white"
        first_pos = "first"
        second_pos = "second"

        andy_position = second_pos
        andy_side = black_side
        user_position = first_pos
        user_side = board_side

        if board_side == black_side:
            andy_position = first_pos
            andy_side = white_side
            user_position = second_pos

        return static_choice.format(andy_side=andy_side,
                                    andy_position=andy_position,
                                    user_side=user_side,
                                    user_position=user_position), True
    else:
        return get_random_choice(ERROR_RESPONSES), False
