"""This module handles intent processing for WAKE_UP_PHRASE.

Attributes:
    HAPPY_PATH_RESPONSES (list): a list of happy-path responses.
    ERROR_RESPONSES (list): a list of responses for errors.

"""
from .utils import get_random_choice


HAPPY_PATH_RESPONSES = [
    "Hi! Do you want to play a game of chess?",
    "I've been waiting for someone to play chess against. Shall we start? ",
    "Hello, do you want to play chess?"
]

HAPPY_PATH_RESPONSES_2 = [
    "Great! What side do you want to choose?",
]

HAPPY_PATH_RESPONSES_3 = [
    "That's fine. I didn't want to play with you either."
]


def handle():
    static_choice = get_random_choice(HAPPY_PATH_RESPONSES)
    return static_choice, True


def handle_yes():
    static_choice = get_random_choice(HAPPY_PATH_RESPONSES_2)
    return static_choice, True


def handle_no():
    return get_random_choice(HAPPY_PATH_RESPONSES_3), True
