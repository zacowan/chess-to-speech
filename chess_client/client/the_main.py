'''
Created on Oct 9, 2021

@author: Legacy
'''
import threading
from pathlib import Path

from . import window
from . import game_engine
from . import audio_detection
from .utils import AUDIO_PATH

# May not need, dependent on Rest API testing, For now I will leave this here
init_complete = False
close = False  # If this gets set to true it will notify all threads to close and cause the program to end

# Method for Threads to see if they need to close


def is_closed():
    return close


def main():
    try:
        # Setup directories
        Path(AUDIO_PATH).mkdir(parents=True, exist_ok=True)
        print("Window being made.")
        screen = window.start_screen()  # Create Window
        print("Window Completed.")
        print("Audio Thread Being made.")
        audio = threading.Thread(
            target=audio_detection.run)  # @IgnorePep8
        print("Audio Thread Completed.")
        print("Audio Thread Starting.")
        audio.start()  # Thread that Handles Incoming and Outgoing audio
        print("Audio Thread Running.")
        print("game_engine Starting.")
        # Main thread will handle Visuals
        game_engine.setup_game_engine(screen)
    except Exception as e:
        global close
        close = True
        print(e)
        traceback.print_exc()


if __name__ == '__main__':  # @IgnorePep8
    main()
