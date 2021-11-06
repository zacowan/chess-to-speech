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
from . import game_engine
from datetime import datetime
from .utils import AUDIO_PATH

BASE_API_URL = "http://127.0.0.1:5000/api"
SESSION_ID = str(uuid.uuid4())
USER_AUDIO_FILENAME = f"{AUDIO_PATH}/user_audio.wav"
ANDY_AUDIO_FILENAME = f"{AUDIO_PATH}/andy_audio.wav"


def run():

    r = sr.Recognizer()

    while not the_main.is_closed():
        # obtain audio from the microphone
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("*"*20)
            print("Say something!")
            game_engine.isMicOn = True
            start_recording_at = datetime.now()
            audio = r.listen(source, phrase_time_limit=8)
            stop_recording_at = datetime.now()
            game_engine.isMicOn = False
            print("Recognizing...")

        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            detected_text = r.recognize_google(audio)
            print(f"Detected text: {detected_text}")
        except sr.UnknownValueError:
            detected_text = None
            print("Google Speech Recognition could not understand audio")
            continue
        except sr.RequestError as e:
            detected_text = None
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))

        # Generate an audio file
        with open(USER_AUDIO_FILENAME, "wb") as f:
            f.write(audio.get_wav_data())

        # Get the intent
        intent_info = get_user_intent(
            detected_text, start_recording_at, stop_recording_at)
        if not intent_info:
            continue
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


def get_audio_response(text):
    request_url = f"{BASE_API_URL}/get-audio-response?session_id={SESSION_ID}"
    response = requests.post(request_url, text)
    if response.status_code == 200:
        return response.content
    else:
        print("API Error, Status Code:"+response.status_code)
        raise Exception


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
            print(response.json()["board_str"])
            if response.json()["board_str"]:
                game_engine.board = chess.Board(response.json()["board_str"])
                game_engine.isGameStarted = True
            return response.json()["response_text"]
        else:
            print("API Error, Status Code:"+response.status_code)
            return None
    except Exception as e:
        print(e)
        traceback.print_exc()


# # For testing
# if __name__ == '__main__':  # @IgnorePep8
#     run()
