"""This module handles intent processing for MOVE_PIECE.

Attributes:
    HAPPY_PATH_RESPONSES (list): a list of happy-path responses.
    ERROR_RESPONSES (list): a list of responses for errors.

"""
from .utils import get_random_choice
import chess


HAPPY_PATH_RESPONSES = [
    "Okay, moving {from_location} to {to_location}.",
    "Great, {from_location} will go to {to_location}."
]

ERROR_RESPONSES = [
    "Sorry, you want to move to where?",
    "Sorry, you want to move from {from_location} to where?"
]

ILLEGAL_MOVE_RESPONSES = [
    "I heard ya, but that move is illegal."
    "I would let ya make that move, but there are rules to this game!"
]


def handle(intent_model, board_str):
    """Handles choosing a response for the MOVE_PIECE intent.

    Args:
        intent_model: the intent model to parse.
        board_str: FEN representation of board from client

    Returns:
        str: the response that should be given, as text.
        boolean: whether or not the intent was handled successfully.

    """
    # TODO: add a check for if a game has started
    # TODO: add a check if player has chosen a side
    if intent_model.all_required_params_present is True:
        from_location = intent_model.output_contexts[0].parameters["fromLocation"]
        to_location = intent_model.parameters["toLocation"]

        # Use string representing latest board to create new chess board
        # This board will be used to check if move is valid and make move if valid
        board = chess.Board(board_str)

        # check if move is valid
        if(chess.Move.from_uci(from_location+to_location) in board.legal_moves):
            # Make the move
            board.push(chess.Move.from_uci(from_location+to_location))

            # TODO: See if player is in check or checkmate after move

            static_choice = get_random_choice(HAPPY_PATH_RESPONSES)

            # Return a happy path response
            return static_choice.format(from_location=from_location, to_location=to_location), True, board.board_fen()
        else:  # Player is attempting an illegal move
            static_choice = get_random_choice(ILLEGAL_MOVE_RESPONSES)
            # Return an illegal move response
            return static_choice, False, board_str
    else:
        static_choice = get_random_choice(ERROR_RESPONSES)
        from_location = intent_model.output_contexts.parameters["fromLocation"]

        return static_choice.format(from_location=from_location), False, board_str
