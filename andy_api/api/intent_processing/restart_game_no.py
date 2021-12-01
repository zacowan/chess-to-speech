"""
TODO add info about intent
"""

from .utils import get_random_choice
from api.state_manager import set_fulfillment_params

HAPPY_PATH_RESPONSES = [
    "Okay- let's continue playing.",
    "Okay- let's finish this round."
]

def handle(session_id, board_str):
    static_choice = get_random_choice(HAPPY_PATH_RESPONSES)

     # Log the fulfillment params
    set_fulfillment_params(session_id, params={
        "curr_board_str": board_str,
    })

    return static_choice, True, board_str