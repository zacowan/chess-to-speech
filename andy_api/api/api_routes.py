"""This module contains all of the routes accessible to the client.

Attributes:
    bp: The blueprint that the __init__.py will use to handle routing.

"""
from flask import (
    Blueprint, request, jsonify
)

from . import speech_text_processing, dialogflow_andy
from .intent_processing import intent_processing

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route("/get-session", methods=["GET"])
def get_session():
    """Route for getting a unique session ID to use with Andy.

    Returns:
        An HTTP response, with the data field containing a JSON object. The data
        field will only be present if the status code of the response is 200.

        {
            'ID': str
        }

        ID (str): the unique session ID generated.

    """
    if request.method == "GET":
        session_id = dialogflow_andy.create_session()
        return jsonify({
            'ID': session_id
        })


@bp.route("/get-response", methods=["POST"])
def get_response():
    """Route for getting a response from Andy and any actions to take.

    Query Params:
        session_id: the unique session ID to use with Andy.

    Body:
        A Blob that contains the audio to interpret.

    Returns:
        An HTTP response, with the data field containing a JSON object. The data
        field will only be present if the status code of the response is 200.

        {
            'response_text': str,
            'response_audio': str,
            'intent': dict
        }

        response_text (str): the response generated by Andy, as text.
        response_audio (str): the location of the audio response generated by
            Dialogflow.
        fulfillment_info (dict): the intent information detected from the user
            and the game state.

            {
                'intent_name': str,
                'success': boolean
            }

            intent_name (str): the name of the detected intent.
            success (boolean): whether or not the fulfillment for the intent was
                performed successfully.

    """
    if request.method == "POST":
        session_id = request.args.get('session_id')

        # Get text from audio file
        transcribed_audio = speech_text_processing.transcribe_audio_file(
            request.data)

        # Detect intent from text
        intent_query_response = dialogflow_andy.perform_intent_query(
            session_id, transcribed_audio)

        # Determine Andy's response
        response_text, fulfillment_info = intent_processing.fulfill_intent(
            intent_query_response, "TEST")

        # Convert response to audio
        response_audio = speech_text_processing.generate_audio_response(
            response_text)

        return jsonify({
            'response_text': response_text,
            'response_audio': response_audio,
            'fulfillment_info': fulfillment_info,
            # Just for debugging:
            'transcribed_audio': transcribed_audio,
            'detected_intent': intent_query_response.intent.display_name
        })
