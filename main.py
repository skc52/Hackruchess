
import sys
import pygame
from Global import *
from Board import Board
pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption("CHESS")
MOUSEPOSX = -100
MOUSEPOSY = -100
DIRECTION = 0
UP = 0
SKEWED = 0
TIMES = 1
BLOCKED = 0
ROOKIEBEHAVIOR = 0
DOUBLEJUMP = False
QUIT = False


# instantiate chess board
board = Board(100, 20, 600, screen)



print("HELLO PLAYER")
while QUIT == False:




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            board.saveGame()
            QUIT = True
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if pygame.mouse.get_pos()[0] < 100 or pygame.mouse.get_pos()[0] > 700 or pygame.mouse.get_pos()[1] < 20 or pygame.mouse.get_pos()[1] > 620:
                MOUSEPOSX = -100
                MOUSEPOSY = -100

            else:
                [MOUSEPOSX, MOUSEPOSY] = pygame.mouse.get_pos()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                UP =1
                if MOUSEPOSY != -100:
                    board.updatePiecePosition(UP, DIRECTION, TIMES, SKEWED, ROOKIEBEHAVIOR, DOUBLEJUMP)

            if event.key == pygame.K_DOWN:
                UP = -1
                if MOUSEPOSY != -100:
                    board.updatePiecePosition(UP, DIRECTION, TIMES, SKEWED, ROOKIEBEHAVIOR, DOUBLEJUMP)

            if event.key == pygame.K_d: # for rook's movement only
                DIRECTION = 1
                ROOKIEBEHAVIOR = 1
                if MOUSEPOSY != -100:
                    board.updatePiecePosition(UP, DIRECTION, TIMES, SKEWED, ROOKIEBEHAVIOR, DOUBLEJUMP)

            if event.key == pygame.K_a: # for rook's movement only
                DIRECTION = -1
                ROOKIEBEHAVIOR = 1
                if MOUSEPOSY != -100:
                    board.updatePiecePosition(UP, DIRECTION, TIMES, SKEWED, ROOKIEBEHAVIOR, DOUBLEJUMP)

            if event.key == pygame.K_w: # for rook's movement only
                UP = 1
                ROOKIEBEHAVIOR = 1
                if MOUSEPOSY != -100:
                    board.updatePiecePosition(UP, DIRECTION, TIMES, SKEWED, ROOKIEBEHAVIOR, DOUBLEJUMP)

            if event.key == pygame.K_s: # for rook's movement only
                UP = -1
                ROOKIEBEHAVIOR = 1
                if MOUSEPOSY != -100:
                    board.updatePiecePosition(UP, DIRECTION, TIMES, SKEWED, ROOKIEBEHAVIOR, DOUBLEJUMP)

            if event.key == pygame.K_z:
                board.undo()

            if event.key == pygame.K_x:
                board.redo()

            if event.key == pygame.K_1:
                TIMES = 1
            if event.key == pygame.K_2:
                TIMES = 2
            if event.key == pygame.K_3:
                TIMES = 3
            if event.key == pygame.K_4:
                TIMES = 4
            if event.key == pygame.K_5:
                TIMES = 5
            if event.key == pygame.K_6:
                TIMES = 6
            if event.key == pygame.K_7:
                TIMES = 7
            if event.key == pygame.K_8:
                TIMES = 8
            if event.key == pygame.K_9:
                TIMES = 9


            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_LEFT]:
                DIRECTION = -1

            if pressed_keys[pygame.K_r]:
                board.restartgame()

            if pressed_keys[pygame.K_RIGHT]:
                DIRECTION = 1
            if pressed_keys[pygame.K_SPACE]:
                SKEWED = 1
            if pressed_keys[pygame.K_LSHIFT]:
                DOUBLEJUMP = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                DIRECTION = 0

            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                UP =0

            if event.key == pygame.K_SPACE:
                SKEWED = 0

            if event.key == pygame.K_LSHIFT:
                DOUBLEJUMP = False

            if event.key == pygame.K_a or event.key == pygame.K_d:
                DIRECTION = 0
                ROOKIEBEHAVIOR = 0

            if event.key == pygame.K_w or event.key == pygame.K_s:
                UP = 0
                ROOKIEBEHAVIOR = 0

    # the following three lines of code should always be in last for the sake of convenience for me
    screen.fill(white)
    board.drawBoard(MOUSEPOSX, MOUSEPOSY)
    board.showTurn(30,10)
    pygame.display.flip()

    if board.gameOver() == True:
        QUIT = True


