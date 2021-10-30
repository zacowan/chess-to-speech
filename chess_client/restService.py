'''
Created on Oct 16, 2021

@author: Legacy
'''
import requests
import theMain
import gameEngine
import time
import uuid
from pygame import mixer
from chess import Board

OUTPUT_FILE_NAME = "andy_response.mp3"

new_audio_path = ""
# potential BUGS: We could receive more audio files then we can send / receive responses for (May have to make queue for audio paths)


def setupRestService():
    global new_audio_path
    session_id = str(uuid.uuid4())
    headers = {'content-type': 'audio/wav'}
    # Change the below condition to theMain.init_complete and not theMain.isClosed() once the rest service is operational
    # This while loop yields the thread until the other threads are finished starting up
    while theMain.init_complete and not theMain.isClosed():
        time.sleep(0)
    # Run until the Program is closed
    while not theMain.isClosed():
        # Yield the Thread until we have file to send
        while new_audio_path == "":  # Yield Thread until Audio file can be sent
            time.sleep(0)

        # Store the file and remove it from our global var
        temp_path = new_audio_path
        new_audio_path = ""
        url = "http://localhost:5000/api/get-response?session_id=" + \
            session_id+"&board_str="+gameEngine.board.fen()

        # API Request
        # TODO: check if the requests are sync or async
        response = requests.post(url, open(temp_path, 'rb'), temp_path)
        if response.status_code == 200:
            print(response.json())
            audio_response = requests.post(
                f"http://localhost:5000/api/get-audio-response?session_id={session_id}", response.json()["response_text"])
            gameEngine.board = Board(response.json()["board_str"])

            # Write audio_response to file
            with open(OUTPUT_FILE_NAME, "wb") as out:
                # Clear the contents of the file
                out.truncate(0)
                # Write the response to the output file.
                out.write(audio_response.content)

            # Plays Andy's Response to the User
            print("Playing sound")
            # TODO: audio not playing, but audio file IS being generated.
            mixer.init()
            mixer.music.load(OUTPUT_FILE_NAME)
            mixer.music.play()
        else:
            print("Error with response")


# Call this Function to Send audio to Andy
def sendUserAudio(filepath):
    global new_audio_path
    print(f"Setting new path to {filepath}. Old path: {new_audio_path}")
    new_audio_path = filepath


# This is for testing purposes will delete later
# method 1 for API requests
#url = "https://f16de73c.ngrok.io/api/audio"
# data = open(r'C:\Users\rickk\Desktop\agenda.wav', 'rb')}
#headers = {'content-type': 'audio/wav'}
#r = requests.post(url, data=data, headers=headers)

# method 2 for API requests
#url = " https://ba7928ba.ngrok.io/api/audio"
#fin = open(r'D:/MediaFiles/OneDrive_1_2-7-2020/Recording_90.wav', 'rb')
#files = {'file': fin}
#r = requests.post(url, files=files)
