"""This module handles intent processing for WAKE_UP_PHRASE.

Attributes:
    HAPPY_PATH_RESPONSES (list): a list of happy-path responses.
    ERROR_RESPONSES (list): a list of responses for errors.

"""
from .utils import get_random_choice


BEFORE_GAME_RESPONSES = [
    "You can start a game of chess with me!",
]

GAME_STARTED_RESPONSES = [
    "You can move a piece, ask legal moves for a piece, and ask what your best move is!",
]


def handle_before_game():
    return get_random_choice(BEFORE_GAME_RESPONSES), True


def hande_game_started():
    return get_random_choice(GAME_STARTED_RESPONSES), True

# If a game has started: tell user they can make a move (if their turn), 2. ask legal moves for a piece, 3. ask what best move is
# api folder. statemanager.pi ask if game started yet
