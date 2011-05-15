#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

# Pygame
import pygame
from pygame.locals import *

# Constantes
import const

from element import *

class App:
    """ Classe définissant l'application The Secret of Tower"""

    def __init__(self):
        """Initialisation de l'application"""

        # Initialisation de pygame
        pygame.init()
        
        # création de la fenetre
        self.fenetre = pygame.display.set_mode((const.fenetre_size_x, const.fenetre_size_y))
        pygame.display.set_caption(const.fenetre_titre)

        # font
        self.font = pygame.font.Font(None, 30)
        
        
    def blit(self, element):
        """Ajoute Element à l'écran"""
        if isinstance(element, Element):
            self.fenetre.blit(element.image, (element.x, element.y))
            

    def flip(self):
        """Rafraichissement"""
        pygame.display.flip()


        
        
        
        
