"""This module will determine what Andy's move will be.

"""
from .intent_processing.utils import get_random_choice
import chess
import os


HAPPY_PATH_RESPONSES = [
    "I'll move my {piece_name} at {from_location} to {to_location}",
    "Let me move my {piece_name} from {from_location} to {to_location}"
]


def get_engine():
    dirname = os.path.dirname(__file__)
    engine_filename = dirname + "/UCI_engine/stockfish"
    engine = chess.engine.SimpleEngine.popen_uci(
        engine_filename)  # load stockfish as chess engine
    return engine


def get_best_move(board_str):
    engine = get_engine()
    board = chess.Board(board_str)
    bestMove = engine.play(board, chess.engine.Limit(time=0.1)).move
    engine.close()
    return bestMove


def make_move(board_str, move):
    board = chess.Board(board_str)
    board.push(chess.Move.from_uci(move.lower()))
    return board.board_fen()


def determine_andy_move(board_str):
    """Handles determining a text response for Andy's move.

    Args:
        board_str: the state of the board, as text.

    Returns:
        str: the response that should be given, as text.
        str: the updated board_str that should be given.
        dict: the move_info to log.

    """
    static_choice = get_random_choice(HAPPY_PATH_RESPONSES)

    move = get_best_move(board_str)

    from_location = move[0:2]
    to_location = move[2:4]

    updated_board_str = make_move(board_str, move)

    new_board = chess.Board(updated_board_str)
    board_location = chess.parse_square(to_location.lower())
    piece_name = new_board.piece_at(board_location)

    # check if board is check
    move_info = {
        "from": from_location,
        "to": to_location
    }

    if(new_board.is_check()):
        return static_choice.format(
            from_location=from_location,
            to_location=to_location,
            piece_name=piece_name) + ', which puts you in check', updated_board_str, move_info

    if(new_board.is_checkmate):
        return static_choice.format(
            from_location=from_location,
            to_location=to_location,
            piece_name=piece_name) + ", and that's checkmate, I win!", updated_board_str, move_info

    return static_choice.format(
        from_location=from_location,
        to_location=to_location,
        piece_name=piece_name), updated_board_str, move_info
