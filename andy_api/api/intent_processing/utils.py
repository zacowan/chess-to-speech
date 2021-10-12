"""This module provides utilities for processing intents.

Attributes:
    INTENT_NAME_BASE (str): The base of the name for an intent
    RESPONSE_TYPES (Enum): An enum for response types.
    INTENT_MAPPING (dict): Contains a mapping of intent IDs to responses.
    RESPONSE_LIST (dict): Contains all static responses and the base for all
        dynamic responses.
    ERROR_RESPONSE_LIST (dict): Contains all static error responses. For example,
        not including a required parameter.
"""

import random
from enum import Enum

INTENT_NAME_BASE = "projects/chess-master-andy-mhyo/agent/intents/"

RESPONSE_TYPES = Enum(
    "RESPONSE_TYPES",
    "HELLO FALLBACK CHOOSE_SIDE"
)


INTENT_MAPPING = {
    INTENT_NAME_BASE + "2ab3d889-b6eb-494e-b822-9992da79280c": RESPONSE_TYPES.FALLBACK,
    INTENT_NAME_BASE + "fc298129-5845-44dc-a976-b7d6ca2f14c3": RESPONSE_TYPES.HELLO,
    INTENT_NAME_BASE + "6fafe557-d27b-41e7-bef0-204a87036e2c": RESPONSE_TYPES.CHOOSE_SIDE
}


RESPONSE_LIST = {
    RESPONSE_TYPES.HELLO: [
        "Hi! How are you?",
        "Hey, what's up?",
        "Yo, how's it going?"
    ],
    RESPONSE_TYPES.FALLBACK: [
        "I didn't get that. Can you say it again?",
        "I missed what you said. What was that?",
        "Sorry, could you say that again?",
        "Can you say that again?",
        "One more time?",
        "What was that?",
        "Say that one more time?",
        "I'm not sure I understood that."
    ],
    RESPONSE_TYPES.CHOOSE_SIDE: [
        "Great, since you're on {user_side} side, you'll go {user_position}.",
        "Good choice, that means you'll go {user_position}.",
        "Sweet, that means I'll go {andy_position} and you'll go {user_position}.",
        "That leaves me {andy_side}, meaning you'll go {user_position}."
    ]
}

ERROR_RESPONSE_LIST = {
    RESPONSE_TYPES.CHOOSE_SIDE: [
        "Sorry, you can only choose between black or white. Which side do you choose?",
        "Oh, you should choose between black or white. What'll it be?"
    ]
}


def get_random_choice(choices, key):
    """Returns a random choice from the list at dict[key]

    Args:
        choices (dict): should be a dictionary where each key is a list of
            strings.
        key (RESPONSE_TYPES): the key of the list to choose from.

    Returns:
        str: a random choice from the list, as text.

    """
    return random.choice(choices.get(key))
