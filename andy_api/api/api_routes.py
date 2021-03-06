"""This module contains all of the routes accessible to the client.

Attributes:
    bp: The blueprint that the __init__.py will use to handle routing.

"""
import traceback
from api.state_manager import get_game_state, set_curr_log_id, get_fulfillment_params, set_fulfillment_params
from datetime import datetime
from threading import Thread
from flask import (
    Blueprint, request, jsonify
)

from . import speech_text_processing, dialogflow_andy, determine_andy_move
from .intent_processing import intent_processing
from .logging import (
    log_andy_response,
    log_error,
    log_user_request,
    log_andy_move,
    log_help_response,
    ERROR_TYPES
)
from .api_route_helpers import get_response_error_return, get_static_error_audio, get_help_response

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route("/get-help-audio-response", methods=["GET"])
def get_help_audio_response():
    """Route for getting help when a user might be confused.

    Likely called in the event of hitting FALLBACK too many times, or not
    talking for awhile.

    Query Params:
        session_id: the unique session ID to use with Andy.
        help_type: one of "FALLBACK" or "TIMEOUT"

    Returns:
        An HTTP response, with the data field containing the raw bytes of the
        audio file. The data field will only be present if the status code of
        the response is 200.

    """
    if request.method == "GET":
        received_at = datetime.now()
        session_id = request.args.get('session_id')
        help_type = request.args.get('help_type')

        # Make sure query params are present
        if not session_id or not help_type:
            raise Exception(
                "get-help-audio-response: missing session_id or help_type")

        # Make sure help_type is one of the expected values
        if help_type not in ["FALLBACK", "TIMEOUT"]:
            raise Exception(
                "get-help-audio-response: help_type is not 'FALLBACK' or 'TIMEOUT'")

        # Get the text response
        text_response = get_help_response(help_type)

        # Get the audio response
        try:
            response_audio = speech_text_processing.generate_audio_response(
                text_response)
        except Exception:
            err_msg = f"Error with text-to-speech: {traceback.format_exc()}"
            log_error(session_id, ERROR_TYPES.TTS, err_msg)
            # Get the error response
            err_response = get_static_error_audio()
            # Log the request
            response_at = datetime.now()
            Thread(target=log_help_response(
                session_id,
                data={
                    "help_type": help_type,
                    "text": text_response,
                    "audio_data": err_response,
                    "received_at": received_at,
                    "response_at": response_at
                }
            )).start()
            # Return the error response
            return err_response

        # Log the request
        response_at = datetime.now()
        Thread(target=log_help_response(
            session_id,
            data={
                "help_type": help_type,
                "text": text_response,
                "audio_data": response_audio,
                "received_at": received_at,
                "response_at": response_at
            }
        )).start()

        # Return
        return response_audio


@bp.route("/get-audio-response", methods=["POST"])
def get_audio_response():
    """Route for getting audio data from text.

    Query Params:
        session_id: the unique session ID to use with Andy.

    Body:
        Text that should be converted into audio.

    Returns:
        An HTTP response, with the data field containing the raw bytes of the
        audio file. The data field will only be present if the status code of
        the response is 200.

    """
    # pylint: disable=broad-except
    if request.method == "POST":
        received_at = datetime.now()
        session_id = request.args.get('session_id')

        # Make sure query params are present
        if not session_id:
            raise Exception("get-audio-response: missing session_id")

        # Convert response to audio
        try:
            response_audio = speech_text_processing.generate_audio_response(
                request.data)
        except Exception:
            err_msg = f"Error with text-to-speech: {traceback.format_exc()}"
            log_error(session_id, ERROR_TYPES.TTS, err_msg)
            # Get the error response
            err_response = get_static_error_audio()
            # Log the request
            response_at = datetime.now()
            Thread(target=log_andy_response(
                session_id,
                data={
                    "text": request.data.decode("utf-8"),
                    "audio_data": err_response,
                    "received_at": received_at,
                    "response_at": response_at
                }
            )).start()
            # Return the error response
            return err_response

        # Log the request
        response_at = datetime.now()
        Thread(target=log_andy_response(
            session_id,
            data={
                "text": request.data.decode("utf-8"),
                "audio_data": response_audio,
                "received_at": received_at,
                "response_at": response_at
            }
        )).start()

        return response_audio


@bp.route("/get-andy-move-response", methods=["GET"])
def get_andy_move_response():
    """Route for getting Andy's verbal move.

    Query Params:
        board_str: the state of the chess board, as text.
        session_id: the unique session ID to use with Andy.

    Returns:
        An HTTP response, with the data field containing a JSON object. The data
        field will only be present if the status code of the response is 200.

        {
            'response_text': str,
            'board_str': str,
            'move_info': {
                'from': str,
                'to': str,
            }
        }

        response_text (str): the response generated by Andy, as text.
        board_str (str): the board string for the client to display.
        move_info (str): the move info (for logging) on the client.

    """
    if request.method == "GET":
        received_at = datetime.now()
        board_str = request.args.get('board_str')
        session_id = request.args.get('session_id')

        # Make sure query params are present
        if not session_id or not board_str:
            raise Exception(
                "get-audio-response: missing session_id or board_str")

        # Determine Andy's response
        response_text, updated_board_str, move_info = determine_andy_move.determine_andy_move(
            session_id,
            board_str
        )

        # Log Andy's move on a separate thread
        response_at = datetime.now()
        Thread(target=log_andy_move(
            session_id,
            data={
                'move_info': move_info,
                'board_str_before': board_str,
                'board_str_after': updated_board_str,
                'received_at': received_at,
                'response_at': response_at
            }
        )).start()

        return jsonify({
            'response_text': response_text,
            'board_str': updated_board_str,
            'move_info': move_info,
            'game_state': get_game_state(session_id)
        })


@bp.route("/get-response", methods=["POST"])
def get_response():
    """Route for getting a response from Andy and any actions to take.

    Query Params:
        session_id: the unique session ID to use with Andy.
        board_str: FEN representation of board from client.
        detected_text: the text detected from the user.
        recording_time_ms: how long the client took to record, in ms.

    Body:
        A Blob that contains the audio to interpret.

    Returns:
        An HTTP response, with the data field containing a JSON object. The data
        field will only be present if the status code of the response is 200.

        {
            'response_text': str,
            'fulfillment_info': dict,
            'fulfillment_params': dict,
            'board_str': str,
        }

        response_text (str): the response generated by Andy, as text.
        fulfillment_info (dict): the intent information detected from the user
            and the game state.

            {
                'intent_name': str,
                'success': boolean
            }

            intent_name (str): the name of the detected intent.
            success (boolean): whether or not the fulfillment for the intent was
                performed successfully.
        fulfillment_params (dict): the parameters used for the intent. This will
            likely only be used in the event of a MOVE_PIECE_TO intent that is
            successful. In this specific case, fulfillment_params will have the
            format:

            {
                'from_location': str,
                'to_location': str,
            }

        board_str (str): the state of the board, as a FEN string.

    """
    # pylint: disable=broad-except
    if request.method == "POST":
        received_at = datetime.now()
        session_id = request.args.get('session_id')
        detected_text = request.args.get('detected_text')
        recording_time_ms = request.args.get('recording_time_ms', -1)
        # grab board string from HTTP arguments
        board_str = request.args.get('board_str')

        # Make sure query params are present
        game_state = get_game_state(session_id)
        if not session_id or not detected_text or (game_state["game_started"] and not board_str):
            raise Exception(
                "get-response: missing session_id , detected_text, or the game has started and board_str is missing")

        # Reset the current log id
        set_curr_log_id(session_id, None)
        # Reset the fulfillment_params
        set_fulfillment_params(session_id, None)

        # Detect intent from text
        intent_query_response = None
        try:
            intent_query_response = dialogflow_andy.perform_intent_query(
                session_id, detected_text)
        except Exception:
            # Log the error
            err_msg = f"Error performing intent detection: {traceback.format_exc()}"
            log_error(session_id, ERROR_TYPES.INTENT, err_msg)
            # Get the error response
            err_response = get_response_error_return(session_id, board_str)
            # Log the user request on a separate thread
            response_at = datetime.now()
            Thread(target=log_user_request(
                session_id,
                data={
                    "text": detected_text,
                    "audio_data": request.data,
                    "detected_intent": None,
                    "detected_fulfillment": err_response["fulfillment_info"]["intent_name"],
                    "fulfillment_success": err_response["fulfillment_info"]["success"],
                    "board_str_before": board_str,
                    "board_str_after": board_str,
                    "received_at": received_at,
                    "response_at": response_at,
                    "recording_time_ms": float(recording_time_ms)
                }
            )).start()
            # Send the error response
            return jsonify(err_response)
        # Determine Andy's response
        try:
            response_text, fulfillment_info, updated_board_str = intent_processing.fulfill_intent(
                session_id=session_id,
                board_str=board_str,
                intent_data=intent_query_response
            )
        except Exception:
            # Log the error
            err_msg = f"Error performing fulfillment: {traceback.format_exc()}"
            log_error(session_id, ERROR_TYPES.FULFILLMENT, err_msg)
            # Get the error response
            err_response = get_response_error_return(session_id, board_str)
            # Log the user request on a separate thread
            response_at = datetime.now()
            Thread(target=log_user_request(
                session_id,
                data={
                    "text": detected_text,
                    "audio_data": request.data,
                    "detected_intent": intent_query_response.intent.name if intent_query_response is not None else None,
                    "detected_fulfillment": err_response["fulfillment_info"]["intent_name"],
                    "fulfillment_success": err_response["fulfillment_info"]["success"],
                    "board_str_before": board_str,
                    "board_str_after": board_str,
                    "received_at": received_at,
                    "response_at": response_at,
                    "recording_time_ms": float(recording_time_ms)
                }
            )).start()
            # Send the error response
            return jsonify(err_response)

        # Log the user request on a separate thread
        response_at = datetime.now()
        Thread(target=log_user_request(
            session_id,
            data={
                "text": detected_text,
                "audio_data": request.data,
                "detected_intent": intent_query_response.intent.name if intent_query_response is not None else None,
                "detected_fulfillment": fulfillment_info["intent_name"],
                "fulfillment_success": fulfillment_info["success"],
                "board_str_before": board_str,
                "board_str_after": updated_board_str,
                "received_at": received_at,
                "response_at": response_at,
                "recording_time_ms": float(recording_time_ms)
            }
        )).start()

        return jsonify({
            'response_text': response_text,
            'fulfillment_info': fulfillment_info,
            'fulfillment_params': get_fulfillment_params(session_id),
            'board_str': updated_board_str,
            'game_state': get_game_state(session_id)
        })
