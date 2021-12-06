"""This module handles intent processing for MOVE_PIECE.
"""
from .utils import get_random_choice
import chess
import chess.engine
from api.state_manager import set_fulfillment_params, get_game_state, set_game_finished, get_board_stack, set_board_stack
from api.chess_logic import (
    check_castle,
    check_if_check,
    check_if_checkmate,
    get_board_str_with_move,
    get_piece_at,
    check_if_move_legal,
    check_if_owns_location,
    check_if_move_causes_check,
    get_piece_name_at,
)


HAPPY_PATH_RESPONSES = [
    "Okay, castling {castle_side}.",
    "Great, your {piece_name} will go to {to_location}.",
    "Cool, castling to the {castle_side}."
]

CHECK_SUFFIXES = [
    "That puts me in check!",
    "And that puts me in check!"
]

CHECKMATE_SUFFIXES = [
    "And that puts me in checkmate, you win!",
    "You've checkmated me, you win!"
]

EMPTY_SPACE_ERROR_RESPONSES = [
    "Oh, it looks like there isn't a piece there.",
    "Sorry, I don't see a piece at {from_location}."
]

WRONG_COLOR_ERROR_RESPONSES = [
    "That piece actually belongs to me, so I'm afraid you can't move it.",
    "Oh, that's one of my pieces, so you can't move it."
]

ILLEGAL_MOVE_ERROR_RESPONSES = [
    "Actually, that move would be against the rules, so you can't do it.",
    "Oh, that's an illegal move. Could you give me a different one?"
]

MOVE_CAUSES_CHECK_ERROR_RESPONSES = [
    "Actually, that move would put you into check, which would be against the rules.",
    "Oh, that move puts your king in danger, so you can't do it."
]

ERROR_RESPONSES = [
    "Sorry, I didn't understand your move. Could you say it again?",
    "I'm not sure I get your move, could you tell me again?"
]

NEED_MORE_INFO_RESPONSES = [
    "Sorry, I'm not sure which piece you are trying to move. Can you give me more info?",
    "Sorry, I need a little bit more information about your move. Could you give me more details?"
]

NEED_TO_LOCATION_ERROR_RESPONSES = [
    "Sorry, where did you want to move your {piece_name} to?",
    "I hear that you want to move your {piece_name}, but where to?"
]


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
        castle_side = intent_model.parameters["CastleSide"]
        user_side = get_game_state(session_id)["chosen_side"]
        to_location = None
        # can user castle
        if check_castle(board_str, castle_side, user_side) == False:
            static_choice = get_random_choice(ILLEGAL_MOVE_ERROR_RESPONSES)
            return static_choice, False, board_str
        elif check_castle(board_str, castle_side, user_side) == "king":
            from_location = chess.Board.king(user_side)
            if user_side == "white":
                to_location == chess.parse_square("H1")
            elif user_side == "black":
                to_location == chess.parse_square("H8")
        elif check_castle(board_str, castle_side, user_side) == "queen":
            from_location = chess.Board.king(user_side)
            if user_side == "white":
                to_location == chess.parse_square("A1")
            elif user_side == "black":
                to_location == chess.parse_square("A8")
        # if we can castle then make move

        
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
        elif not check_if_owns_location(board_str, from_location):
            # Player does not own that piece
            static_choice = get_random_choice(WRONG_COLOR_ERROR_RESPONSES)

            return static_choice, False, board_str

        # Check if the move is legal
        if check_if_move_legal(board_str, from_location + to_location):

            # Update the board_str
            updated_board_str = get_board_str_with_move(
                board_str, from_location + to_location)

            # Get the response
            static_choice = get_random_choice(HAPPY_PATH_RESPONSES)

            # check if user has put andy in check or checkmate
            if check_if_checkmate(updated_board_str):
                static_choice += get_random_choice(CHECKMATE_SUFFIXES)
                set_game_finished(session_id)
                # Log the fulfillment params with a victory
                set_fulfillment_params(session_id, params={
                    "from_location": from_location,
                    "to_location": to_location,
                    "won": True
                })
            elif check_if_check(updated_board_str):
                static_choice += get_random_choice(CHECK_SUFFIXES)

            # Get the piece name
            actual_piece_name = get_piece_name_at(board_str, from_location)

            # Update stack of board strings with last board string before move
            board_stack = get_board_stack(session_id)
            board_stack.append(board_str)
            set_board_stack(session_id, board_stack)

            return static_choice.format(
                piece_name=actual_piece_name,
                to_location=to_location
            ), True, updated_board_str
        else:
            # Illegal move
            static_choice = get_random_choice(ILLEGAL_MOVE_ERROR_RESPONSES)

            # Check if move results in check
            if check_if_move_causes_check(board_str, from_location + to_location):
                static_choice = get_random_choice(
                    MOVE_CAUSES_CHECK_ERROR_RESPONSES)

            return static_choice, False, board_str
    else:
        # Not sure which piece to move, return error
        static_choice = get_random_choice(ERROR_RESPONSES)
        return static_choice, False, board_str
