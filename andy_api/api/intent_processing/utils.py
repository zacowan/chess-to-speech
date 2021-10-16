"""This module provides utilities for processing intents.

Attributes:
    INTENT_NAME_BASE (str): The base of the name for an intent
    RESPONSE_TYPES (Enum): An enum for response types.
    INTENT_MAPPING (dict): Contains a mapping of intent IDs to responses.

"""

import random
from enum import Enum

INTENT_NAME_BASE = "projects/chess-master-andy-mhyo/agent/intents/"

# The name of each type is separated by a space
RESPONSE_TYPES = Enum(
    "RESPONSE_TYPES",
    "HELLO FALLBACK CHOOSE_SIDE MOVE_PIECE_FROM MOVE_PIECE_TO"
)


INTENT_MAPPING = {
    INTENT_NAME_BASE + "2ab3d889-b6eb-494e-b822-9992da79280c": RESPONSE_TYPES.FALLBACK,
    INTENT_NAME_BASE + "fc298129-5845-44dc-a976-b7d6ca2f14c3": RESPONSE_TYPES.HELLO,
    INTENT_NAME_BASE + "6fafe557-d27b-41e7-bef0-204a87036e2c": RESPONSE_TYPES.CHOOSE_SIDE,
    INTENT_NAME_BASE + "3d732581-d539-44cf-8fce-3a9b18dd7e59": RESPONSE_TYPES.MOVE_PIECE_FROM,
    INTENT_NAME_BASE + "3d732581-d539-44cf-8fce-3a9b18dd7e59": RESPONSE_TYPES.MOVE_PIECE_TO,
}


def get_random_choice(choices):
    """Returns a random choice from a list.

    Args:
        choices (dict): the list of choices to choose from.

    Returns:
        str: a random choice from the list, as text.

    """
    return random.choice(choices)
