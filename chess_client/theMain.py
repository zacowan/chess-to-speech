'''
Created on Oct 9, 2021

@author: Legacy
'''
import threading
import window
import gameEngine
import audioEngine
import restService

# May not need, dependent on Rest API testing, For now I will leave this here
init_complete = False
close = False  # If this gets set to true it will notify all threads to close and cause the program to end

# Method for Threads to see if they need to close


def isClosed():
    return close


def main():
    print("Window being made.")
    screen = window.startScreen()  # Create Window
    print("Window Completed.")
    print("Audio Thread Being made.")
    audio = threading.Thread(
        target=audioEngine.setupAudioEngine)  # @IgnorePep8
    print("Audio Thread Completed.")
    print("Audio Thread Starting.")
    audio.start()  # Thread that Handles Incoming and Outgoing audio
    print("Audio Thread Running.")
    print("Rest Service Thread Being made.")
    rest = threading.Thread(target=restService.setupRestService)  # @IgnorePep8
    print("Rest Service Thread Completed.")
    print("Rest Service Thread Starting.")
    rest.start()  # Thread that Handles Incoming and Outgoing API Data
    print("Rest Service Thread Running.")
    print("GameEngine Starting.")
    gameEngine.setupGameEngine(screen)  # Main thread will handle Visuals


if __name__ == '__main__':  # @IgnorePep8
    main()
