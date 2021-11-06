"""This module handles intent processing for MOVE_PIECE.
Attributes:
    HAPPY_PATH_RESPONSES (list): a list of happy-path responses.
    ERROR_RESPONSES (list): a list of responses for errors.
"""
from os import stat
import chess

from .utils import get_random_choice
from api.state_manager import set_curr_move_from, set_fulfillment_params


HAPPY_PATH_RESPONSES = [
    "Okay, and where would you like to move to?",
    "And where to?"
]

EMPTY_SPACE_RESPONSE = [
    "What- you movin a ghost piece or sumtin?",
    "Let me know when you wanna move a real piece..."
]

WRONG_COLOR_RESPONSE = [
    "Don't touch my pieces!",
    "You can win without cheating- move your own colored piece!"
]

STANDARD_ERROR_RESPONSES = [
    "Sorry, the piece at where?",
    "Sorry, the piece at which location?"
]


col_num = {
    "a":0,
    "b":1,
    "c":2,
    "d":3,
    "e":4,
    "f":5,
    "g":6,
    "h":7
}

row_num = {
    "8":0,
    "7":1,
    "6":2,
    "5":3,
    "4":4,
    "3":5,
    "2":6,
    "1":7
}


# (row * 8) + col = piece_num
def locationToNumber(location):
    letter = location[0:1]
    number = location[1:2]
    col = col_num[letter]
    row = row_num[number]
    piece_num = (row*8) + col
    return piece_num


def handle(session_id, intent_model, board_str):
    """Handles choosing a response for the MOVE_PIECE intent.
    Args:
        intent_model: the intent model to parse.
    Returns:
        str: the response that should be given, as text.
        boolean: whether or not the intent was handled successfully.
    """
    updated_board_str = board_str

    # TODO: add a check for if a game has started
    # TODO: add a check if player has chosen a side
    if intent_model.all_required_params_present is True:
        from_location = intent_model.parameters["fromLocation"].lower()
        piece_num = locationToNumber(from_location)
        static_choice = get_random_choice(HAPPY_PATH_RESPONSES)

        board = chess.Board(board_str)

        # check if space contains piece
        if(board.piece_at(piece_num) == None):
            static_choice = get_random_choice(EMPTY_SPACE_RESPONSE)
            return static_choice, False, updated_board_str

        # check that player owns piece
        player_color = board.color_at(piece_num)
        from_color = board.turn()
        if(player_color != from_color):
            static_choice = get_random_choice(WRONG_COLOR_RESPONSE)
            return static_choice, False, updated_board_str

        # Update game state
        set_curr_move_from(session_id, from_location)
        # Log the fulfillment params
        set_fulfillment_params(session_id, params={
            "from_location": from_location
        })

        return static_choice, True, updated_board_str
    else:
        static_choice = get_random_choice(STANDARD_ERROR_RESPONSES)

        return static_choice, False, updated_board_str
