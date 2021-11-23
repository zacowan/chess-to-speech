import chess
import chess.engine
import os

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


def get_board_str_with_move(board_str, move_sequence):
    board = chess.Board(board_str)
    board.push_uci(move_sequence.lower())
    return board.fen()

def get_new_board():
    board = chess.Board()
    board_str = board.fen()
    return board_str


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
        return False


def check_if_move_causes_check(board_str, move_sequence):
    board = chess.Board(board_str)
    move_to_make = chess.Move.from_uci(move_sequence.lower())
    if move_to_make in board.pseudo_legal_moves:
        return True
    else:
        return False


class IllegalMoveError(Exception):
    pass


class MultiplePiecesCanMoveError(Exception):
    pass


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
