"""This module processes intents and determines a text response.

Attributes:
    STATIC_RESPONSES (dict): a dictionary of lists for static response types.

Example Intent Model:
    {
        query_text: "I\'ll take white side."
        parameters {
            fields {
                key: "BoardSide"
                value {
                    string_value: "white"
                }
            }
        }
        all_required_params_present: true
        fulfillment_text: "Great, you\'ll play white side then!"
        fulfillment_messages {
            text {
                text: "Great, you\'ll play white side then!"
            }
        }
        intent {
            name: "projects/chess-master-andy-mhyo/agent/intents/6fafe557-d27b-41e7-bef0-204a87036e2c"
            display_name: "Choose Side Intent"
        }
        intent_detection_confidence: 1.0
        language_code: "en"
    }

"""
from .utils import INTENT_MAPPING, RESPONSE_TYPES, get_random_choice
from . import choose_side, move_piece_from, move_piece_to


STATIC_RESPONSES = {
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
    ]
}


def fulfill_intent(intent_data, board_str):
    """Fulfills an intent, performing any actions and generating a response.

    Args:
        intent_data (dict): the intent query response generated by Dialogflow.
        board_str (str): the FEN string representation of the board.

    Returns:
        str: the response that should be given, as text.
        dict: the internal name of the intent and the success of its
            fulfillment.

    """
    if intent_data is None:
        response_choice = get_random_choice(
            STATIC_RESPONSES.get(RESPONSE_TYPES.FALLBACK))
        return response_choice, {
            'intent_name': RESPONSE_TYPES.FALLBACK.name,
            'success': False
        }, board_str

    # Determine the response type from the intent
    response_type = INTENT_MAPPING.get(
        intent_data.intent.name, RESPONSE_TYPES.FALLBACK)
    response_choice = "No response."
    success = False

    updated_board_str = board_str

    # Handle more complex responses
    if response_type == RESPONSE_TYPES.CHOOSE_SIDE:
        response_choice, success = choose_side.handle(intent_data)
    elif response_type == RESPONSE_TYPES.MOVE_PIECE_FROM:
        response_choice, success, updated_board_str = move_piece_from.handle(
            intent_data, board_str)
    elif response_type == RESPONSE_TYPES.MOVE_PIECE_TO:
        response_choice, success, updated_board_str = move_piece_to.handle(
            intent_data, board_str)
    else:
        # TODO: double check this
        # Catch for all static responses
        response_choice = get_random_choice(
            STATIC_RESPONSES.get(response_type))
        success = True

    # Return the determined response
    return response_choice, {
        'intent_name': response_type.name,
        'success': success
    }, updated_board_str
