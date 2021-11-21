"""Updated way of detecting voice and determining turn-taking.

Based on https://github.com/wiseman/py-webrtcvad/blob/master/example.py.
"""
import wave
import uuid
import requests
import speech_recognition as sr
import simpleaudio as sa
import chess
import traceback
from . import the_main
from . import bias_adjustment
from . import game_engine
from datetime import datetime
from .utils import AUDIO_PATH

BASE_API_URL = "http://127.0.0.1:5000/api"
SESSION_ID = str(uuid.uuid4())
USER_AUDIO_FILENAME = f"{AUDIO_PATH}/user_audio.wav"
ANDY_AUDIO_FILENAME = f"{AUDIO_PATH}/andy_audio.wav"

# Speech recognition constants
STARTING_ENERGY_THRESHOLD = 3000
VOICE_FACTOR = 2.5
MINIMUM_ENERGY_THRESHOLD = 150


def run():
    timer=datetime.now()
    timerActive= False
    prefix = ""
    timerThreshold= 45
    failCounterThreshold=2
    failCounter = 0
    r = sr.Recognizer()

    # Recognition settings
    # This controls the default threshold for what we consider to be background noise
    r.energy_threshold = STARTING_ENERGY_THRESHOLD
    # This controls the factor that voice is louder than the threshold
    r.dynamic_energy_ratio = VOICE_FACTOR

    while not the_main.is_closed() and not game_engine.is_game_over:
        # obtain audio from the microphone
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
            print("Recognizing...")
            if(the_main.is_closed()):
                break

        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            detected_text = r.recognize_google(audio)
            detected_text = bias_adjustment.adjust_with_bias(detected_text)
            game_engine.lastSaid = detected_text
            print(f"Detected text: {detected_text}")
        except sr.UnknownValueError:
            detected_text = None
            print("Loadded")
            print((datetime.now()-timer).total_seconds())
            print("Google Speech Recognition could not understand audio")
            if timerActive and (datetime.now()-timer).total_seconds()>timerThreshold:
                print("TRIGGER")
                timer=datetime.now()
                timerActive= False
                detected_text = "What is my best move?"
                prefix ="You seem to be taking a while, "
            else:
                continue
        except sr.RequestError as e:
            detected_text = None
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))

        # Generate an audio file
        with open(USER_AUDIO_FILENAME, "wb") as f:
            f.write(audio.get_wav_data())

        # Get the intent
        intent_response = get_user_intent(
            detected_text, start_recording_at, stop_recording_at)
        if not intent_response:
            continue
        print(intent_response["fulfillment_info"]["intent_name"])
        intent_info = intent_response["response_text"]
        print(not intent_response["fulfillment_info"]["intent_name"] == "FALLBACK" or not failCounter==failCounterThreshold)
        if not intent_response["fulfillment_info"]["intent_name"] == "FALLBACK" or not failCounter+1==failCounterThreshold:
            # Get the audio response
            audio_response = get_audio_response(prefix+intent_info)
            # Play the audio response
            f = open(ANDY_AUDIO_FILENAME, "wb")
            f.truncate(0)
            f.write(audio_response)
            f.close()
            wave_obj = sa.WaveObject.from_wave_file(ANDY_AUDIO_FILENAME)
            play_obj = wave_obj.play()
            play_obj.wait_done()  # Wait until sound has finished playing
            game_engine.is_game_over = intent_response["game_state"]["game_finished"]
        if intent_response["game_state"]["game_finished"]:
            timerActive = False
        if (intent_response["fulfillment_info"]["intent_name"] == "FALLBACK" or not prefix =="") and game_engine.isGameStarted:
            failCounter+=1
            timerThreshold+=10
            if failCounter==failCounterThreshold:
                failCounterThreshold+=1
                failCounter+=4
                
                detected_text = "What Can I do"
                intent_response = get_user_intent(detected_text, start_recording_at, stop_recording_at)
                if not intent_response:
                    continue
                print(intent_response["fulfillment_info"]["intent_name"])
                intent_info = intent_response["response_text"]
                # Get the audio response
                audio_response = get_audio_response("You seem to be having difficulty asking me to do something, "+intent_info)
                # Play the audio response
                f = open(ANDY_AUDIO_FILENAME, "wb")
                f.truncate(0)
                f.write(audio_response)
                f.close()
                wave_obj = sa.WaveObject.from_wave_file(ANDY_AUDIO_FILENAME)
                play_obj = wave_obj.play()
                play_obj.wait_done()  # Wait until sound has finished playing     
        else:
            failCounter=0
        prefix =""
        if (intent_response["fulfillment_info"]["intent_name"] == "MOVE_PIECE" or (intent_response["fulfillment_info"]["intent_name"] == "CHOOSE_SIDE" and intent_response["game_state"]["chosen_side"] == "black")) and intent_response["fulfillment_info"]["success"]:
            # Get the intent
            if intent_response["fulfillment_info"]["intent_name"] == "MOVE_PIECE":
                game_engine.move_history.insert(
                    0, "User: " + intent_response['fulfillment_params']['from_location'].upper() + " to " + intent_response['fulfillment_params']['to_location'].upper())
            intent_response = get_andy_move()
            if not timerActive:
                timerActive = True
                timer = datetime.now()
                timerThreshold = 45
            if not intent_response:
                continue
            intent_info = intent_response["response_text"]
            # Get the audio response
            audio_response = get_audio_response(intent_info)
            # Play the audio response
            f = open(ANDY_AUDIO_FILENAME, "wb")
            f.truncate(0)
            f.write(audio_response)
            f.close()
            wave_obj = sa.WaveObject.from_wave_file(ANDY_AUDIO_FILENAME)
            play_obj = wave_obj.play()
            play_obj.wait_done()  # Wait until sound has finished playing
            game_engine.board = chess.Board(intent_response["board_str"])
            print(game_engine.board)
            game_engine.move_history.insert(0, "Andy: " + intent_response['move_info']['from'].upper(
            ) + " to " + intent_response['move_info']['to'].upper())
            game_engine.is_game_over = intent_response["game_state"]["game_finished"]
        if (intent_response["fulfillment_info"]["intent_name"] == "RESTART_GAME"):
            game_engine.move_history.clear()
            game_engine.isGameStarted = False
            game_engine.lastSaid = ""
            game_engine.user_is_black = False
            game_engine.is_game_over = False
            game_engine.board = None
        if (intent_response["fulfillment_info"]["intent_name"] == "UNDO_MOVE"):
            if game_engine.move_history.size()>1:
                game_engine.move_history.pop(0)
                game_engine.move_history.pop(0)
            else:
                print("Attempted to Pop and empty move history list")
def get_audio_response(text):
    request_url = f"{BASE_API_URL}/get-audio-response?session_id={SESSION_ID}"
    print(f"Body: {text}")
    response = requests.post(request_url, text)
    if response.status_code == 200:
        return response.content
    else:
        print("API Error, Status Code:"+response.status_code)
        raise Exception


def get_andy_move():
    try:
        request_url = f"{BASE_API_URL}/get-andy-move-response?session_id={SESSION_ID}&board_str={game_engine.board.fen()}"
        response = requests.get(request_url)
        if response.status_code == 200:
            return response.json()
        else:
            print("API Error, Status Code:"+response.status_code)
            return None
    except Exception as e:
        print(e)


def get_user_intent(detected_text, start_recording, stop_recording):
    try:
        recording_time_ms = (
            stop_recording - start_recording).total_seconds() * 1000
        if game_engine.board:
            request_url = f"{BASE_API_URL}/get-response?session_id={SESSION_ID}&board_str={game_engine.board.fen()}&detected_text={detected_text}"
        else:
            request_url = f"{BASE_API_URL}/get-response?session_id={SESSION_ID}&detected_text={detected_text}"

        # Send recording_time_ms to API
        request_url += f"&recording_time_ms={str(recording_time_ms)}"

        response = requests.post(request_url, open(
            USER_AUDIO_FILENAME, 'rb'), USER_AUDIO_FILENAME)
        if response.status_code == 200:
            if response.json()["board_str"]:
                game_engine.board = chess.Board(response.json()["board_str"])
                game_engine.isGameStarted = True
            if response.json()["game_state"]["chosen_side"] == "black":
                game_engine.user_is_black = True
            return response.json()
        else:
            print("API Error, Status Code:"+response.status_code)
            return None
    except Exception as e:
        print(e)
        traceback.print_exc()


# # For testing
# if __name__ == '__main__':  # @IgnorePep8
#     run()
