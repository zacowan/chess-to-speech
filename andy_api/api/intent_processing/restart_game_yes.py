"""
TODO add info about intent
"""

from .utils import get_random_choice
from api.state_manager import set_fulfillment_params
from api.state_manager import restart_game
from api.chess_logic import get_new_board

HAPPY_PATH_RESPONSES = [
    "Okay- let's play again.",
    "Okay- let's restarts the game."
]

def handle(session_id, board_str):
    static_choice = get_random_choice(HAPPY_PATH_RESPONSES)

    restart_game(session_id)

    updated_board_str = get_new_board()

     # Log the fulfillment params
    set_fulfillment_params(session_id, params={
        "curr_board_str": board_str,
        "updated_board_str": updated_board_str
    })

    return static_choice, True, updated_board_str