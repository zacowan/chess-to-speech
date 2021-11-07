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
    get_piece_name_at
)


HAPPY_PATH_RESPONSES = [
    "Okay, moving your {piece_name} to {to_location}.",
    "Great, your {piece_name} will go to {to_location}."
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

MOVE_CAUSES_CHECK_ERROR_RESPONSES = [
    "Sorry, you can't do that because it would put you into check.",
    "That move will put you into check, so you can't do it."
]

ERROR_RESPONSES = [
    "Sorry, I didn't understand your move. Say it again?",
    "I'm not sure I understand your move, could you tell me again?"
]

TO_ERROR_RESPONSES = [
    "You wanted to move your piece at {from_location} to where?",
    "Where did you want to move your piece at {from_location} to?"
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
        else:
            # We need to figure out the from_location
            move_info = {
                "to_location": to_location,
                "piece_name": piece_name,
            }
            from_location = get_from_location_from_move_info(
                board_str, move_info)
            if not from_location:
                # Not sure which piece to move, return error
                static_choice = get_random_choice(ERROR_RESPONSES)

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
                set_game_finished(session_id)
            elif check_if_check(updated_board_str):
                static_choice += get_random_choice(CHECK_ADDITIONS)

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

            return static_choice.format(from_location=from_location), False, board_str

    else:
        # Not sure which piece to move, return error
        static_choice = get_random_choice(ERROR_RESPONSES)

        return static_choice, False, board_str
    # else:
    #     # Missing toLocation, but we have fromLocation
    #     static_choice = get_random_choice(TO_ERROR_RESPONSES)

    #     # Log the fulfillment params
    #     from_location = intent_model.parameters["fromLocation"]
    #     set_fulfillment_params(session_id, params={
    #         "from_location": from_location,
    #     })

    #     # Chess logic
    #     if not get_piece_at(board_str, from_location):
    #         # No piece at that location
    #         static_choice = get_random_choice(EMPTY_SPACE_ERROR_RESPONSES)
    #         return static_choice.format(from_location=from_location), False, board_str
    #     elif not check_if_turn(board_str, from_location):
    #         # Player does not own that piece
    #         static_choice = get_random_choice(WRONG_COLOR_ERROR_RESPONSES)
    #         # Get the player's color
    #         player_color = get_game_state(session_id).get("chosen_side")
    #         return static_choice.format(player_color=player_color, from_location=from_location), False, board_str

    #     return static_choice.format(from_location=from_location), False, board_str
