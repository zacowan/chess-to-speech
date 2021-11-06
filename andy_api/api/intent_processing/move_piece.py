"""This module handles intent processing for MOVE_PIECE.
"""
import chess

from .utils import get_random_choice
from api.state_manager import set_fulfillment_params


HAPPY_PATH_RESPONSES = [
    "Okay, moving {from_location} to {to_location}.",
    "Great, {from_location} will go to {to_location}."
]

CHECK_ADDITIONS = [
    "That puts me in check!"
]

CHECKMATE_ADDITIONS = [
    "And that puts me in checkmate, you win!"
]

EMPTY_SPACE__ERROR_RESPONSES = [
    "What- you movin a ghost piece or sumtin?",
    "Let me know when you wanna move a real piece..."
]

WRONG_COLOR_ERROR_RESPONSES = [
    "Don't touch my pieces!",
    "You can win without cheating- move your own colored piece!"
]

ILLEGAL_MOVE_ERROR_RESPONSES = [
    "I heard ya, but that move is illegal."
    "I would let ya make that move, but there are rules to this game!"
]

FROM_ERROR_RESPONSES = [
    "Which piece did you want to move?",
    "You wanted to move the piece at which location?"
]

TO_ERROR_RESPONSES = [
    "You wanted to move your piece to where?",
    "Where did you want to move your piece to?"
]

col_num = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7
}

row_num = {
    "8": 0,
    "7": 1,
    "6": 2,
    "5": 3,
    "4": 4,
    "3": 5,
    "2": 6,
    "1": 7
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

    if intent_model.all_required_params_present is True:
        # Get piece locations
        from_location = intent_model.parameters["fromLocation"].lower()
        to_location = intent_model.parameters["toLocation"].lower()
        move_sequence = from_location + to_location

        # Chess logic
        piece_num = locationToNumber(from_location)
        static_choice = get_random_choice(HAPPY_PATH_RESPONSES)
        board = chess.Board(board_str)

        # check if space contains piece
        if board.piece_at(piece_num) == None:
            static_choice = get_random_choice(EMPTY_SPACE__ERROR_RESPONSES)
            return static_choice, False, updated_board_str

        # check that player owns piece
        player_color = board.color_at(piece_num)
        from_color = board.turn
        if player_color != from_color:
            static_choice = get_random_choice(WRONG_COLOR_ERROR_RESPONSES)
            return static_choice, False, updated_board_str

        # Check if the move is legal
        if chess.Move.from_uci(move_sequence) in board.legal_moves:
            # Make the move
            board.push(chess.Move.from_uci(move_sequence))

            # Update the board_str
            updated_board_str = board.board_fen()

            # Get the response
            static_choice = get_random_choice(HAPPY_PATH_RESPONSES)

            # check if user has put andy in check or checkmate
            if board.is_checkmate():
                static_choice += get_random_choice(CHECKMATE_ADDITIONS)
            elif board.is_check():
                static_choice += get_random_choice(CHECK_ADDITIONS)

            # Log the fulfillment params
            set_fulfillment_params(session_id, params={
                "from_location": from_location,
                "to_location": to_location
            })

            return static_choice.format(
                from_location=from_location,
                to_location=to_location
            ), True, updated_board_str
        else:
            # Illegal move
            static_choice = get_random_choice(ILLEGAL_MOVE_ERROR_RESPONSES)

            # Log the fulfillment params
            set_fulfillment_params(session_id, params={
                "from_location": from_location,
                "to_location": to_location
            })

            return static_choice, False, updated_board_str

    elif not intent_model.parameters["fromLocation"]:
        # Missing fromLocation
        static_choice = get_random_choice(FROM_ERROR_RESPONSES)

        return static_choice, False, updated_board_str
    else:
        # Missing toLocation, but we have fromLocation
        static_choice = get_random_choice(TO_ERROR_RESPONSES)

        # Log the fulfillment params
        from_location = intent_model.parameters["fromLocation"].lower()
        set_fulfillment_params(session_id, params={
            "from_location": from_location,
        })

        return static_choice, False, updated_board_str
