"""Updated way of detecting voice and determining turn-taking.

Based on https://github.com/wiseman/py-webrtcvad/blob/master/example.py.
"""
import uuid
import requests
import speech_recognition as sr
import simpleaudio as sa
import chess
import traceback
from typing import Tuple, Union
from . import the_main
from . import bias_adjustment
from . import game_engine
from datetime import datetime
from .utils import AUDIO_PATH
from .help_timer_counter import HelpTimerCounter

BASE_API_URL = "http://127.0.0.1:5000/api"
SESSION_ID = str(uuid.uuid4())
USER_AUDIO_FILENAME = f"{AUDIO_PATH}/user_audio.wav"
ANDY_AUDIO_FILENAME = f"{AUDIO_PATH}/andy_audio.wav"

# Speech recognition constants
STARTING_ENERGY_THRESHOLD = 3000
VOICE_FACTOR = 2.5
MINIMUM_ENERGY_THRESHOLD = 150


def run():
    timer_counter = HelpTimerCounter()
    r = sr.Recognizer()

    # Recognition settings
    # This controls the default threshold for what we consider to be background noise
    r.energy_threshold = STARTING_ENERGY_THRESHOLD
    # This controls the factor that voice is louder than the threshold
    r.dynamic_energy_ratio = VOICE_FACTOR

    while not the_main.is_closed() and not game_engine.is_game_over:
        # Obtain audio from the microphone
        audio, start_recording_at, stop_recording_at = record_audio(r)
        # Don't try to continue if the game stopped while recording
        if the_main.is_closed():
            break

        # Get text from audio
        detected_text = recognize_audio(r, audio)

        # If we don't detect anything and we exceed a timeout, tell the user we can provide them with a move
        if not detected_text:
            if timer_counter.check_timer():
                print("TRIGGER")
                timer_counter.stop_timer()
                audio_response = get_help_response("TIMEOUT")
                play_audio_response(audio_response)
                continue
            else:
                # Go back to the start of the loop
                continue

        # Generate an audio file
        with open(USER_AUDIO_FILENAME, "wb") as f:
            f.write(audio.get_wav_data())

        # Get the intent
        intent_response = get_user_intent(
            detected_text, start_recording_at, stop_recording_at)
        # If no intent was detected, go back to the start of the loop
        if not intent_response:
            continue
        print(intent_response["fulfillment_info"]["intent_name"])

        response_game_state = intent_response["game_state"]
        response_intent_name = intent_response["fulfillment_info"]["intent_name"]
        fulfillment_success = intent_response["fulfillment_info"]["success"]

        # Successful or failed fulfillments
        if game_engine.isGameStarted and response_intent_name == "FALLBACK" and timer_counter.update_counter():
            timer_counter.hit_counter()
            # Get the audio response
            audio_response = get_help_response("FALLBACK")
            # Play the audio response
            play_audio_response(audio_response)
        else:
            if response_intent_name != "FALLBACK":
                timer_counter.reset_counter()
            timer_counter.update_timer()
            # Get Andy's audio response
            audio_response = get_audio_response(
                intent_response["response_text"])

            # Play the audio response
            play_audio_response(audio_response)

            # Successful fulfillments only
            if fulfillment_success:
                if response_intent_name == "MOVE_PIECE":
                    # Update move history
                    from_loc = intent_response['fulfillment_params']['from_location']
                    to_loc = intent_response['fulfillment_params']['to_location']
                    update_move_history(True, from_loc, to_loc)
                    # Move Andy's piece
                    handle_move_andy_piece()
                # TODO: change this to the new DIFFICULTY_SELECTION intent when ready
                elif response_intent_name == "CHOOSE_SIDE" and game_engine.user_is_black:
                    # Make Andy's first move
                    handle_move_andy_piece()
                elif response_intent_name == "RESTART_GAME_YES":
                    # Clear all of the game state
                    game_engine.move_history.clear()
                    game_engine.isGameStarted = False
                    game_engine.lastSaid = ""
                    game_engine.user_is_black = False
                    game_engine.is_game_over = False
                    game_engine.board = None
                    timer_counter = HelpTimerCounter()
                    continue
                elif response_intent_name == "UNDO_MOVE":
                    if len(game_engine.move_history) > 1:
                        game_engine.move_history.pop(0)
                        game_engine.move_history.pop(0)
                    else:
                        print("Attempted to Pop and empty move history list")
                # Enable the counter when we encounter a successful intent
                timer_counter.start_timer()

        # Update game state
        game_engine.is_game_over = response_game_state["game_finished"]
        if game_engine.is_game_over:
            timer_counter.stop_timer()


def play_audio_response(audio_data: bytes):
    """
    Plays Andy's audio response from raw bytes.
    """
    f = open(ANDY_AUDIO_FILENAME, "wb")
    f.truncate(0)
    f.write(audio_data)
    f.close()
    wave_obj = sa.WaveObject.from_wave_file(ANDY_AUDIO_FILENAME)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing


def record_audio(r: sr.Recognizer) -> Tuple[sr.AudioData, datetime, datetime]:
    """
    Records audio from the microphone.

    Returns:
        Audio data captured.
        The time that recording started at.
        The time that recording stopped at.
    """
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        # Create a minimum for the energy threshold
        if r.energy_threshold < MINIMUM_ENERGY_THRESHOLD:
            r.energy_threshold = MINIMUM_ENERGY_THRESHOLD
        print(f"Energy threshold: {r.energy_threshold}")
        print("*"*20)
        print("Say something!")
        start_recording_at = datetime.now()
        game_engine.isMicOn = True
        audio = r.listen(source, phrase_time_limit=8)
        game_engine.isMicOn = False
        stop_recording_at = datetime.now()
        print(f"{(stop_recording_at-start_recording_at).total_seconds()*1000} ms")

    return audio, start_recording_at, stop_recording_at


def recognize_audio(r: sr.Recognizer, audio: sr.AudioData) -> Union[str, None]:
    """
    Recognizes speech from audio data.

    Returns:
        The detected text, adjusted with bias corrections, or None if nothing
        was detected.
    """
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        detected_text = r.recognize_google(audio)
        detected_text = bias_adjustment.adjust_with_bias(detected_text)
        game_engine.lastSaid = detected_text
        print(f"Detected text: {detected_text}")
        return detected_text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(e))
        return None


def handle_move_andy_piece():
    # Get Andy's move
    andy_move_response = get_andy_move()
    if not andy_move_response:
        return
    # Get the audio response
    audio_response = get_audio_response(
        andy_move_response["response_text"])
    # Play the audio response
    play_audio_response(audio_response)
    # Update game state
    game_engine.board = chess.Board(
        andy_move_response["board_str"])
    print(game_engine.board)
    # Update move history
    from_loc = andy_move_response['move_info']['from']
    to_loc = andy_move_response['move_info']['to']
    update_move_history(False, from_loc, to_loc)


def update_move_history(user_move: bool, from_location: str, to_location: str):
    mover = "Andy"
    if user_move:
        mover = "You"
    entry = f"{mover}: {from_location.upper()} to {to_location.upper()}"
    game_engine.move_history.insert(0, entry)


def get_help_response(help_type):
    """
    help_type is one of ["TIMEOUT", "FALLBACK"]
    """
    request_url = f"{BASE_API_URL}/get-help-audio-response?session_id={SESSION_ID}&help_type={help_type}"
    response = requests.get(request_url)
    if response.status_code == 200:
        return response.content
    else:
        print("API Error, Status Code:" + str(response.status_code))
        raise Exception


def get_audio_response(text):
    request_url = f"{BASE_API_URL}/get-audio-response?session_id={SESSION_ID}"
    print(f"Body: {text}")
    response = requests.post(request_url, text)
    if response.status_code == 200:
        return response.content
    else:
        print("API Error, Status Code:" + str(response.status_code))
        raise Exception


def get_andy_move():
    try:
        request_url = f"{BASE_API_URL}/get-andy-move-response?session_id={SESSION_ID}&board_str={game_engine.board.fen()}"
        response = requests.get(request_url)
        if response.status_code == 200:
            return response.json()
        else:
            print("API Error, Status Code:" + str(response.status_code))
            return None
    except Exception as e:
        print(e)
        return None


def get_user_intent(detected_text, start_recording, stop_recording):
    try:
        recording_time_ms = (
            stop_recording - start_recording).total_seconds() * 1000

        request_url = f"{BASE_API_URL}/get-response?session_id={SESSION_ID}&detected_text={detected_text}"

        # Add board string to request URL
        if game_engine.board:
            request_url += f"&board_str={game_engine.board.fen()}"

        # Add recording time to request URL
        request_url += f"&recording_time_ms={str(recording_time_ms)}"

        # Make the request
        response = requests.post(request_url, open(
            USER_AUDIO_FILENAME, 'rb'), USER_AUDIO_FILENAME)

        if response.status_code == 200:
            response_json = response.json()

            if response_json["game_state"]["chosen_side"] == "black":
                game_engine.user_is_black = True

            if response_json["board_str"]:
                game_engine.board = chess.Board(response_json["board_str"])
                game_engine.isGameStarted = True

            return response_json
        else:
            print("API Error, Status Code:" + str(response.status_code))
            return None
    except Exception as e:
        print(e)
        traceback.print_exc()
        return None


# # For testing
# if __name__ == '__main__':  # @IgnorePep8
#     run()
