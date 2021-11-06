"""This module handles intent processing for MOVE_PIECE.

Attributes:
    HAPPY_PATH_RESPONSES (list): a list of happy-path responses.
    ERROR_RESPONSES (list): a list of responses for errors.

"""
from .utils import get_random_choice
from api.state_manager import set_curr_move_from, get_game_state, set_fulfillment_params
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


def handle(session_id, intent_model, board_str):
    """Handles choosing a response for the MOVE_PIECE intent.

    Args:
        intent_model: the intent model to parse.
        board_str: FEN representation of board from client

    Returns:
        str: the response that should be given, as text.
        boolean: whether or not the intent was handled successfully.

    """
    from_location = get_game_state(session_id)["curr_move_from"]
    if intent_model.all_required_params_present is True:
        to_location = intent_model.parameters["toLocation"]
        move_sequence = from_location+to_location
        move_sequence = move_sequence.lower()

        # Use string representing latest board to create new chess board
        # This board will be used to check if move is valid and make move if valid
        board = chess.Board(board_str)

        # check if move is valid
        if(chess.Move.from_uci(move_sequence) in board.legal_moves):
            # Make the move
            board.push(chess.Move.from_uci(move_sequence))

            # TODO: See if player is in check or checkmate after move

            static_choice = get_random_choice(HAPPY_PATH_RESPONSES)

            # Update game state
            set_curr_move_from(session_id, None)
            # Log the fulfillment params
            set_fulfillment_params(session_id, params={
                "from_location": from_location,
                "to_location": to_location
            })

            # check if user has put andy in check or checkmate
            if(board.is_check()):
                return static_choice.format(
                    from_location=from_location,
                    to_location=to_location) + "... How did you put me in check?!", True, board.board_fen()
            if(board.is_checkmate):
                return static_choice.format(
                    from_location=from_location,
                    to_location=to_location) + "... You beat me - unbelievable!", True, board.board_fen()

            # Return a happy path response
            return static_choice.format(from_location=from_location, to_location=to_location), True, board.board_fen()
        else:  # Player is attempting an illegal move
            static_choice = get_random_choice(ILLEGAL_MOVE_RESPONSES)
            # Update game state
            set_curr_move_from(session_id, None)
            # Log the fulfillment params
            set_fulfillment_params(session_id, params={
                "from_location": from_location,
                "to_location": to_location
            })
            # Return an illegal move response
            return static_choice, False, board_str
    else:
        static_choice = get_random_choice(ERROR_RESPONSES)
        # Log the fulfillment params
        set_fulfillment_params(session_id, params={
            "from_location": from_location
        })

        return static_choice.format(from_location=from_location), False, board_str
