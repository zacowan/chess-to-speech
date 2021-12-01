"""
TODO add info about intent
"""

import os
from .utils import get_random_choice
from api.state_manager import set_game_started, set_difficulty_selection, set_fulfillment_params, get_game_state

import chess

DEFAULT_BOARD_STR = chess.STARTING_FEN
DEMO_BOARD_STR = "r2qk2r/pb4pp/1n2Pb2/2B2Q2/p1p5/2P5/2B2PPP/RN2R1K1 w - - 1 0"
BOARD_MODE = os.environ.get("STARTING_BOARD")

STARTING_BOARD_STR = DEMO_BOARD_STR if BOARD_MODE == "demo" else DEFAULT_BOARD_STR

HAPPY_PATH_RESPONSES = [
    "Great. You've selected {difficulty_selection} difficulty.",
    "Perfect. This game will be played in {difficulty_selection} difficulty"
]

HAPPY_PATH_SUFFIXES = [
    "Whenever you're ready, I can make a move for you or tell you what else you can do. To move a piece, you can say 'pawn to E5', or, 'B3 to F3'.",
    "I can make your move when you're ready, or I can tell you what else you can do. To move a piece, you can say 'pawn to C4', or, 'E7 to E5'."
]

ERROR_RESPONSES = [
    "Sorry, you must select between easy difficulty and hard difficulty.",
    "Sorry- I didn't understand your difficulty selection. Please choose either easy or hard."
]

def get_suffix(session_id):
    game_state = get_game_state(session_id)
    chosen_side = game_state["chosen_side"]

    if chosen_side == "white":
        return " " + get_random_choice(HAPPY_PATH_SUFFIXES)
    else:
        return ""

def handle(session_id, intent_model):
    if intent_model.all_required_params_present is True:
        static_choice = get_random_choice(HAPPY_PATH_RESPONSES)
        difficulty_selection = intent_model.parameters["DifficultySelection"]
        difficulty_selection = difficulty_selection.lower()
        suffix = get_suffix(session_id)

        # Update game state.
        set_game_started(session_id)
        set_difficulty_selection(session_id, difficulty_selection)

        # Log the fulfillment params.
        set_fulfillment_params(session_id, params={
            "difficulty_selection": difficulty_selection
        })

        return static_choice.format(difficulty_selection=difficulty_selection) + suffix, True, STARTING_BOARD_STR
    else:
        return get_random_choice(ERROR_RESPONSES), False, None