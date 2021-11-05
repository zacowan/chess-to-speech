"""This module handles intent processing for CHOOSE_SIDE.

Attributes:
    HAPPY_PATH_RESPONSES (list): a list of happy-path responses.
    ERROR_RESPONSES (list): a list of responses for errors.

"""
from .utils import get_random_choice
from api.state_manager import set_chosen_side, set_game_started

import chess

import os

DEMO_BOARD_STR = "r2qk2r/pb4pp/1n2Pb2/2B2Q2/p1p5/2P5/2B2PPP/RN2R1K1 w - - 1 0"

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
        set_game_started(session_id)
        set_chosen_side(session_id, user_side)

        starting_board_str = chess.Board().board_fen
        if(os.environ['DEMO_MODE'] == True):
            starting_board_str = DEMO_BOARD_STR

        return static_choice.format(andy_side=andy_side,
                                    andy_position=andy_position,
                                    user_side=user_side,
                                    user_position=user_position), True, starting_board_str
    else:
        return get_random_choice(ERROR_RESPONSES), False, None
