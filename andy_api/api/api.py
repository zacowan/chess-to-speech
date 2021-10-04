from flask import (
    Blueprint, request, jsonify
)
from . import speech_to_text, andy

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route("/")
def hello_world():
    return "Chess-to-Speech Client API"


@bp.route("/start-session", methods=["GET"])
def start_session():
    if (request.method == "GET"):
        return jsonify(andy.create_session())


@bp.route("/get-audio-response", methods=["POST"])
def get_audio_response():
    if request.method == "POST":
        session_id = request.args.get('session_id')

        transcribed_audio = speech_to_text.transcribe_audio_file(request.data)

        if transcribed_audio == None:
            return "Failed to transcribe audio"

        try:
            response = jsonify(andy.fetch_response(
                session_id, transcribed_audio))
            return response
        except:
            return "Could not determine intent"
