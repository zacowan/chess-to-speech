"""This module handles intent processing for WAKE_UP_PHRASE.

Attributes:
    HAPPY_PATH_RESPONSES (list): a list of happy-path responses.
    ERROR_RESPONSES (list): a list of responses for errors.

"""
from .utils import get_random_choice


HAPPY_PATH_RESPONSES = [
    "Awesome, I'm so excited. But first, which side would you like?",
    "Okay, what side do you want to play on?",
    "Alright, let's do this. Which side do you want?"
]


def handle():
    static_choice = get_random_choice(HAPPY_PATH_RESPONSES)
    return static_choice, True
