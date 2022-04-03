from collections import deque
from Global import *

import pygame
from Pieces import Pieces
from Databasechess import Database, DatabaseTurn

stackOfPieces = deque()
stackOfKilled = deque()
stackOfMoves = deque()

redostackOfPieces = deque()
redostackOfKilled = deque()
redostackOfMoves = deque()

stackForCastling = deque()

# remember the positions of the pieces
db = Database("chess.db")

# remember the turn
dbCount = DatabaseTurn()

class Board:

    def __init__(self, startX, startY, length, screen):
        self.startX = startX
        self.startY = startY
        self.length = length
        self.alphabetName = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.numericName = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.squareX = -1
        self.squareY = -1
        self.turn = 0
        self.blocked = 0
        self.bkingPos = [0, 4]
        self.wkingPos = [7, 4]
        self.screen = screen

        db.sql_table()
        dbCount.sql_table()
        if db.doesDataExist() == False:
            print("False")
            self.positions = [
                ["br", "bk", "bb", "bq", "bking", "bb", "bk", "br"],
                ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                ["wr", "wk", "wb", "wq", "wking", "wb", "wk", "wr"]
            ]

        elif db.doesDataExist() == True:
            # print("Here")
            self.turn = dbCount.sql_fetch_count()

            self.positions = []

            for row in db.sql_fetch():
                row = list(row)
                del row[0]
                self.positions.append(row)


    def showTurn(self, X, Y):
        if self.turn %2 == 0:
            who = "White"
        else:
            who = "black"
        font = pygame.font.Font("freesansbold.ttf", 20)
        text = font.render(who, True, black, white)
        textRect = text.get_rect()
        textRect.center = (X, Y)
        self.screen.blit(text, textRect)


    def drawBoard(self, MOUSEPOSX, MOUSEPOSY):

        widOfSmallRect = self.length / 8

        for i in range(0, 9):
            updatedStartX = self.startX + (widOfSmallRect * i)
            updatedStartY = self.startY + (widOfSmallRect * i)

            # draw vertical line
            pygame.draw.line(self.screen, black, (updatedStartX, self.startY),
                             (updatedStartX, self.startY + self.length))
            # write name alphabetically
            if i > 0:
                self.nameBoxes(updatedStartX - widOfSmallRect / 2, self.startY / 2, self.alphabetName[i - 1])
            # draw horizontal line
            pygame.draw.line(self.screen, black, (self.startX, updatedStartY),
                             (self.startX + self.length, updatedStartY))
            # write name numerically
            if i < 8:
                self.nameBoxes(self.startX - 10, updatedStartY + widOfSmallRect / 2, self.numericName[8 - i - 1])

        # fills alternate boxes with color
        self.fillAlternate(self.startX, self.startY + widOfSmallRect * 7, widOfSmallRect)

        if 100 <= MOUSEPOSX <= 700 and 20 <= MOUSEPOSY <= 620:
            self.getClickedSquare(MOUSEPOSX, MOUSEPOSY)
        self.blitPieces(widOfSmallRect)

    def fillAlternate(self, x, y, widOFSmallRect):
        for i in self.numericName:
            if int(i) % 2 == 1:
                startX = x
            else:

                startX = x + widOFSmallRect
            for j in range(4):
                pygame.draw.rect(self.screen, gray, pygame.Rect(startX, y, widOFSmallRect, widOFSmallRect))
                startX = startX + widOFSmallRect * 2
            y = y - widOFSmallRect

    def blitPieces(self, widOfSmallRect):
        team = ""
        for i in range(len(self.positions)):
            for j in range(len(self.positions[i])):
                if self.positions[i][j] != "":
                    if self.positions[i][j][0] == "b":
                        team = "black"
                    elif self.positions[i][j][0] == "w":
                        team = "white"
                    pawn = Pieces(team, self.positions[i][j] + ".png", self.startX + widOfSmallRect * j,
                                  self.startY + widOfSmallRect * i, self.screen)
                    pawn.displayPiece()

    def getClickedSquare(self, MOUSEPOSX, MOUSEPOSY):
        widOfSmallRect = 75
        self.squareX = (MOUSEPOSX - self.startX) // widOfSmallRect
        self.squareY = (MOUSEPOSY - self.startY) // widOfSmallRect
        # set focus
        pygame.draw.rect(self.screen, highlight, pygame.Rect(self.startX + widOfSmallRect * self.squareX,
                                                             self.startY + widOfSmallRect * self.squareY,
                                                             widOfSmallRect, widOfSmallRect))

    def updatePiecePosition(self, UP, DIRECTION, TIMES, SKEWED, ROOKIEBEHAVIOR, DOUBLEJUMP):
        if self.positions[self.squareY][self.squareX] != "":
            if self.positions[self.squareY][self.squareX][-1] == "p":
                self.updatePawnPos(DIRECTION, DOUBLEJUMP)
            elif self.positions[self.squareY][self.squareX][-1] == "k":
                self.updateKnightPiece(UP, DIRECTION, SKEWED)
            elif self.positions[self.squareY][self.squareX][-1] == "b":
                self.updateBishopPiece("wb", "bb", DIRECTION, UP, TIMES)
            elif self.positions[self.squareY][self.squareX][-1] == "r":
                self.updateRookPiece("wr", "br", UP, DIRECTION, TIMES)
            elif self.positions[self.squareY][self.squareX][-1] == "q":
                self.updateQueenPiece(ROOKIEBEHAVIOR, DIRECTION, UP, TIMES)
            elif self.positions[self.squareY][self.squareX][-1] == "g":
                self.updateKingPiece(ROOKIEBEHAVIOR, DIRECTION, UP)

    def updatePawnPos(self, DIRECTION, DOUBLEJUMP):
        global noOfSteps

        if self.turn % 2 == 1:
            if self.positions[self.squareY][self.squareX][0] == "b":
                if DIRECTION == 0:
                    if DOUBLEJUMP and self.squareY == 1:
                        noOfSteps = 2
                    else:
                        noOfSteps = 1
                    if self.positions[self.squareY + noOfSteps][self.squareX] == "":
                        self.positions[self.squareY + noOfSteps][self.squareX] = "bp"
                        self.positions[self.squareY][self.squareX] = ""
                        stackOfPieces.append("bp")
                        stackOfKilled.append("")
                        stackOfMoves.append((self.squareX, self.squareY))
                        stackOfMoves.append((self.squareX, self.squareY + noOfSteps))
                        self.turn += 1

                else:
                    if (0 <= self.squareX + 1 * DIRECTION <= 7 and 0 <= self.squareY + 1 <= 7
                            and self.positions[self.squareY + 1][self.squareX + 1 * DIRECTION] != ""):
                        if self.positions[self.squareY + 1][self.squareX + 1 * DIRECTION][0] == "w":
                            stackOfKilled.append(self.positions[self.squareY + 1][self.squareX + 1 * DIRECTION])
                            self.positions[self.squareY + 1][self.squareX + 1 * DIRECTION] = "bp"
                            self.positions[self.squareY][self.squareX] = ""
                            stackOfPieces.append("bp")
                            stackOfMoves.append((self.squareX, self.squareY))
                            stackOfMoves.append((self.squareX + 1 * DIRECTION, self.squareY + 1))
                            self.turn += 1
        else:
            if self.positions[self.squareY][self.squareX][0] == "w":

                if DIRECTION == 0:
                    if DOUBLEJUMP and self.squareY == 6:
                        noOfSteps = 2
                    else:
                        noOfSteps = 1
                    if self.positions[self.squareY - noOfSteps][self.squareX] == "":
                        self.positions[self.squareY - noOfSteps][self.squareX] = "wp"
                        self.positions[self.squareY][self.squareX] = ""
                        stackOfPieces.append("wp")
                        stackOfKilled.append("")
                        stackOfMoves.append((self.squareX, self.squareY))
                        stackOfMoves.append((self.squareX, self.squareY - noOfSteps))
                        self.turn += 1
                else:
                    if (0 <= self.squareX + 1 * DIRECTION <= 7 and 0 <= self.squareY + 1 <= 7
                            and self.positions[self.squareY - 1][self.squareX + 1 * DIRECTION] != ""):
                        if self.positions[self.squareY - 1][self.squareX + 1 * DIRECTION][0] == "b":
                            stackOfKilled.append(self.positions[self.squareY - 1][self.squareX + 1 * DIRECTION])
                            self.positions[self.squareY - 1][self.squareX + 1 * DIRECTION] = "wp"
                            self.positions[self.squareY][self.squareX] = ""
                            stackOfPieces.append("wp")
                            stackOfMoves.append((self.squareX, self.squareY))
                            stackOfMoves.append((self.squareX + 1 * DIRECTION, self.squareY - 1))
                            self.turn += 1


    def undo(self):
        if stackOfMoves:
            (x, y) = stackOfMoves.pop()
            redostackOfMoves.append((x, y))

            self.positions[y][x] = stackOfKilled.pop()
            redostackOfKilled.append(self.positions[y][x])

            (x, y) = stackOfMoves.pop()
            redostackOfMoves.append((x, y))

            self.positions[y][x] = stackOfPieces.pop()
            redostackOfPieces.append(self.positions[y][x])

            self.turn -= 1

    def redo(self):
        if redostackOfMoves:
            (x, y) = redostackOfMoves.pop()
            stackOfMoves.append((x, y))
            self.positions[y][x] = redostackOfKilled.pop()
            stackOfKilled.append(self.positions[y][x])
            (x, y) = redostackOfMoves.pop()
            stackOfMoves.append((x, y))
            self.positions[y][x] = redostackOfPieces.pop()
            stackOfPieces.append(self.positions[y][x])
            self.turn += 1

    def updateKnightPiece(self, UP, DIRECTION, SKEWED):

        if DIRECTION == 1 or DIRECTION == -1:
            if SKEWED == 1:
                if self.turn % 2 == 1:
                    if 0 <= self.squareY + 1 * UP <= 7 and 0 <= self.squareX + 2 * DIRECTION <= 7:
                        if self.positions[self.squareY][self.squareX][0] == "b":
                            if (self.positions[self.squareY + 1 * UP][self.squareX + 2 * DIRECTION] == ""
                                    or self.positions[self.squareY + 1 * UP][self.squareX + 2 * DIRECTION][0] == "w"):
                                stackOfKilled.append(
                                    self.positions[self.squareY + 1 * UP][self.squareX + 2 * DIRECTION])
                                self.positions[self.squareY + 1 * UP][self.squareX + 2 * DIRECTION] = "bk"
                                self.positions[self.squareY][self.squareX] = ""
                                stackOfPieces.append("bk")
                                stackOfMoves.append((self.squareX, self.squareY))
                                stackOfMoves.append((self.squareX + 2 * DIRECTION, self.squareY + 1 * UP))
                                self.turn += 1
                else:
                    if 0 <= self.squareY - 1 * UP <= 7 and 0 <= self.squareX + 2 * DIRECTION <= 7:
                        if self.positions[self.squareY][self.squareX][0] == "w":
                            if (self.positions[self.squareY - 1 * UP][self.squareX + 2 * DIRECTION] == ""
                                    or self.positions[self.squareY - 1 * UP][self.squareX + 2 * DIRECTION][0] == "b"):
                                stackOfKilled.append(
                                    self.positions[self.squareY - 1 * UP][self.squareX + 2 * DIRECTION])
                                self.positions[self.squareY - 1 * UP][self.squareX + 2 * DIRECTION] = "wk"
                                self.positions[self.squareY][self.squareX] = ""
                                stackOfPieces.append("wk")
                                stackOfMoves.append((self.squareX, self.squareY))
                                stackOfMoves.append((self.squareX + 2 * DIRECTION, self.squareY - 1 * UP))
                                self.turn += 1
            else:
                if self.turn % 2 == 1:
                    if 0 <= self.squareY + 2 * UP <= 7 and 0 <= self.squareX + 1 * DIRECTION <= 7:
                        if self.positions[self.squareY][self.squareX][0] == "b":
                            if (self.positions[self.squareY + 2 * UP][self.squareX + 1 * DIRECTION] == ""
                                    or self.positions[self.squareY + 2 * UP][self.squareX + 1 * DIRECTION][0] == "w"):
                                stackOfKilled.append(
                                    self.positions[self.squareY + 2 * UP][self.squareX + 1 * DIRECTION])
                                self.positions[self.squareY + 2 * UP][self.squareX + 1 * DIRECTION] = "bk"
                                self.positions[self.squareY][self.squareX] = ""
                                stackOfPieces.append("bk")
                                stackOfMoves.append((self.squareX, self.squareY))
                                stackOfMoves.append((self.squareX + 1 * DIRECTION, self.squareY + 2 * UP))
                                self.turn += 1
                else:
                    if 0 <= self.squareY - 2 * UP <= 7 and 0 <= self.squareX + 1 * DIRECTION <= 7:
                        if self.positions[self.squareY][self.squareX][0] == "w":
                            if (self.positions[self.squareY - 2 * UP][self.squareX + 1 * DIRECTION] == ""
                                    or self.positions[self.squareY - 2 * UP][self.squareX + 1 * DIRECTION][0] == "b"):
                                stackOfKilled.append(
                                    self.positions[self.squareY - 2 * UP][self.squareX + 1 * DIRECTION])
                                self.positions[self.squareY - 2 * UP][self.squareX + 1 * DIRECTION] = "wk"
                                self.positions[self.squareY][self.squareX] = ""
                                stackOfPieces.append("wk")
                                stackOfMoves.append((self.squareX, self.squareY))
                                stackOfMoves.append((self.squareX + 1 * DIRECTION, self.squareY - 2 * UP))
                                self.turn += 1

    def updateBishopPiece(self, wb, bb, DIRECTION, UP, TIMES):

        if DIRECTION == 1 or DIRECTION == -1:
            steps = self.noOfAvailableStepsForBishop(UP, DIRECTION, TIMES)
            if TIMES <= steps:
                if self.turn % 2 == 1:
                    if 0 <= self.squareY + 1 * UP * TIMES <= 7 and 0 <= self.squareX + 1 * DIRECTION * TIMES <= 7:

                        if self.positions[self.squareY][self.squareX][0] == "b":
                            if (self.positions[self.squareY + 1 * UP * TIMES][
                                self.squareX + 1 * DIRECTION * TIMES] == ""
                                    or
                                    self.positions[self.squareY + 1 * UP * TIMES][self.squareX + 1 * DIRECTION * TIMES][
                                        0] == "w"):
                                stackOfKilled.append(
                                    self.positions[self.squareY + 1 * UP * TIMES][self.squareX + 1 * DIRECTION * TIMES])
                                self.positions[self.squareY + 1 * UP * TIMES][self.squareX + 1 * DIRECTION * TIMES] = bb
                                if bb == "bking":
                                    self.bkingPos = [self.squareY + 1 * UP * TIMES,
                                                     self.squareX + 1 * DIRECTION * TIMES]
                                    if bb not in stackForCastling:
                                        stackForCastling.append(bb)
                                self.positions[self.squareY][self.squareX] = ""
                                stackOfPieces.append(bb)
                                stackOfMoves.append((self.squareX, self.squareY))
                                stackOfMoves.append(
                                    (self.squareX + 1 * DIRECTION * TIMES, self.squareY + 1 * UP * TIMES))
                                self.turn += 1
                else:
                    if 0 <= self.squareY - 1 * UP * TIMES <= 7 and 0 <= self.squareX + 1 * DIRECTION * TIMES <= 7:
                        if self.positions[self.squareY][self.squareX][0] == "w":
                            if (self.positions[self.squareY - 1 * UP * TIMES][
                                self.squareX + 1 * DIRECTION * TIMES] == ""
                                    or
                                    self.positions[self.squareY - 1 * UP * TIMES][self.squareX + 1 * DIRECTION * TIMES][
                                        0] == "b"):
                                stackOfKilled.append(
                                    self.positions[self.squareY - 1 * UP * TIMES][self.squareX + 1 * DIRECTION * TIMES])
                                self.positions[self.squareY - 1 * UP * TIMES][self.squareX + 1 * DIRECTION * TIMES] = wb
                                if wb == "wking":
                                    self.wkingPos = [self.squareY - 1 * UP * TIMES,
                                                     self.squareX + 1 * DIRECTION * TIMES]
                                    if wb not in stackForCastling:
                                        stackForCastling.append(wb)
                                self.positions[self.squareY][self.squareX] = ""
                                stackOfPieces.append(wb)
                                stackOfMoves.append((self.squareX, self.squareY))
                                stackOfMoves.append(
                                    (self.squareX + 1 * DIRECTION * TIMES, self.squareY - 1 * UP * TIMES))
                                self.turn += 1

    def noOfAvailableStepsForBishop(self, UP, DIRECTION, TIMES):
        availableSteps = 0

        if self.turn % 2 == 1:
            if 0 <= self.squareY + UP * TIMES <= 7 and 0 <= self.squareX + DIRECTION * TIMES <= 7:
                while availableSteps < TIMES:
                    if self.positions[self.squareY + UP + (UP * availableSteps)][
                        self.squareX + DIRECTION + (DIRECTION * availableSteps)] == "":
                        availableSteps += 1
                    else:
                        if self.positions[self.squareY + UP + (UP * availableSteps)][
                            self.squareX + DIRECTION + (DIRECTION * availableSteps)][0] == "w":
                            availableSteps += 1
                        print(availableSteps)
                        return availableSteps
            else:
                print("Cannot go outside the board")
        else:
            if 0 <= self.squareY - UP * TIMES <= 7 and 0 <= self.squareX + DIRECTION * TIMES <= 7:

                while availableSteps < TIMES:

                    if self.positions[self.squareY - UP - (UP * availableSteps)][
                        self.squareX + DIRECTION + (DIRECTION * availableSteps)] == "":
                        availableSteps += 1
                    else:
                        if self.positions[self.squareY - UP - (UP * availableSteps)][
                            self.squareX + DIRECTION + (DIRECTION * availableSteps)][0] == "b":
                            availableSteps += 1
                        print(availableSteps)
                        return availableSteps
            else:
                print("Cannot go outside the board")

        print(availableSteps)
        return availableSteps

    def updateRookPiece(self, wr, br, UP, DIRECTION, TIMES):
        steps = self.noOfAvailableStepsRook(UP, DIRECTION, TIMES)
        if TIMES <= steps:
            if self.turn % 2 == 1:
                if self.positions[self.squareY][self.squareX][0] == "b":
                    if DIRECTION != 0:
                        if 0 <= self.squareX + DIRECTION * TIMES <= 7:
                            if (self.positions[self.squareY][self.squareX + DIRECTION * TIMES] == ""
                                    or self.positions[self.squareY][self.squareX + DIRECTION * TIMES][0] == "w"):
                                stackOfKilled.append(self.positions[self.squareY][self.squareX + DIRECTION * TIMES])
                                self.positions[self.squareY][self.squareX + DIRECTION * TIMES] = br
                                if br == "bking":
                                    self.bkingPos = [self.squareY, self.squareX + DIRECTION * TIMES]
                                    if br not in stackForCastling:
                                        stackForCastling.append(br)
                                self.positions[self.squareY][self.squareX] = ""
                                stackOfPieces.append(br)
                                stackOfMoves.append((self.squareX, self.squareY))
                                stackOfMoves.append((self.squareX + DIRECTION * TIMES, self.squareY))

                                self.turn += 1
                            else:
                                print("Cannot kill same team")
                        else:
                            print("Cannot go beyond")

                    if UP != 0:
                        if 0 <= self.squareY + UP * TIMES <= 7:
                            if (self.positions[self.squareY + UP * TIMES][self.squareX] == ""
                                    or self.positions[self.squareY + UP * TIMES][self.squareX][0] == "w"):
                                stackOfKilled.append(self.positions[self.squareY + UP * TIMES][self.squareX])
                                self.positions[self.squareY + UP * TIMES][self.squareX] = br
                                if br == "bking":
                                    self.bkingPos = [self.squareY + UP * TIMES, self.squareX]
                                    if br not in stackForCastling:
                                        stackForCastling.append(br)
                                self.positions[self.squareY][self.squareX] = ""
                                stackOfPieces.append(br)
                                stackOfMoves.append((self.squareX, self.squareY))
                                stackOfMoves.append((self.squareX, self.squareY + UP * TIMES))
                                self.turn += 1
                            else:
                                print("Cannot kill same team")
                        else:
                            print("Cannot go beyond")

            else:
                if self.positions[self.squareY][self.squareX][0] == "w":
                    if DIRECTION != 0:
                        if 0 <= self.squareX + DIRECTION * TIMES <= 7:
                            if (self.positions[self.squareY][self.squareX + DIRECTION * TIMES] == ""
                                    or self.positions[self.squareY][self.squareX + DIRECTION * TIMES][0] == "b"):
                                stackOfKilled.append(self.positions[self.squareY][self.squareX + DIRECTION * TIMES])
                                self.positions[self.squareY][self.squareX + DIRECTION * TIMES] = wr
                                if wr == "wking":
                                    self.wkingPos = [self.squareY, self.squareX + DIRECTION * TIMES]
                                    if wr not in stackForCastling:
                                        stackForCastling.append(wr)
                                self.positions[self.squareY][self.squareX] = ""
                                stackOfPieces.append(wr)
                                stackOfMoves.append((self.squareX, self.squareY))
                                stackOfMoves.append((self.squareX + DIRECTION * TIMES, self.squareY))
                                self.turn += 1
                            else:
                                print("Cannot kill same team")
                        else:
                            print("Cannot go beyond")

                    if UP != 0:
                        if 0 <= self.squareY - UP * TIMES <= 7:
                            if (self.positions[self.squareY - UP * TIMES][self.squareX] == ""
                                    or self.positions[self.squareY - UP * TIMES][self.squareX][0] == "b"):
                                stackOfKilled.append(self.positions[self.squareY - UP * TIMES][self.squareX])
                                self.positions[self.squareY - UP * TIMES][self.squareX] = wr
                                if wr == "wking":
                                    self.wkingPos = [self.squareY - UP * TIMES, self.squareX]
                                    if wr not in stackForCastling:
                                        stackForCastling.append(wr)
                                self.positions[self.squareY][self.squareX] = ""
                                stackOfPieces.append(wr)
                                stackOfMoves.append((self.squareX, self.squareY))
                                stackOfMoves.append((self.squareX, self.squareY - UP * TIMES))
                                self.turn += 1
                            else:
                                print("Cannot kill same team")
                        else:
                            print("Cannot go beyond")

    def noOfAvailableStepsRook(self, UP, DIRECTION, TIMES):
        availableSteps = 0
        if self.turn % 2 == 1:
            if UP != 0:
                if 0 <= self.squareY + UP * TIMES <= 7:
                    while availableSteps < TIMES:
                        if self.positions[self.squareY + UP + UP * availableSteps][self.squareX] == "":
                            availableSteps += 1
                        else:
                            if self.positions[self.squareY + UP + UP * availableSteps][self.squareX][0] == "w":
                                availableSteps += 1
                            print(availableSteps)
                            return availableSteps
            if DIRECTION != 0:
                if 0 <= self.squareX + DIRECTION * TIMES <= 7:
                    while availableSteps < TIMES:
                        if self.positions[self.squareY][self.squareX + DIRECTION + DIRECTION * availableSteps] == "":
                            availableSteps += 1
                        else:
                            if self.positions[self.squareY][self.squareX + DIRECTION + DIRECTION * availableSteps][
                                0] == "w":
                                availableSteps += 1
                            print(availableSteps)
                            return availableSteps

        else:
            if UP != 0:
                if 0 <= self.squareY - UP * TIMES <= 7:
                    while availableSteps < TIMES:
                        if self.positions[self.squareY - UP - UP * availableSteps][self.squareX] == "":
                            availableSteps += 1
                        else:
                            if self.positions[self.squareY - UP - UP * availableSteps][self.squareX][0] == "b":
                                availableSteps += 1
                            print(availableSteps)
                            return availableSteps
            if DIRECTION != 0:
                if 0 <= self.squareX + DIRECTION * TIMES <= 7:
                    while availableSteps < TIMES:
                        if self.positions[self.squareY][self.squareX + DIRECTION + DIRECTION * availableSteps] == "":
                            availableSteps += 1
                        else:
                            if self.positions[self.squareY][self.squareX + DIRECTION + DIRECTION * availableSteps][
                                0] == "b":
                                availableSteps += 1
                            print(availableSteps)
                            return availableSteps

        print(availableSteps)
        return availableSteps

    def updateQueenPiece(self, ROOKIEBEHAVIOR, DIRECTION, UP, TIMES):
        if ROOKIEBEHAVIOR == 0:
            self.updateBishopPiece("wq", "bq", DIRECTION, UP, TIMES)
        else:
            self.updateRookPiece("wq", "bq", UP, DIRECTION, TIMES)

    def updateKingPiece(self, ROOKIEBEHAVIOR, DIRECTION, UP):

        if ROOKIEBEHAVIOR == 0:
            self.updateBishopPiece("wking", "bking", DIRECTION, UP, 1)
        else:
            self.updateRookPiece("wking", "bking", UP, DIRECTION, 1)

    def nameBoxes(self, centerX, centerY, letter):
        font = pygame.font.Font("freesansbold.ttf", 20)
        text = font.render(letter, True, black, white)
        textRect = text.get_rect()
        textRect.center = (centerX, centerY)
        self.screen.blit(text, textRect)

    def gameOver(self):

        if "wking" in stackOfKilled:
            print("Black wins")
            # sql_delete(self.con)
            self.restartgame()
            self.saveGame()
            return True
        elif "bking" in stackOfKilled:
            print("White wins")
            # sql_delete(self.con)
            self.restartgame()
            self.saveGame()
            return True

        return False

    def saveGame(self):

        db.sql_delete()
        dbCount.sql_delete()
        dbCount.sql_insert((0,self.turn))
        for i in range(len(self.positions)):
            row = self.positions[i]
            row.insert(0, i)
            db.sql_insert(row)


    def restartgame(self):
        self.positions = [
            ["br", "bk", "bb", "bq", "bking", "bb", "bk", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wk", "wb", "wq", "wking", "wb", "wk", "wr"]
        ]
        stackOfMoves.clear()
        redostackOfMoves.clear()
        self.turn = 0
