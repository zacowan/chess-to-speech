'''
Created on Oct 11, 2021

@author: Legacy
'''
import sys
import pygame
import chess

from . import the_main

# Path to images
IMAGES_PATH = './images'
isMicOn = False
isGameStarted = False

# Sets up the Default Board
#board = chess.Board('r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4')
board = None

# handles Setting up the Game and the Game State
def setup_game_engine(screen):
    # Lets Other Threads know the Game Engine is Ready. # @IgnorePep8
    the_main.init_complete = True
    print("GameEngine Running.")
    start_game(screen)


def start_game(screen):
    while not the_main.is_closed():
        screen.fill((255, 255, 255))  # Background Color
        mic_img=None
        if isMicOn:
            mic_img = pygame.image.load(f'{IMAGES_PATH}/MicOn2.png')
        else:
            mic_img = pygame.image.load(f'{IMAGES_PATH}/MicOff2.png')
        if isGameStarted:
            create_board(screen)
            screen.blit(mic_img, (300, 500))
        else:
            welcome_img = pygame.image.load(f'{IMAGES_PATH}/Welcome.png')
            screen.blit(welcome_img, (350, 200))
            screen.blit(mic_img, (400, 500))
        #draw mic
        # this provides clicking functionality for the future if we want it @IgnorePep8
        mx, my = pygame.mouse.get_pos()
        # this provides clicking functionality for the future if we want it @IgnorePep8
        m1_clicked = False
        # Event loop, This handles any button presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                the_main.close = True
                pygame.mixer.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # the_main.close = True
                    # this provides clicking functionality for the future if we want it @IgnorePep8
                    m1_clicked = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.quit()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def create_board(screen):
    board_img = pygame.image.load(f'{IMAGES_PATH}/board.png')
    screen.blit(board_img, (200, 75))
    for i in range(8):
        for j in range(8):
            if board.piece_at((i*8)+j):
                screen.blit(convert_to_png(board.piece_at((i*8)+j).symbol()),
                            (215 + j * 45, 95 + i * 45))  # @IgnorePep8


def change_board(newBoard):
    global board
    board = newBoard


def convert_to_png(piece):
    if piece.isupper():
        return pygame.image.load(f"{IMAGES_PATH}/{piece}b.png")
    else:
        return pygame.image.load(f"{IMAGES_PATH}/{piece}w.png")
