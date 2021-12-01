"""
TODO add info about intent
"""

from .utils import get_random_choice
from .choose_side import STARTING_BOARD_STR
from api.state_manager import set_fulfillment_params
from api.state_manager import restart_game

HAPPY_PATH_RESPONSES = [
    "Okay- let's play again.",
    "Okay- let's restarts the game."
]


def handle(session_id, board_str):
    static_choice = get_random_choice(HAPPY_PATH_RESPONSES)

    restart_game(session_id)

    # Log the fulfillment params
    set_fulfillment_params(session_id, params={
        "curr_board_str": board_str,
        "updated_board_str": STARTING_BOARD_STR
    })

    return static_choice, True, STARTING_BOARD_STR
