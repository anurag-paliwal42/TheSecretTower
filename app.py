#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

# Pygame
import pygame
from pygame.locals import *


# Element
from element import *

from menu import *
from jeu import *
from map import *
from editeur import *

# Constantes
import const

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
        
        
    def main(self):
        cmd = 1
        while cmd:
            cmd =  menu(self, "Menu principal", ["Nouvelle Partie", "Charger Partie", "Editeur de map", "Quitter"])
            
            if cmd == 1:
                i = 0
                while open_map("map{0}".format(i)) != [] and cmd == 1:
                    cmd = jeu(self, open_map("map{0}".format(i)))
                    i = i+1
                
            elif cmd == 2:
                cmd = jeu(self, open_map(ask(self, "Entrez le nom de la map :")))
                if cmd == 2:
                    cmd = menu(self, "Game Over", ["Rejouer", "Quitter"])
            elif cmd == 3:
                cmd = menu(self, "Editeur de map", ["Nouvelle map", "Charger map"])
                if cmd == 1:
                    cmd = editeur(self, [])
                elif cmd == 2:
                    cmd = editeur(self, open_map(ask(self, "Entrez le nom de la map :")))

        pygame.quit()
        
    def blit(self, element):
        """Ajoute Element à l'écran"""
        if isinstance(element, Element):
            self.fenetre.blit(element.image, (element.x,element.y))
            

    def flip(self):
        """Rafraichissement"""
        pygame.display.flip()


        
        
        
        
