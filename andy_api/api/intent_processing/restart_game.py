"""
TODO add info about intent
"""

from .utils import get_random_choice
from api.state_manager import restart_game
from api.chess_logic import get_new_board

HAPPY_PATH_RESPONSES = [
    "Okay- let's play again!",
    "Lets restart the round..."
]

def handle(session_id):
    static_choice = get_random_choice(HAPPY_PATH_RESPONSES)
    restart_game(session_id)
    updated_board_str = get_new_board()
    return static_choice, True, updated_board_str