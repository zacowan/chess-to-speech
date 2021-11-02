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

ERROR_RESPONSES = [
    "I'm sorry, can you repeat that?",
    "Huh?"
]


def handle(intent_model):
    """Handles choosing a response for the CHOOSE_SIDE intent.

    Args:
        intent_model: the intent model to parse.

    Returns:
        str: the response that should be given, as text.

    """

    if intent_model.all_required_params_present is True:
        static_choice = get_random_choice(HAPPY_PATH_RESPONSES)
        startGame = intent_model.parameters["startGame"]

        startResponse = "yes"

        start_game = startResponse

        if startGame == "yes":
            return static_choice.format(start_game)
        else:
            return get_random_choice(ERROR_RESPONSES)
