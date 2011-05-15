#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

from element import *
import const

# Pygame
import pygame
from pygame.locals import *


class Perso(Element):
    """ Personnnage principal """
    
    def __init__(self):
        Element.__init__(self)
        self.perso_d = pygame.image.load("img/perso_d.png").convert_alpha()
        self.perso_g = pygame.image.load("img/perso_g.png").convert_alpha()
        
        self.changer_image(self.perso_d)
        
