'''
Created on Oct 9, 2021

@author: Legacy
'''
import threading
from . import window
from . import game_engine
from . import audio_engine
from . import rest_service

# May not need, dependent on Rest API testing, For now I will leave this here
init_complete = False
close = False  # If this gets set to true it will notify all threads to close and cause the program to end

# Method for Threads to see if they need to close


def is_closed():
    return close


def main():
    try:
        print("Window being made.")
        screen = window.start_screen()  # Create Window
        print("Window Completed.")
        print("Audio Thread Being made.")
        audio = threading.Thread(
            target=audio_engine.setup_audio_engine)  # @IgnorePep8
        print("Audio Thread Completed.")
        print("Audio Thread Starting.")
        audio.start()  # Thread that Handles Incoming and Outgoing audio
        print("Audio Thread Running.")
        print("Rest Service Thread Being made.")
        rest = threading.Thread(
            target=rest_service.setup_rest_service)  # @IgnorePep8
        print("Rest Service Thread Completed.")
        print("Rest Service Thread Starting.")
        rest.start()  # Thread that Handles Incoming and Outgoing API Data
        print("Rest Service Thread Running.")
        print("game_engine Starting.")
        # Main thread will handle Visuals
        game_engine.setup_game_engine(screen)
    except Exception as e:
        global close
        close = True


if __name__ == '__main__':  # @IgnorePep8
    main()
