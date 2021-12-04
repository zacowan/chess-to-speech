"""
TODO add info about intent
"""

from .utils import get_random_choice

HAPPY_PATH_RESPONSES = [
    "I hear you want to restart, is that right?",
    "It seems like you want to start over, is that right?"
]


def handle():
    return get_random_choice(HAPPY_PATH_RESPONSES), True
