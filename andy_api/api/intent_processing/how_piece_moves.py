"""
TODO add info about intent
"""

from .utils import get_random_choice
from api.state_manager import set_fulfillment_params
from api.chess_logic import get_piece_name_at

import chess


HOW_KING_MOVES = [
    "Kings move one square in any direction, so long as that square is not attacked by an enemy piece. Additionally, kings are able to make a special move, known as castling."]

HOW_QUEEN_MOVES = [
    "Queens move diagonally, horizontally, or vertically any number of squares. They are unable to jump over pieces."]

HOW_ROOKS_MOVE = [
    "Rooks move horizontally or vertically any number of squares. They are unable to jump over pieces. Rooks move when the king castles."]

HOW_BISHOPS_MOVE = [
    "Bishops move diagonally any number of squares. They are unable to jump over pieces."]

HOW_KNIGHTS_MOVE = ["Knights move in an L shape: two squares in a horizontal or vertical direction, then move one square horizontally or vertically. They are the only piece able to jump over other pieces."]


# TODO: add this functionality:
# Upon reaching the other side of the board a pawn promotes into any other piece, except for a king. Additionally, pawns can make a special move named En Passant.
HOW_PAWNS_MOVE = ["Pawns move vertically forward one square, with the option to move two squares if they have not yet moved. Pawns are the only piece to capture different to how they move. The pawns capture one square diagonally in a forward direction. Pawns are unable to move backward on captures or moves."]

EMPTY_SPACE_RESPONSE = [
    "Hmmmm, there doesn't seem to be anything at {piece_location}."]

STANDARD_ERROR_RESPONSES = [
    "Sorry, I'm not sure which piece you are talking about.",
    "I'm not sure I can provide any information about that."
]


def get_piece_at(board_str, location):
    board = chess.Board(board_str)
    board_location = chess.parse_square(location.lower())
    return board.piece_at(board_location)


def handle(session_id, intent_data, board_str):
    piece_location = intent_data.parameters["pieceLocation"] or None
    piece_name = intent_data.parameters["pieceName"] or None

    suffix = ""

    if piece_location or piece_name:
        if not piece_name:
            piece_name = get_piece_name_at(board_str, piece_location)
            if not piece_name:
                static_choice = get_random_choice(
                    EMPTY_SPACE_RESPONSE)
                return static_choice.format(piece_location=piece_location), False
        elif piece_location:
            actual_piece_name = get_piece_name_at(board_str, piece_location)
            if piece_name.lower() != actual_piece_name and actual_piece_name:
                suffix = f"That's not a {piece_name.lower()}, that's a {actual_piece_name}. "
                piece_name = actual_piece_name
            elif not actual_piece_name:
                static_choice = get_random_choice(
                    EMPTY_SPACE_RESPONSE)
                return static_choice.format(piece_location=piece_location), False

        piece_name = piece_name.lower()

        # Update the fulfillment params
        set_fulfillment_params(session_id, {
            "piece_name": piece_name,
            "piece_location": piece_location
        })

        # find specific response depending on piece type
        if(piece_name == "pawn"):
            static_choice = get_random_choice(
                HOW_PAWNS_MOVE)
            return suffix + static_choice, True
        elif(piece_name == "knight"):
            static_choice = get_random_choice(
                HOW_KNIGHTS_MOVE).format(piece_location=piece_location)
            return suffix + static_choice, True
        elif(piece_name == "bishop"):
            static_choice = get_random_choice(
                HOW_BISHOPS_MOVE).format(piece_location=piece_location)
            return suffix + static_choice, True
        elif(piece_name == "rook"):
            static_choice = get_random_choice(
                HOW_ROOKS_MOVE).format(piece_location=piece_location)
            return suffix + static_choice, True
        elif(piece_name == "queen"):
            static_choice = get_random_choice(
                HOW_QUEEN_MOVES).format(piece_location=piece_location)
            return suffix + static_choice, True
        elif(piece_name == "king"):
            static_choice = get_random_choice(
                HOW_KING_MOVES).format(piece_location=piece_location)
            return suffix + static_choice, True

    else:
        static_choice = get_random_choice(STANDARD_ERROR_RESPONSES)
        return static_choice, False
