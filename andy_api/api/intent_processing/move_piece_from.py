"""This module handles intent processing for MOVE_PIECE.

Attributes:
    HAPPY_PATH_RESPONSES (list): a list of happy-path responses.
    ERROR_RESPONSES (list): a list of responses for errors.

"""
import chess

from .utils import get_random_choice
from api.state_manager import set_curr_move_from


HAPPY_PATH_RESPONSES = [
    "Okay, and where would you like to move to?",
    "And where to?"
]

ERROR_RESPONSES = [
    "Sorry, the piece at where?",
    "Sorry, the piece at which location?"
]


def handle(session_id, intent_model, board_str):
    """Handles choosing a response for the MOVE_PIECE intent.

    Args:
        intent_model: the intent model to parse.

    Returns:
        str: the response that should be given, as text.
        boolean: whether or not the intent was handled successfully.

    """
    updated_board_str = board_str

    # TODO: add a check for if a game has started
    # TODO: add a check if player has chosen a side
    if intent_model.all_required_params_present is True:
        from_location = intent_model.parameters["fromLocation"]
        static_choice = get_random_choice(HAPPY_PATH_RESPONSES)

        board = chess.Board(board_str)

        # check if space contains piece
        if(board.piece_at(from_location) == None):
            return "What are you trying to move- there's nothing there?", False, updated_board_str

        # check that player owns piece
        player_color = board.color_at(from_location)
        from_color = board.turn()
        if(player_color != from_color):
            return "Don't touch my piece!", False, updated_board_str

        # Update game state
        set_curr_move_from(session_id, from_location)

        return static_choice, True, updated_board_str
    else:
        static_choice = get_random_choice(ERROR_RESPONSES)

        return static_choice, False, updated_board_str
