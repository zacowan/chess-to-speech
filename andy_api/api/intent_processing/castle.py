"""This module handles intent processing for MOVE_PIECE.
"""
from .utils import get_random_choice
from api.state_manager import set_fulfillment_params, get_game_state, set_game_finished, get_board_stack, set_board_stack
from api.chess_logic import (
    check_castle,
    check_if_check,
    check_if_checkmate,
    get_board_str_with_move,
    get_piece_at,
    check_if_move_legal,
    check_if_move_causes_check,
    get_castle_locations
)
from api.intent_processing import move_piece


HAPPY_PATH_RESPONSES = [
    "Okay, your king will castle on {castle_side}-side.",
    "Cool, castling your king to {castle_side}-side."
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
    "Oh, it looks like your king isn't there.",
    "Sorry, I don't see your king at {from_location}."
]

MOVE_CAUSES_CHECK_ERROR_RESPONSES = [
    "Actually, castling there would put you into check, which would be against the rules.",
    "Oh, castling there puts your king in danger, so you can't do it."
]

ERROR_RESPONSES = [
    "Sorry, which side did you want to castle on?",
    "Sorry, where did you want to castle to?"
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
        from_location = None
        # can user castle
        if not check_castle(board_str, castle_side, user_side):
            static_choice = get_random_choice(
                move_piece.ILLEGAL_MOVE_ERROR_RESPONSES)
            return static_choice, False, board_str
        else:
            from_location, to_location = get_castle_locations(
                board_str, castle_side, user_side)
        # if we can castle then make move

        # Log the fulfillment params
        set_fulfillment_params(session_id, params={
            "from_location": from_location,
            "to_location": to_location,
            "castle_side": castle_side
        })

        # Chess logic
        if not get_piece_at(board_str, from_location):
            # No piece at that location
            static_choice = get_random_choice(EMPTY_SPACE_ERROR_RESPONSES)
            return static_choice.format(from_location=from_location), False, board_str

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
                    "castle_side": castle_side,
                    "won": True
                })
            elif check_if_check(updated_board_str):
                static_choice += get_random_choice(CHECK_SUFFIXES)

            # Update stack of board strings with last board string before move
            board_stack = get_board_stack(session_id)
            board_stack.append(board_str)
            set_board_stack(session_id, board_stack)

            return static_choice.format(
                to_location=to_location,
                castle_side=castle_side
            ), True, updated_board_str
        else:
            # Illegal move
            static_choice = get_random_choice(
                move_piece.ILLEGAL_MOVE_ERROR_RESPONSES)

            # Check if move results in check
            if check_if_move_causes_check(board_str, from_location + to_location):
                static_choice = get_random_choice(
                    MOVE_CAUSES_CHECK_ERROR_RESPONSES)

            return static_choice, False, board_str
    else:
        # Not sure which piece to move, return error
        static_choice = get_random_choice(ERROR_RESPONSES)
        return static_choice, False, board_str
