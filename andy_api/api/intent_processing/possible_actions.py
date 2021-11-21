"""This module handles intent processing for POSSIBLE_ACTIONS.

Attributes:
    HAPPY_PATH_RESPONSES (list): a list of happy-path responses.
    ERROR_RESPONSES (list): a list of responses for errors.

"""
from .utils import get_random_choice

HAPPY_PATH_RESPONSES = [
    "I can perform a move for you, tell you how a named piece moves, give you advice on your next move, I can undo a move, or I can restart the game.",
    "I can move a piece for you, tell you how named pieces move, help you make your next move, I can undo a move, and I can restart the game."
]


def handle():
    return get_random_choice(HAPPY_PATH_RESPONSES), True
