"""This module handles intent processing for START_GAME.

Attributes:
    HAPPY_PATH_RESPONSES (list): a list of happy-path responses.
    ERROR_RESPONSES (list): a list of responses for errors.

"""
from .utils import get_random_choice


HAPPY_PATH_RESPONSES = [
    "Awesome, I'm so excited. But first, do you want black or white side?",
    "Okay, would you like black or white side?",
    "Alright, let's do this. Did you want black side or white side?"
]


def handle():
    static_choice = get_random_choice(HAPPY_PATH_RESPONSES)
    return static_choice, True
