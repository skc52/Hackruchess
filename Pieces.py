import pygame

class Pieces:

    def __init__(self, team, imgname, x, y, screen):
        self.team = team
        self.imgname = imgname
        self.posX = x
        self.posY = y
        self.screen = screen

    def displayPiece(self):
        image = pygame.image.load("images/" + self.imgname)
        self.screen.blit(image, (self.posX, self.posY))
