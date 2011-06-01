#-*-coding:Utf-8 -*
# Auteur : Pierre Surply


import os

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

        self.partie = []
        
        
    def main(self):
        cmd = 1
        while cmd:
            cmd =  menu(self, "Menu principal", ["Nouvelle Partie", "Charger Partie", "Charger Niveau","Editeur de Niveaux", "Quitter"])
            
            if cmd == 1 or cmd == 2:
                if cmd == 1:
                    self.partie = self.nouvelle_partie(ask(self, "Nom de la partie : "))
                elif cmd == 2:
                    self.partie = self.charger_partie(ask(self, "Nom de la partie : "))
                
                i = self.partie[1]
                cmd = 1
                while open_map("save/{0}/map{1}".format(self.partie[0], i)) != [] and cmd == 1:
                    cmd = jeu(self, open_map("save/{0}/map{1}".format(self.partie[0], i)), self.partie[2], self.partie[3])
                    i = i+1

            elif cmd == 3:
                cmd = jeu(self, open_map("map/custom/" + ask(self, "Entrez le nom de la map :")))
                if cmd == 2:
                    cmd = menu(self, "Game Over", ["Rejouer", "Quitter"])
            elif cmd == 4:
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

    def nouvelle_partie(self, nom):
        partie = [nom, 1, -1, -1]
        i = 0
        if not os.path.isdir("data/save/{0}/".format(nom)):
            os.mkdir("data/save/{0}/".format(nom))
       
        while open_map("map/std/map{0}".format(i)) != []:
            save_map("save/{0}/map{1}".format(nom,i),open_map("map/std/map{0}".format(i)))
            i = i+1

        file = open("data/save/{0}/{0}".format(nom), "w")
        file.write("map=0\nposx=-1\nposy=-1\n")
        file.close()
        return partie

    def charger_partie(self, nom):
        partie = []
        partie.append(nom)
        try:
            file = open("data/save/{0}/{0}".format(nom))
            tampon = file.read()
            elements = tampon.split("\n")
            i = 1
            for element in elements:
                if element != "":
                    prop = element.split("=")
                    if prop[0] == "map" and i == 1:
                        partie.append(int(prop[1]))
                        i = i+1
                    elif prop[0] == "posx" and i == 2:
                        partie.append(int(prop[1]))
                        i = i+1
                    elif prop[0] == "posy" and i == 3:
                        partie.append(int(prop[1]))
                        i = i +1
            file.close()
                    
        except IOError:
            print (path + " : Partie introuvable !")

        return partie


    def save_partie(self):
        file = open("data/save/{0}/{0}".format(self.partie[0], "w"))
        
        tampon = "map={0}\n".format(self.partie[1])
        tampon = "posx={0}\n".format(self.partie[2])
        tampon = "posy={0}\n".format(self.partie[3])
        
        file.write(tampon)
        file.close()

        
            
        
        
        
        


        
        
        
        
