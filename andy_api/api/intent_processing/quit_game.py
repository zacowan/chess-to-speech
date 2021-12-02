"""
This module handles intent processing for QUIT_GAME and its followup intents.
"""
from .utils import get_random_choice
from api.state_manager import set_game_finished, set_fulfillment_params

PROMPT_RESPONSES = [
    "It sounds like you're all done - would you like to quit?",
    "I hear that you're all finished, is that right?"
]

YES_RESPONSES = [
    "Okay, thanks for playing with me!",
    "Alright, good game! I hope we can play again soon."
]

NO_RESPONSES = [
    "Okay, let's continue then.",
    "Alright, let's keep playing then."
]


def handle():
    return get_random_choice(PROMPT_RESPONSES), True


def handle_yes(session_id):
    set_game_finished(session_id)
    # Log the fulfillment params with a defeat
    set_fulfillment_params(session_id, params={
        "won": False
    })

    return get_random_choice(YES_RESPONSES), True


def handle_no():
    return get_random_choice(NO_RESPONSES), True
