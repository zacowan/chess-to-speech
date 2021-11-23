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
    "HELLO FALLBACK CHOOSE_SIDE MOVE_PIECE HOW_PIECE_MOVES BEST_MOVE START_GAME POSSIBLE_ACTIONS ERROR RESTART_GAME"
)

INTENT_MAPPING = {
    INTENT_NAME_BASE + "2ab3d889-b6eb-494e-b822-9992da79280c": RESPONSE_TYPES.FALLBACK,
    INTENT_NAME_BASE + "fc298129-5845-44dc-a976-b7d6ca2f14c3": RESPONSE_TYPES.HELLO,
    INTENT_NAME_BASE + "6fafe557-d27b-41e7-bef0-204a87036e2c": RESPONSE_TYPES.CHOOSE_SIDE,
    INTENT_NAME_BASE + "67bf1b70-c4f3-44e5-976e-960837acff06": RESPONSE_TYPES.MOVE_PIECE,
    INTENT_NAME_BASE + "a18c9f1a-c779-4e99-b72c-20014150ddcf": RESPONSE_TYPES.HOW_PIECE_MOVES,
    INTENT_NAME_BASE + "734e5b0a-80d0-4f3e-b9c3-f9502888dd45": RESPONSE_TYPES.BEST_MOVE,
    INTENT_NAME_BASE + "2b614d03-2366-4878-b22d-86df4003138d": RESPONSE_TYPES.START_GAME,
    INTENT_NAME_BASE + "33ccbac2-0304-4e23-8299-8bc552ef1bba": RESPONSE_TYPES.POSSIBLE_ACTIONS,
    INTENT_NAME_BASE + "a7e3fb42-b1c9-4430-be3f-597a86b552d1": RESPONSE_TYPES.RESTART_GAME
}


def get_random_choice(choices):
    """Returns a random choice from a list.
    Args:
        choices (dict): the list of choices to choose from.
    Returns:
        str: a random choice from the list, as text.
    """
    return random.choice(choices)
