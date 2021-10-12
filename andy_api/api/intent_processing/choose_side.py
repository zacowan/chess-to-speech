"""This module handles intent processing for CHOOSE_SIDE."""
from .utils import get_random_choice, RESPONSE_LIST, RESPONSE_TYPES, ERROR_RESPONSE_LIST


def handle(intent_model):
    """Handles choosing a response for the CHOOSE_SIDE intent.

    Args:
        intent_model: the intent model to parse.

    Returns:
        str: the response that should be given, as text.

    """
    # TODO: add a check for if a game has started
    # TODO: add a check if player has already chosen a side
    if intent_model.all_required_params_present is True:
        static_choice = get_random_choice(
            RESPONSE_LIST, RESPONSE_TYPES.CHOOSE_SIDE)
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
                                    user_position=user_position)
    else:
        return get_random_choice(
            ERROR_RESPONSE_LIST,
            RESPONSE_TYPES.CHOOSE_SIDE)
