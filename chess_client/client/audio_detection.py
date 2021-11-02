"""Updated way of detecting voice and determining turn-taking.

Based on https://github.com/wiseman/py-webrtcvad/blob/master/example.py.
"""
import wave
import uuid
import collections
import requests
import webrtcvad
from pyaudio import PyAudio, paInt16
import simpleaudio as sa

from . import game_engine
from .utils import AUDIO_PATH

BASE_API_URL = "http://127.0.0.1:5000/api"
SESSION_ID = str(uuid.uuid4())
FORMAT = paInt16
CHANNELS = 1
RATE = 48000
CHUNK_DURATION_MS = 30
PADDING_DURATION_MS = 1000
VOICED_AUDIO_THRESHOLD = 0.8
NUM_PADDING_FRAMES = int(PADDING_DURATION_MS / CHUNK_DURATION_MS)
CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)
USER_AUDIO_FILENAME = f"{AUDIO_PATH}/user_audio.wav"
ANDY_AUDIO_FILENAME = f"{AUDIO_PATH}/andy_audio.wav"


def run():
    # Setup
    vad = webrtcvad.Vad(3)
    p = PyAudio()

    while True:

        audio_stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE
        )

        have_utterance = False

        audio_window_buffer = collections.deque(maxlen=NUM_PADDING_FRAMES)
        triggered = False

        voiced_frames = []

        while not have_utterance:
            chunk = audio_stream.read(CHUNK_SIZE)
            is_speech = vad.is_speech(chunk, RATE)

            if is_speech:
                print("1")
            else:
                print("_")

            # User has not started speaking yet
            if not triggered:
                # Add audio to the current window
                audio_window_buffer.append((chunk, is_speech))
                num_voiced_frames = len(
                    [f for f, speech in audio_window_buffer if speech])

                # Check if voiced audio duration is above VOICED_AUDIO_THRESHOLD * PADDING_DURATION_MS
                if num_voiced_frames > (audio_window_buffer.maxlen * VOICED_AUDIO_THRESHOLD):
                    print("Started speaking")
                    # User has started speaking
                    triggered = True
                    # Include audio within the window inside of the return array
                    for f, _ in audio_window_buffer:
                        voiced_frames.append(f)
                    # Clear the current window
                    audio_window_buffer.clear()
            else:
                # Add audio to the return array
                voiced_frames.append(chunk)
                # Add audio to the current window
                audio_window_buffer.append((chunk, is_speech))
                num_unvoiced = len(
                    [f for f, speech in audio_window_buffer if not speech])

                # Check if unvoiced audio duration is above VOICED_AUDIO_THRESHOLD * PADDING_DURATION_MS
                if num_unvoiced > (audio_window_buffer.maxlen * VOICED_AUDIO_THRESHOLD):
                    print("Stopped speaking")
                    # User is done speaking
                    have_utterance = True

        audio_stream.stop_stream()
        audio_stream.close()

        # Generate an audio file
        write_user_audio_file(voiced_frames, p.get_sample_size(FORMAT))

        # Get the intent
        intent_info = get_user_intent()
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

    p.terminate()
    print("Audio detection closed")


def get_audio_response(text):
    request_url = f"{BASE_API_URL}/get-audio-response?session_id={SESSION_ID}"
    response = requests.post(request_url, text)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception


def get_user_intent():
    request_url = f"{BASE_API_URL}/get-response?session_id={SESSION_ID}&board_str={game_engine.board.fen()}"
    response = requests.post(request_url, open(
        USER_AUDIO_FILENAME, 'rb'), USER_AUDIO_FILENAME)
    if response.status_code == 200:
        return response.json()["response_text"]
    else:
        return None


def write_user_audio_file(frames, sample_width):
    # Write an audio file out
    wf = wave.open(USER_AUDIO_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


# # For testing
# if __name__ == '__main__':  # @IgnorePep8
#     run()
