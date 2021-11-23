from api.state_manager import get_board_stack, set_board_stack
from .utils import get_random_choice

HAPPY_PATH_RESPONSES = [
    "I can undo your last move.",
    "Allow me to undo your last move."
]


ERROR_RESPONSES = [
    "Sorry, I'm having trouble undoing your last move.",
    "Sorry, I can't find your last move."
]


def handle(session_id):
    """TODO add details about method
    """
    static_choice = get_random_choice(HAPPY_PATH_RESPONSES)

    # Update board stack and grab board string before user made last move.
    board_stack = get_board_stack(session_id)
    if(board_stack.empty()):
        return get_random_choice(ERROR_RESPONSES)
    updated_board_str = board_stack.pop()
    set_board_stack(session_id, board_stack)

    return static_choice, True, updated_board_str

