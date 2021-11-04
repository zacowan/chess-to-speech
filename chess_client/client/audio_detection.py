"""Updated way of detecting voice and determining turn-taking.

Based on https://github.com/wiseman/py-webrtcvad/blob/master/example.py.
"""
import wave
import uuid
import requests
import speech_recognition as sr
import simpleaudio as sa

from . import game_engine
from .utils import AUDIO_PATH

BASE_API_URL = "http://127.0.0.1:5000/api"
SESSION_ID = str(uuid.uuid4())
USER_AUDIO_FILENAME = f"{AUDIO_PATH}/user_audio.wav"
ANDY_AUDIO_FILENAME = f"{AUDIO_PATH}/andy_audio.wav"


def run():

    r = sr.Recognizer()

    while True:

        # obtain audio from the microphone
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("*"*20)
            print("Say something!")
            audio = r.listen(source, phrase_time_limit=8)
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
        except sr.RequestError as e:
            detected_text = None
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))

        # Generate an audio file
        with open(USER_AUDIO_FILENAME, "wb") as f:
            f.write(audio.get_wav_data())

        # Get the intent
        intent_info = get_user_intent(detected_text)
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
        raise Exception


def get_user_intent(detected_text):
    request_url = f"{BASE_API_URL}/get-response?session_id={SESSION_ID}&board_str={game_engine.board.fen()}&detected_text={detected_text}"
    response = requests.post(request_url, open(
        USER_AUDIO_FILENAME, 'rb'), USER_AUDIO_FILENAME)
    if response.status_code == 200:
        return response.json()["response_text"]
    else:
        return None


# # For testing
# if __name__ == '__main__':  # @IgnorePep8
#     run()
