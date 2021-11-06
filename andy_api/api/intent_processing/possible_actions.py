import state_manager
"""This module handles intent processing for WAKE_UP_PHRASE.

Attributes:
    HAPPY_PATH_RESPONSES (list): a list of happy-path responses.
    ERROR_RESPONSES (list): a list of responses for errors.

"""
from .utils import get_random_choice


HAPPY_PATH_RESPONSES = [
    "You can start a game of chess with me!",
]

GAME_STARTED_RESPONSES = [
    "You can tell me a piece to move, ask legal moves for a piece, and ask what your best move is!",
]


def handle():
    if (state_manager.get_game_state["game_started"] == True):
        return get_random_choice(GAME_STARTED_RESPONSES)

    return get_random_choice(HAPPY_PATH_RESPONSES)
# If a game has started: tell user they can make a move (if their turn), 2. ask legal moves for a piece, 3. ask what best move is
# api folder. statemanager.pi ask if game started yet
