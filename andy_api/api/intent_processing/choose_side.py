"""This module handles intent processing for CHOOSE_SIDE.

Attributes:
    HAPPY_PATH_RESPONSES (list): a list of happy-path responses.
    ERROR_RESPONSES (list): a list of responses for errors.

"""
from .utils import get_random_choice
from api.state_manager import set_chosen_side, set_fulfillment_params

HAPPY_PATH_RESPONSES = [
    "Okay, you'll go {user_position}.",
    "Good choice, that means you'll go {user_position}.",
    "Ok, then I'll take {andy_side}."
]

HAPPY_PATH_SUFFIXES = [
    "Now, would you like to play on easy difficulty or hard difficulty?",
    "You must choose between easy difficulty and hard difficulty. What is your choice?"
]

ERROR_RESPONSES = [
    "Sorry, black side or white side?",
    "Did you want black side, or white side?"
]


# TODO: add logic with board_str
def handle(session_id, intent_model):
    """Handles choosing a response for the CHOOSE_SIDE intent.

    Args:
        intent_model: the intent model to parse.

    Returns:
        str: the response that should be given, as text.
        boolean: whether or not the intent was handled successfully.

    """
    if intent_model.all_required_params_present is True:
        static_choice = get_random_choice(HAPPY_PATH_RESPONSES)
        suffix = get_random_choice(HAPPY_PATH_SUFFIXES)
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

        # Update game state
        set_chosen_side(session_id, user_side)

        # Log the params
        set_fulfillment_params(session_id, params={
            "chosen_side": user_side
        })

        return static_choice.format(andy_side=andy_side,
                                    andy_position=andy_position,
                                    user_side=user_side,
                                    user_position=user_position) + suffix, True
    else:
        return get_random_choice(ERROR_RESPONSES), False
