import chess
import chess.engine
import os

# This is a relative location to the directory in which you run the script (aka, andy_api/)
STOCKFISH_ENGINE_LOCATION = os.environ.get("STOCKFISH_LOCATION")

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
    best_move = engine.play(board, chess.engine.Limit(time=0.1)).move
    engine.quit()
    return best_move.uci()


def make_move(board_str, move):
    board = chess.Board(board_str)
    board.push(chess.Move.from_uci(move.lower()))
    return board.fen()


def get_piece_name_at(board_str, location):
    board = chess.Board(board_str)
    board_location = chess.parse_square(location)
    piece_symbol = board.piece_at(board_location).symbol()
    return CHESS_PIECE_NAMES.get(piece_symbol.upper(), 'unknown piece')


def check_if_check(board_str):
    board = chess.Board(board_str)
    return board.is_check()


def check_if_checkmate(board_str):
    board = chess.Board(board_str)
    return board.is_checkmate()


def get_current_color_turn(board_str):
    board = chess.Board(board_str)
    return board.turn
