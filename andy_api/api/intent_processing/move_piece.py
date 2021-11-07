"""This module handles intent processing for MOVE_PIECE.
"""
import chess

from .utils import get_random_choice
from api.state_manager import set_fulfillment_params, get_game_state


HAPPY_PATH_RESPONSES = [
    "Okay, moving {from_location} to {to_location}.",
    "Great, {from_location} will go to {to_location}."
]

CHECK_ADDITIONS = [
    "That puts me in check!"
]

CHECKMATE_ADDITIONS = [
    "And that puts me in checkmate, you win!"
]

EMPTY_SPACE_ERROR_RESPONSES = [
    "I don't see a piece at {from_location}, Perhaps I misunderstood?",
    "It seems like there is no piece at {from_location}",
    "It seems like there is no piece at {from_location}, Perhaps I misunderstood?",
    "I don't see a piece at {from_location}",
]

WRONG_COLOR_ERROR_RESPONSES = [
    "I see that you attempted to move my piece, keep in mind your pieces are the {player_color} pieces.",
    "The piece at {from_location} is my piece, keep in mind you are playing with the {player_color} pieces."
]

ILLEGAL_MOVE_ERROR_RESPONSES = [
    "That is an illegal move, if you would like to know legal moves for the piece at {from_location}. You Can ask what legal move can I do with my piece at {from_location}.",
    "That is not how that piece moves, if you would like help, You Can ask me for help by saying, Andy can you help me?"
]

FROM_ERROR_RESPONSES = [
    "Which piece did you want to move?",
    "You wanted to move the piece at which location?"
]

TO_ERROR_RESPONSES = [
    "You wanted to move your piece at {from_location} to where?",
    "Where did you want to move your piece at {from_location} to?"
]


def get_piece_at(board_str, location):
    board = chess.Board(board_str)
    board_location = chess.parse_square(location.lower())
    return board.piece_at(board_location)


def check_if_turn(board_str, location):
    board = chess.Board(board_str)
    board_location = chess.parse_square(location.lower())
    return board.turn == board.color_at(board_location)


def check_if_move_legal(board_str, move_sequence):
    board = chess.Board(board_str)
    return chess.Move.from_uci(move_sequence.lower()) in board.legal_moves


def get_board_str_with_move(board_str, move_sequence):
    board = chess.Board(board_str)
    board.push_uci(move_sequence.lower())
    return board.fen()


def check_if_check(board_str):
    board = chess.Board(board_str)
    return board.is_check()


def check_if_checkmate(board_str):
    board = chess.Board(board_str)
    return board.is_checkmate()


def handle(session_id, intent_model, board_str):
    """Handles choosing a response for the MOVE_PIECE intent.
    Args:
        intent_model: the intent model to parse.
    Returns:
        str: the response that should be given, as text.
        boolean: whether or not the intent was handled successfully.
    """
    if intent_model.all_required_params_present is True:
        # Get piece locations
        from_location = intent_model.parameters["fromLocation"]
        to_location = intent_model.parameters["toLocation"]

        # Log the fulfillment params
        set_fulfillment_params(session_id, params={
            "from_location": from_location,
            "to_location": to_location
        })

        # Chess logic
        if not get_piece_at(board_str, from_location):
            # No piece at that location
            static_choice = get_random_choice(EMPTY_SPACE_ERROR_RESPONSES)
            return static_choice.format(from_location=from_location), False, board_str
        elif not check_if_turn(board_str, from_location):
            # Player does not own that piece
            static_choice = get_random_choice(WRONG_COLOR_ERROR_RESPONSES)

            # Get the player's color
            player_color = get_game_state(session_id).get("chosen_side")

            return static_choice.format(player_color=player_color, from_location=from_location), False, board_str

        # Check if the move is legal
        if check_if_move_legal(board_str, from_location + to_location):
            # Update the board_str
            updated_board_str = get_board_str_with_move(
                board_str, from_location + to_location)

            # Get the response
            static_choice = get_random_choice(HAPPY_PATH_RESPONSES)

            # check if user has put andy in check or checkmate
            if check_if_checkmate(updated_board_str):
                static_choice += get_random_choice(CHECKMATE_ADDITIONS)
            elif check_if_check(updated_board_str):
                static_choice += get_random_choice(CHECK_ADDITIONS)

            return static_choice.format(
                from_location=from_location,
                to_location=to_location
            ), True, updated_board_str
        else:
            # Illegal move
            static_choice = get_random_choice(ILLEGAL_MOVE_ERROR_RESPONSES)

            return static_choice.format(from_location=from_location), False, board_str

    elif not intent_model.parameters["fromLocation"]:
        # Missing fromLocation
        static_choice = get_random_choice(FROM_ERROR_RESPONSES)

        return static_choice, False, board_str
    else:
        # Missing toLocation, but we have fromLocation
        static_choice = get_random_choice(TO_ERROR_RESPONSES)

        # Log the fulfillment params
        from_location = intent_model.parameters["fromLocation"]
        set_fulfillment_params(session_id, params={
            "from_location": from_location,
        })

        # Chess logic
        if not get_piece_at(board_str, from_location):
            # No piece at that location
            static_choice = get_random_choice(EMPTY_SPACE_ERROR_RESPONSES)
            return static_choice.format(from_location=from_location), False, board_str
        elif not check_if_turn(board_str, from_location):
            # Player does not own that piece
            static_choice = get_random_choice(WRONG_COLOR_ERROR_RESPONSES)
            # Get the player's color
            player_color = get_game_state(session_id).get("chosen_side")
            return static_choice.format(player_color=player_color, from_location=from_location), False, board_str

        return static_choice.format(from_location=from_location), False, board_str
