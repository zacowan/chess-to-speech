"""This module fulfills an intent in the event of an internal error.

Attributes:
    RESPONSES (list): a list of error responses.

"""
from .utils import get_random_choice, RESPONSE_TYPES

RESPONSES = [
    "Sorry, my brain just stopped working. Could you say that again?",
    "Sorry, I'm a little slow today, could you tell me that again?",
    "Sorry, I'm having some trouble with things. Could you try that again?"
]


def get_error_fulfillment():
    """Handles choosing a response for an error.

    Returns:
        str: the response that should be given, as text.
        dict: the error intent and the success of the intent (always false)

    """
    static_choice = get_random_choice(RESPONSES)

    return static_choice, {
        'intent_name': RESPONSE_TYPES.ERROR.name,
        'success': False
    }
