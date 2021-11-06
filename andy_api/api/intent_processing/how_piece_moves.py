"""
TODO add info about intent
"""

from andy_api.api.intent_processing.move_piece_from import STANDARD_ERROR_RESPONSES
from .utils import get_random_choice
# TODO add api state manager variables for this interaction?

import chess


HOW_KING_MOVES = "Oh the piece at {piece_location} is a King. Kings move one square in any direction, so long as that square is not attacked by an enemy piece. Additionally, kings are able to make a special move, known as castling."

HOW_QUEEN_MOVES = "At {piece_location} lies the Queen. Queens move diagonally, horizontally, or vertically any number of squares. They are unable to jump over pieces."

HOW_ROOKS_MOVE = "There is a Rook on that space. Rooks move horizontally or vertically any number of squares. They are unable to jump over pieces. Rooks move when the king castles."

HOW_BISHOPS_MOVE = "Oh {piece_location}- thats A Bishop! Bishops move diagonally any number of squares. They are unable to jump over pieces."

HOW_KNIGHTS_MOVE =  "{piece_location} holds a Knight. Knights move in an ‘L’ shape’: two squares in a horizontal or vertical direction, then move one square horizontally or vertically. They are the only piece able to jump over other pieces."

HOW_PAWNS_MOVE = "And at {piece_location} we have a pawn. Pawns move vertically forward one square, with the option to move two squares if they have not yet moved. Pawns are the only piece to capture different to how they move. The pawns capture one square diagonally in a forward direction. Pawns are unable to move backward on captures or moves. Upon reaching the other side of the board a pawn promotes into any other piece, except for a king. Additionally, pawns can make a special move named En Passant."

EMPTY_SPACE_RESPONSE = "Hmmmm there doesn't seem to be anything at {piece_location}"

STANDARD_ERROR_RESPONSES = [
    "You want to hear more about the piece at which location?",
    "Wait...what's the location of the piece you want to learn more about?"
]


def get_piece_at(board_str, location):
    board = chess.Board(board_str)
    board_location = chess.parse_square(location.lower())
    return board.piece_at(board_location)

def handle(session_id, intent_data, board_str):
    """TODO add details about method
    """

    if intent_data.all_required_params_present is True:

         # check if space contains piece
        board = chess.Board(board_str)
        piece_location = intent_data.parameters["pieceLocation"]
        piece_location = piece_location.lower()
        piece_num = get_piece_at(board_str,piece_location)
        piece = board.piece_at(piece_num)

        # find specific response depending on piece type
        if(piece == None):
            static_choice = get_random_choice(EMPTY_SPACE_RESPONSE.format(piece_location))
            return static_choice, True
        elif(piece == chess.PAWN):
            static_choice = get_random_choice(HOW_PAWNS_MOVE.format(piece_location))
            return static_choice, True
        elif(piece == chess.KNIGHT):
            static_choice = get_random_choice(HOW_KNIGHTS_MOVE.format(piece_location))
            return static_choice, True
        elif(piece == chess.BISHOP):
            static_choice = get_random_choice(HOW_BISHOPS_MOVE.format(piece_location))
            return static_choice, True
        elif(piece == chess.ROOK):
            static_choice = get_random_choice(HOW_ROOKS_MOVE.format(piece_location))
            return static_choice, True
        elif(piece == chess.QUEEN):
            static_choice = get_random_choice(HOW_QUEEN_MOVES.format(piece_location))
            return static_choice, True
        elif(piece == chess.KING):
            static_choice = get_random_choice(HOW_KING_MOVES.format(piece_location))
            return static_choice, True
        
        else:
            static_choice = get_random_choice(STANDARD_ERROR_RESPONSES)
            return static_choice, False
