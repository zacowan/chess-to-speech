"""
TODO add info about intent
"""

from .utils import get_random_choice

HAPPY_PATH_RESPONSES = [
    "Okay- let's continue playing.",
    "Okay- let's finish this round."
]


def handle():
    return get_random_choice(HAPPY_PATH_RESPONSES), True
