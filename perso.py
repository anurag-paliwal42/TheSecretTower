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

        # images perso
        self.perso_d = pygame.image.load("img/perso_d.png").convert_alpha()
        self.perso_g = pygame.image.load("img/perso_g.png").convert_alpha()
        
        # changer_image
        self.changer_image(self.perso_d)

        # Gravité
        self.v_y = 0
        self.isingrav = False
    
    def tomber(self):
        if self.y < 500 or self.v_y < 0:
            self.move_to_y(self.y + self.v_y)
            #self.y = self.y + self.v_y
            self.v_y = self.v_y + 1
        else:
            self.isingrav = False
            
    def sauter(self):
        if self.isingrav == False:
            self.v_y = self.v_y - 20
            self.isingrav = True

    def move_to_y(self, y):
        if y < 500:
            self.y = y
        else:
            self.y = 500
        
        
        
