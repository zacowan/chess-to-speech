"""
TODO add info about intent
"""

from .utils import get_random_choice

HAPPY_PATH_RESPONSES = [
    "Okay - let's continue playing then.",
    "Okay - let's finish this game then."
]


def handle():
    return get_random_choice(HAPPY_PATH_RESPONSES), True
