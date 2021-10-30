'''
Created on Oct 11, 2021

@author: Legacy
'''
import theMain
import pygame
import sys
import chess

# Path to images
IMAGES_PATH = './images'


# Sets up the Default Board
board = chess.Board()


# handles Setting up the Game and the Game State
def setupGameEngine(screen):
    # Lets Other Threads know the Game Engine is Ready. # @IgnorePep8
    theMain.init_complete = True
    print("GameEngine Running.")
    startGame(screen)


def startGame(screen):
    while not theMain.isClosed():
        screen.fill((255, 255, 255))  # Background Color
        createBoard(screen)
        # this provides clicking functionality for the future if we want it @IgnorePep8
        mx, my = pygame.mouse.get_pos()
        # this provides clicking functionality for the future if we want it @IgnorePep8
        m1_clicked = False
        # Event loop, This handles any button presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                theMain.close = True
                pygame.mixer.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # theMain.close = True
                    # this provides clicking functionality for the future if we want it @IgnorePep8
                    m1_clicked = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.quit()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def createBoard(screen):
    Boardimg = pygame.image.load(f'{IMAGES_PATH}/board.png')
    screen.blit(Boardimg, (100, 100))
    for i in range(8):
        for j in range(8):
            if board.piece_at((i*8)+j):
                screen.blit(convertToPng(board.piece_at((i*8)+j).symbol()),
                            (115 + j * 45, 115 + i * 45))  # @IgnorePep8


def changeBoard(newBoard):
    board = newBoard


def convertToPng(piece):
    if piece.isupper():
        return pygame.image.load(f"{IMAGES_PATH}/{piece}b.png")
    else:
        return pygame.image.load(f"{IMAGES_PATH}/{piece}w.png")
