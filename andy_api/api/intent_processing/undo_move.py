from api.state_manager import set_fulfillment_params, get_board_stack, set_board_stack
from .utils import get_random_choice

HAPPY_PATH_RESPONSES = [
    "Okay, I'll move the pieces back to where they were before.",
    "Sure thing, moving the pieces back to where they were before."
]


ERROR_RESPONSES = [
    "Actually, I can't do that because you haven't made a move yet.",
    "Sorry, I'm unable to do that since you haven't made a move yet."
]


def handle(session_id, board_str):
    """TODO add details about method
    """

    static_choice = get_random_choice(HAPPY_PATH_RESPONSES)

    # Update board stack and grab board string before user made last move.
    board_stack = get_board_stack(session_id)
    if len(board_stack) == 0:
        return get_random_choice(ERROR_RESPONSES), False, board_str
    updated_board_str = board_stack.pop()

    # Log the fulfillment params
    set_fulfillment_params(session_id, params={
        "curr_board_str": board_str,
        "updated_board_str": updated_board_str
    })

    set_board_stack(session_id, board_stack)

    return static_choice, True, updated_board_str
