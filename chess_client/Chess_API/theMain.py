'''
Created on Oct 9, 2021

@author: Legacy
'''
import threading
import window
import gameEngine
import audioEngine
import restService

init_complete = False


def main():
    print("Window being made.")
    screen = window.startScreen()  # Create Window
    print("Window Completed.")
    print("Audio Thread Being made.")
    audio = threading.Thread(target= audioEngine.setupAudioEngine, args=(0,))  # @IgnorePep8
    print("Audio Thread Completed.")
    print("Audio Thread Starting.")
    audio.start()  # Thread that Handles Incoming and Outgoing audio
    print("Audio Thread Running.")
    print("Rest Service Thread Being made.")
    audio = threading.Thread(target= restService.setupRestService, args=(0,))  # @IgnorePep8
    print("Rest Service Thread Completed.")
    print("Rest Service Thread Starting.")
    audio.start()  # Thread that Handles Incoming and Outgoing audio
    print("Rest Service Thread Running.")
    print("GameEngine Starting.")
    gameEngine.setupGameEngine(screen)  # Main thread handles Visuals


if __name__ == '__main__':  # @IgnorePep8
    main()


