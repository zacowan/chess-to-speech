"""This module handles intent processing for MOVE_PIECE.
"""
from .utils import get_random_choice
from api.state_manager import set_fulfillment_params, get_game_state, set_game_finished
from api.chess_logic import (
    check_if_check,
    check_if_checkmate,
    get_board_str_with_move,
    get_piece_at,
    check_if_move_legal,
    check_if_turn,
    check_if_move_causes_check,
    get_from_location_from_move_info,
    get_piece_name_at,
    IllegalMoveError,
    MultiplePiecesCanMoveError
)


HAPPY_PATH_RESPONSES = [
    "Okay, moving your {piece_name} to {to_location}.",
    "Great, your {piece_name} will go to {to_location}.",
    "Cool, {piece_name} to {to_location}."
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
        locations = intent_model.parameters["locations"]
        piece_name = intent_model.parameters["pieceName"] or None
        to_location = locations[0]
        from_location = None

        if len(locations) >= 2:
            # We have a from_location and a to_location
            from_location = locations[0]
            to_location = locations[1]
        elif piece_name:
            # We need to figure out the from_location
            move_info = {
                "to_location": to_location,
                "piece_name": piece_name,
            }
            try:
                from_location = get_from_location_from_move_info(
                    board_str, move_info)
            except IllegalMoveError:
                static_choice = get_random_choice(ILLEGAL_MOVE_ERROR_RESPONSES)

                return static_choice, False, board_str
            except MultiplePiecesCanMoveError:
                static_choice = get_random_choice(NEED_MORE_INFO_RESPONSES)

                return static_choice, False, board_str
        else:
            # Not sure which piece to move, return error
            static_choice = get_random_choice(NEED_MORE_INFO_RESPONSES)

            return static_choice, False, board_str

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
            elif check_if_check(updated_board_str):
                static_choice += get_random_choice(CHECK_SUFFIXES)

            # Get the piece name
            actual_piece_name = get_piece_name_at(board_str, from_location)

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

        piece_name = intent_model.parameters["pieceName"] or None
        if piece_name:
            # User should specify a to location
            static_choice = get_random_choice(
                NEED_TO_LOCATION_ERROR_RESPONSES).format(piece_name=piece_name.lower())

        return static_choice, False, board_str
