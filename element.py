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

    def changer_image(self, path):
            self.image = path

    def changer_text(self, text, font):
        if isinstance(text, str):
            self.image = font.render(text, 1, (0,0,0))
        
