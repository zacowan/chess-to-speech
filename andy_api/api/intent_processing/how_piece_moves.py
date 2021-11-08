"""
TODO add info about intent
"""

from .utils import get_random_choice
from api.state_manager import set_fulfillment_params
from api.chess_logic import get_piece_name_at

# TODO: add this functionality:
# Additionally, kings are able to make a special move, known as castling.
HOW_KING_MOVES = [
    "Kings move one square in any direction, so long as that square is not in danger from an enemy piece. They are unable to jump over pieces."
]

HOW_QUEEN_MOVES = [
    "Queens move diagonally, horizontally, or vertically any number of squares. They are unable to jump over pieces."
]

# TODO: add this functionality
# Rooks move when the king castles.
HOW_ROOKS_MOVE = [
    "Rooks move horizontally or vertically any number of squares. They are unable to jump over pieces."
]

HOW_BISHOPS_MOVE = [
    "Bishops move diagonally any number of squares. They are unable to jump over pieces."
]

HOW_KNIGHTS_MOVE = [
    "Knights move in an L shape: two squares in a horizontal or vertical direction, then one additional square horizontally or vertically. They are the only piece able to jump over other pieces."
]


# TODO: add this functionality:
# Upon reaching the other side of the board a pawn promotes into any other piece, except for a king. Additionally, pawns can make a special move named En Passant.
HOW_PAWNS_MOVE = [
    "Pawns move vertically forward one square, or optionally, two squares if they haven't been moved yet. They can attack forward one square diagonally, but they are unable to move backwards."
]

LOCATION_INCLUDED_PREFIXES = [
    "So that's a {piece_name}.",
    "Oh, that's a {piece_name}."
]

PIECE_NAME_MISMATCH_PREFIXES = [
    "Actually, that's a {actual_piece_name}."
]

EMPTY_SPACE_RESPONSE = [
    "Actually, there isn't a piece at {piece_location}."
]

STANDARD_ERROR_RESPONSES = [
    "Sorry, I need to know which piece you are talking about to tell you how it moves.",
    "Sorry, I'm not sure which piece you want to know more about."
]


def get_prefix(board_str, piece_name, piece_location):
    actual_piece_name = get_piece_name_at(board_str, piece_location)
    if piece_name.lower() != actual_piece_name:
        return get_random_choice(PIECE_NAME_MISMATCH_PREFIXES).format(
            actual_piece_name=actual_piece_name,
            spoken_piece_name=piece_name.lower()
        ) + " "
    elif piece_location and actual_piece_name:
        return get_random_choice(LOCATION_INCLUDED_PREFIXES).format(
            piece_name=actual_piece_name
        ) + " "
    else:
        return ""


def handle(session_id, intent_data, board_str):
    piece_location = intent_data.parameters["pieceLocation"] or None
    piece_name = intent_data.parameters["pieceName"] or None

    if piece_location or piece_name:
        if not piece_name:
            piece_name = get_piece_name_at(board_str, piece_location)
            if not piece_name:
                static_choice = get_random_choice(
                    EMPTY_SPACE_RESPONSE)
                return static_choice.format(piece_location=piece_location), False

        piece_name = piece_name.lower()
        prefix = get_prefix(board_str, piece_name, piece_location)

        # Update the fulfillment params
        set_fulfillment_params(session_id, {
            "piece_name": piece_name,
            "piece_location": piece_location
        })

        # find specific response depending on piece type
        if piece_name == "pawn":
            static_choice = get_random_choice(
                HOW_PAWNS_MOVE)
            return prefix + static_choice, True
        elif piece_name == "knight":
            static_choice = get_random_choice(
                HOW_KNIGHTS_MOVE).format(piece_location=piece_location)
            return prefix + static_choice, True
        elif piece_name == "bishop":
            static_choice = get_random_choice(
                HOW_BISHOPS_MOVE).format(piece_location=piece_location)
            return prefix + static_choice, True
        elif piece_name == "rook":
            static_choice = get_random_choice(
                HOW_ROOKS_MOVE).format(piece_location=piece_location)
            return prefix + static_choice, True
        elif piece_name == "queen":
            static_choice = get_random_choice(
                HOW_QUEEN_MOVES).format(piece_location=piece_location)
            return prefix + static_choice, True
        elif piece_name == "king":
            static_choice = get_random_choice(
                HOW_KING_MOVES).format(piece_location=piece_location)
            return prefix + static_choice, True

    else:
        static_choice = get_random_choice(STANDARD_ERROR_RESPONSES)
        return static_choice, False
