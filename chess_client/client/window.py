'''
Created on Oct 9, 2021

@author: Legacy
'''
import pygame

# Creates the Frame/Window for the visuals to go into


def start_screen():
    window_size = (1000, 600)
    pygame.init()
    pygame.display.set_caption("Chess Master Andy")  # Title for the Window
    screen = pygame.display.set_mode(window_size, 0, 32)
    # screen = pygame.display.set_mode(window_size,pygame.FULLSCREEN) For those who like living dangerously
    return screen
