#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

# Pygame
import pygame
from pygame.locals import *

class Element:
    """ Définit l'élément de base de la fentre """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.rect = None

    def changer_image(self, src):
        self.image = src
        if self.rect == None:
            self.rect = self.image.get_rect()

    def changer_text(self, text, font):
        if isinstance(text, str):
            self.image = font.render(text, 1, (0,0,0))
        if self.rect == None:
            self.rect = self.image.get_rect()

    def move_el(self, x, y):
        self.x = self.x+x
        self.y = self.y+y
        self.rect = self.rect.move(x,y)
        
            
        
