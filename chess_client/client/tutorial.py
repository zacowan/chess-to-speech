"""This file will handle displaying the tutorial screens.

Created on November 16, 2021.

@author: Zach Cowan

"""
import pygame
from . import audio_detection

TUTORIAL_SCREEN_LOCATIONS = [
    "./images/title_screen.png",
    "./images/tutorial1_screen.png",
    "./images/tutorial2_screen.png"
]


WHITE_FILL = (255, 255, 255)


def run(screen: pygame.Surface):
    """Main method for going through the tutorial screens."""
    clock = pygame.time.Clock()

    my_font = pygame.font.SysFont('Times', 22)
    session_id_text = my_font.render(
        "Your Session ID: " + audio_detection.SESSION_ID[0:8], True, (0, 0, 0))

    # Preload images
    screens: list[pygame.Surface] = []
    for loc in TUTORIAL_SCREEN_LOCATIONS:
        s = pygame.image.load(loc)
        screens.append(s)

    drawn = False
    curr_screen = 0
    while curr_screen < len(screens):
        # Display the current screen
        if not drawn:
            screen.fill(WHITE_FILL)
            screen.blit(screens[curr_screen], (0, 0))
            screen.blit(session_id_text, (20, 560))
            pygame.display.update()
            drawn = True

        # Allow the user to click to continue
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                curr_screen += 1
                drawn = False

        # Limit frame rate to 60 fps
        clock.tick(60)
