'''
Created on Oct 11, 2021

@author: Legacy
'''
import sys
import pygame
import chess
from . import audio_detection
from . import the_main

# Path to images
IMAGES_PATH = './images'
isMicOn = False
isGameStarted = False
lastSaid =""
user_is_black=False
is_game_over = False
move_history=[]
#move_history=["User: Pawn in A2 to Captures Knight in A4", "Andy: Pawn in A7 to A5", "User: Pawn in B2 to B4", "Andy: Pawn in B7 to B5"]
# Sets up the Default Board
#board = chess.Board('rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1')
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
        pygame.font.init()
        myfont = pygame.font.SysFont('Times', 22)
        if isMicOn:
            mic_img = pygame.image.load(f'{IMAGES_PATH}/MicOn2.png')
        else:
            mic_img = pygame.image.load(f'{IMAGES_PATH}/MicOff2.png')
        if isGameStarted:
            textsurface = myfont.render("Your Session ID: " +audio_detection.SESSION_ID[0:8], True, (0, 0, 0))
            screen.blit(textsurface,(255,25))
            textsurface = myfont.render("Move History: ", True, (0, 0, 0))
            screen.blit(textsurface,(675,25))
            create_board(screen)
            screen.blit(mic_img, (250, 500))
            if is_game_over:
                game_over = pygame.image.load(f'{IMAGES_PATH}/DemoOver.png')
                screen.blit(game_over, (0, 0))
            if lastSaid:
                stringPrint =""
                lineNum=0
                for word in  ("I understood: "+lastSaid).split():
                    if(len(stringPrint+word)>40):
                        textsurface = myfont.render(stringPrint, True, (0, 0, 0))
                        screen.blit(textsurface,(575,475+lineNum))
                        lineNum+=25
                        stringPrint =""
                    stringPrint += word+ " "
                textsurface = myfont.render(stringPrint, True, (0, 0, 0))
                screen.blit(textsurface,(575,475+lineNum))
            if move_history:
                stringPrint =""
                lineNum=0
                for sentence in move_history:
                    if lineNum > 375:
                        break
                    for word in  (sentence).split():
                        if(len(stringPrint+word)>40):
                            textsurface = myfont.render(stringPrint, True, (0, 0, 0))
                            screen.blit(textsurface,(575,50+lineNum))
                            lineNum+=25
                            stringPrint =""
                        stringPrint += word+ " "
                        if lineNum> 375:
                            break
                    textsurface = myfont.render(stringPrint, True, (0, 0, 0))
                    screen.blit(textsurface,(575,50+lineNum))
                    lineNum+=25
                    stringPrint = ""
                    stringPrint ="-"*50
                    textsurface = myfont.render(stringPrint, True, (0, 0, 0))
                    screen.blit(textsurface,(575,50+lineNum-13))
                    stringPrint = ""

        else:
            welcome_img = pygame.image.load(f'{IMAGES_PATH}/Welcome.png')
            screen.blit(welcome_img, (350, 175))
            screen.blit(mic_img, (400, 500))
            textsurface = myfont.render("Your Session ID: " +audio_detection.SESSION_ID[0:8], True, (0, 0, 0))
            screen.blit(textsurface,(375,25))
        
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


    if not user_is_black:
        board_img = pygame.image.load(f'{IMAGES_PATH}/board.png')
        screen.blit(board_img, (150, 75))
        for i in range(8):
            for j in range(8):
                if board.piece_at((i*8)+j):
                    screen.blit(convert_to_png(board.piece_at((i*8)+j).symbol()),
                                (165 + j * 45, 405 - i * 45))  # @IgnorePep8
    else:
        board_img = pygame.image.load(f'{IMAGES_PATH}/board2.png')
        #board_img = pygame.transform.flip(board_img, True, True)
        screen.blit(board_img, (150, 75))
        for i in range(8):
            for j in range(8):
                if board.piece_at((i*8)+j):
                    screen.blit(convert_to_png(board.piece_at((i*8)+j).symbol()),
                                (480 - j * 45, 90 + i * 45))  # @IgnorePep8


def change_board(newBoard):
    global board
    board = newBoard


def convert_to_png(piece):
    if piece.isupper():
        return pygame.image.load(f"{IMAGES_PATH}/{piece}w.png")
    else:
        return pygame.image.load(f"{IMAGES_PATH}/{piece}b.png")

