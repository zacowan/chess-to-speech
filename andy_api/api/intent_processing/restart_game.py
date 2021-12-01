"""
TODO add info about intent
"""

from .utils import get_random_choice

HAPPY_PATH_RESPONSES = [
    "Are you sure you'd like to restart the game?",
    "Would you really like to start another round?"
]


def handle():
    return get_random_choice(HAPPY_PATH_RESPONSES), True
