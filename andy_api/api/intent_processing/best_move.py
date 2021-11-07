"""
TODO add info about intent
"""

from utils import get_random_choice
# TODO add api state manager variables for this interaction?

import chess
import chess.engine

import os


HAPPY_PATH_RESPONSES = [
    "Lemme give ya a hand... Move {from_location} to {to_location}.",
    "Okay! I know I'm pretty good, so here's a tip- move {from_location} to {to_location}."
]


def get_engine():
    dirname = os.path.dirname(__file__)
    engine_filename = dirname + "/../UCI_engine/stockfish"
    engine = chess.engine.SimpleEngine.popen_uci(engine_filename) #load stockfish as chess engine
    return engine

def get_best_move(board_str):
    engine = get_engine()
    board = chess.Board(board_str)
    bestMove = engine.play(board, chess.engine.Limit(time=0.1)).move
    engine.close()
    return bestMove

def handle(session_id, intent_model, board_str):
    """TODO add details about method
    """
    if intent_model.all_required_params_present is True:
        static_choice = get_random_choice(HAPPY_PATH_RESPONSES)
        best_move = get_best_move(board_str).uci()

        from_location = best_move[0:2]
        to_location = best_move[2:4]

        return static_choice.format(
            from_location = from_location,
            to_location = to_location
        ), True

        # TODO add error messages/check for errors from player?

