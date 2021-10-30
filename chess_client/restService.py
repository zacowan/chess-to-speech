'''
Created on Oct 16, 2021

@author: Legacy
'''
import requests
import theMain
import gameEngine
import time
import audioEngine
import uuid
from chess import Board

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
            session_id+"&board_str="+gameEngine.board.__str__()
        # API Request
        # TODO:Fill in With Proper info @IgnorePep8
        response = requests.post(url, open(temp_path, 'rb'), temp_path)
        audio_response = requests.post(
            f"http://localhost:5000/api/get-audio-response?session_id={session_id}", response.json()["response_text"])
        gameEngine.board = Board(response.json()["board_str"])

        # TODO: Some how create an audio file of Andy's response from the data sent back
        file_path = "TODO: File name for Andy's response"

        # Plays Andy's Response to the User
        audioEngine.playAudio(file_path)


# Call this Function to Send audio to Andy
def sendUserAudio(filepath):
    global new_audio_path
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
