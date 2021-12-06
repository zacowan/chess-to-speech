from typing import Tuple, cast
import chess
import chess.engine
import os
import random

from api.state_manager import get_game_state

# This is a relative location to the directory in which you run the script (aka, andy_api/)
STOCKFISH_ENGINE_LOCATION = os.environ.get("STOCKFISH_LOCATION")

# Time limit for calculating best move, in seconds
BEST_MOVE_ALGORITHM_TIME_LIMIT = 0.2

if not STOCKFISH_ENGINE_LOCATION:
    raise Exception("You need to specify a location for the stockfish engine.")

CHESS_PIECE_NAMES = {
    'P': 'pawn',
    'R': 'rook',
    'N': 'knight',
    'B': 'bishop',
    'Q': 'queen',
    'K': 'king'
}


def get_engine():
    return chess.engine.SimpleEngine.popen_uci(STOCKFISH_ENGINE_LOCATION)


def get_best_move(board_str):
    engine = get_engine()
    board = chess.Board(board_str)
    best_move = engine.play(board, chess.engine.Limit(
        time=BEST_MOVE_ALGORITHM_TIME_LIMIT)).move
    engine.quit()
    return best_move.uci()


def get_random_move(board_str):
    board = chess.Board(board_str)
    legal_moves = list(board.legal_moves)
    move = random.choice(legal_moves)
    return move.uci()


def get_board_str_with_move(board_str, move_sequence):
    board = chess.Board(board_str)
    board.push_uci(move_sequence.lower())
    return board.fen()


def get_piece_name_at(board_str, location):
    if location:
        board = chess.Board(board_str)
        board_location = chess.parse_square(location.lower())
        piece = board.piece_at(board_location)
        if piece:
            return CHESS_PIECE_NAMES.get(piece.symbol().upper(), None)
        else:
            return None
    else:
        return None


def check_if_check(board_str):
    board = chess.Board(board_str)
    return board.is_check()


def check_if_checkmate(board_str):
    board = chess.Board(board_str)
    return board.is_checkmate()


def get_current_color_turn(board_str):
    board = chess.Board(board_str)
    return board.turn


def get_piece_at(board_str, location):
    board = chess.Board(board_str)
    board_location = chess.parse_square(location.lower())
    return board.piece_at(board_location)


def check_if_owns_location(board_str, location):
    board = chess.Board(board_str)
    board_location = chess.parse_square(location.lower())
    return board.turn == board.color_at(board_location)


def check_if_move_legal(board_str, move_sequence):
    board = chess.Board(board_str)
    try:
        return chess.Move.from_uci(move_sequence.lower()) in board.legal_moves
    except ValueError:
        # Throws if locations are the same (for example, h1h1)
        return False


def check_if_move_causes_check(board_str, move_sequence):
    board = chess.Board(board_str)
    try:
        move_to_make = chess.Move.from_uci(move_sequence.lower())
    except ValueError:
        # Throws if locations are the same (for example, h1h1)
        return False
    if move_to_make in board.pseudo_legal_moves:
        return True
    else:
        return False


class IllegalMoveError(Exception):
    pass


class MultiplePiecesCanMoveError(Exception):
    pass


def get_castle_locations(board_str, castle_side, user_side) -> Tuple[str, str]:
    """Returns from_location, to_location"""
    castle_side = check_castle(board_str, castle_side, user_side)
    if castle_side == "king" and user_side == "white":
        return 'E1', 'G1'
    elif castle_side == "king" and user_side == "black":
        return 'E8', 'G8'
    elif castle_side == "queen" and user_side == "white":
        return 'E1', 'C1'
    else:
        return 'E8', 'C8'


def check_castle(board_str, castle_side, user_side):
    board = chess.Board(board_str)
    castle_side = castle_side.lower()
    if(user_side == "white"):
        user_side = chess.WHITE
        if(castle_side == "left"):
            castle_side = "queen"
        elif(castle_side == "right"):
            castle_side = "king"
    if(user_side == "black"):
        user_side = chess.BLACK
        if(castle_side == "left"):
            castle_side = "king"
        elif(castle_side == "right"):
            castle_side = "queen"
    if board.has_castling_rights(user_side):
        if ((castle_side == "king" and board.has_kingside_castling_rights(user_side)) or
                (castle_side == "queen" and board.has_queenside_castling_rights(user_side))):
            return castle_side
    else:
        return None


def get_from_location_from_move_info(board_str, move_info):
    board = chess.Board(board_str)

    to_location = move_info.get("to_location").lower()
    piece_name = move_info.get("piece_name").lower()

    # Get a list of all possible from locations based on to_location
    potential_from_loc = []
    for loc in chess.SQUARE_NAMES:
        p = board.piece_at(chess.parse_square(loc))
        if p and CHESS_PIECE_NAMES.get(p.symbol().upper()) == piece_name:
            potential_from_loc.append(loc)

    if len(potential_from_loc) == 1:
        return potential_from_loc[0]
    elif len(potential_from_loc) == 0:
        raise IllegalMoveError()

    actual_from_loc = []
    for mv in board.pseudo_legal_moves:
        from_loc = chess.square_name(mv.from_square)
        to_loc = chess.square_name(mv.to_square)
        if from_loc in potential_from_loc and to_loc == to_location:
            actual_from_loc.append(from_loc)

    if len(actual_from_loc) == 1:
        return actual_from_loc[0]
    elif len(actual_from_loc) > 1:
        raise MultiplePiecesCanMoveError()
    else:
        raise IllegalMoveError()
