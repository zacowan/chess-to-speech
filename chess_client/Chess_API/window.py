'''
Created on Oct 9, 2021

@author: Legacy
'''
import pygame


def startScreen():
    window_size = (1000, 600)
    pygame.init()
    pygame.display.set_caption("Chess Master Andy")
    screen = pygame.display.set_mode(window_size, 0, 32)
    return screen
