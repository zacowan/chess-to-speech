"""This module handles intent processing for CHOOSE_SIDE.

Attributes:
    HAPPY_PATH_RESPONSES (list): a list of happy-path responses.
    ERROR_RESPONSES (list): a list of responses for errors.

"""
import os
from .utils import get_random_choice
from api.state_manager import set_chosen_side, set_game_started, set_fulfillment_params

import chess

DEFAULT_BOARD_STR = chess.STARTING_FEN
DEMO_BOARD_STR = "r2qk2r/pb4pp/1n2Pb2/2B2Q2/p1p5/2P5/2B2PPP/RN2R1K1 w - - 1 0"
BOARD_MODE = os.environ.get("STARTING_BOARD")

STARTING_BOARD_STR = DEMO_BOARD_STR if BOARD_MODE == "demo" else DEFAULT_BOARD_STR

HAPPY_PATH_RESPONSES = [
    "Okay, you'll go {user_position}.",
    "Good choice, that means you'll go {user_position}.",
    "Ok, then I'll take {andy_side}."
]

HAPPY_PATH_SUFFIXES = [
    "Whenever you're ready, I can make a move for you. To move a piece, you can say something like 'pawn to E5', or, 'B3 to F3'. We'll play till one of us wins, or whenever you'd like to stop.",
    "When you're ready to move a piece, you can say something like 'pawn to C4', or, 'E7 to E5'. We'll play out the game till the end, or when you tell me you're done."
]

ERROR_RESPONSES = [
    "Sorry, black side or white side?",
    "Did you want black side, or white side?"
]


def get_suffix(user_side):
    if user_side == "white":
        return " " + get_random_choice(HAPPY_PATH_SUFFIXES)
    else:
        return ""


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
        # Log the params
        set_fulfillment_params(session_id, params={
            "chosen_side": user_side
        })

        suffix = get_suffix(user_side)

        return static_choice.format(andy_side=andy_side,
                                    andy_position=andy_position,
                                    user_side=user_side,
                                    user_position=user_position) + suffix, True, STARTING_BOARD_STR
    else:
        return get_random_choice(ERROR_RESPONSES), False, None
