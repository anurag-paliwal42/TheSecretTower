#-*-coding:Utf-8 -*
# Auteur : Pierre Surply


import os
import random
import math
import copy

# Pygame
import pygame
from pygame.locals import *


# Element
from element import *

from menu import *
from jeu import *
from map import *
from editeur import *

# Constante
import const

class App:
    """ Classe définissant l'application The Secret Tower"""

    def __init__(self):
        """Initialisation de l'application"""

        # Initialisation de pygame
        pygame.init()
        
        # création de la fenetre
        self.size = [800, 600]
        self.fenetre = pygame.display.set_mode((self.size[0], self.size[1]), pygame.DOUBLEBUF)
        pygame.display.set_caption(const.fenetre_titre)

        # font
        self.font = pygame.font.Font("img/font.ttf", 20)
        self.font_petit = pygame.font.Font("img/font.ttf", 15)

        const.sprite_bloc = pygame.image.load("img/bloc.png").convert_alpha()
        const.sprite_lave = pygame.image.load("img/lave.png").convert_alpha()
        const.sprite_torch = pygame.image.load("img/torch.png").convert_alpha()
        const.sprite_perso = pygame.image.load("img/perso.png").convert_alpha()
        const.sprite_arm = pygame.image.load("img/arm_perso.png").convert_alpha()
        const.sprite_item = pygame.image.load("img/item.png").convert_alpha()
        const.sprite_mobs = pygame.image.load("img/mobs.png").convert_alpha()
        const.sprite_degats = pygame.image.load("img/degats.png").convert_alpha()
        const.vide = pygame.image.load("img/vide.png").convert_alpha()

        self.perso = Perso()
        self.partie = []
        self.coef = 2
        
        
    def main(self):
        cmd = 1
        while cmd:
            cmd =  menu(self, "Main Menu", ["New Game", "Load Game", "Load Level","Edit Level", "Quitter"])
            
            if cmd == 1 or cmd == 2:
                if cmd == 1:
                    self.perso = Perso()
                    self.partie = []
                    self.partie = self.nouvelle_partie(ask(self, "Nom de la partie : "))
                elif cmd == 2:
                    self.partie = self.charger_partie(ask(self, "Nom de la partie : "))
                
                self.perso.map = self.partie[1]
                self.perso.id = self.partie[2]
                cmd = 1
                while open_map("save/{0}/map{1}".format(self.partie[0], self.partie[1])) != [] and cmd == 1:
                    cmd = jeu(self, open_map("save/{0}/map{1}".format(self.partie[0], self.partie[1])), self.perso)
                    self.partie[1] = self.perso.map

            elif cmd == 3:
                self.partie = ["Gen", 0]
                self.perso.map = 0
                cmd = jeu(self, open_map("map/custom/" + ask(self, "Entrez le nom de la map :")), self.perso)
            elif cmd == 4:
                self.partie = ["Gen", 0]
                self.perso.map = 0
                cmd = menu(self, "Edit Level", ["New level", "Load level"])
                if cmd == 1:
                    cmd = editeur(self, [])
                elif cmd == 2:
                    cmd = editeur(self, open_map("map/custom/"+ask(self, "Entrez le nom de la map :")))

        pygame.quit()
        print "Merci d'avoir joué !"
        
    def blit(self, element):
        """Ajoute Element à l'écran"""
        if isinstance(element, Perso):
            if not element.sens:
                self.fenetre.blit(element.image, (element.x-(element.image.get_width()-50), element.y))
            else:
                self.fenetre.blit(element.image, (element.x,element.y))
        elif isinstance(element, Element):
            self.fenetre.blit(element.image, (element.x,element.y))
    
    def scale(self, coef):
        x = self.perso.x*coef-((800-50*coef)/2)
        y = self.perso.y*coef-((600-50*coef)/2)
        if x < 0:
            x=0
        if x+800 >800*coef:
            x = 800*coef-800
        if y < 0:
            y = 0
        if y+600 >600*coef:
            y = 600*coef-600

        self.fenetre.blit(pygame.transform.scale(self.fenetre, (800*coef, 600*coef)), (0,0), (x,y, 800, 600))
            

    def flip(self):
        """Rafraichissement"""
        """if self.size[0] != 800 or self.size[1] != 600:
            self.fenetre.blit(pygame.transform.scale(self.fenetre, (self.size[0], self.size[1])), (0,0))"""
        pygame.display.flip()

    def save_screen(self):
        return copy.copy(self.fenetre)

    def nouvelle_partie(self, nom):
        partie = [nom, 0, 0]
        # Copie map std
        i = 0
        if not os.path.isdir("data/save/{0}/".format(nom)):
            os.mkdir("data/save/{0}/".format(nom))
       
        while open_map("map/std/map{0}".format(i)) != []:
            save_map("save/{0}/map{1}".format(nom,i),open_map("map/std/map{0}".format(i)))
            i = i+1

        # Génération sous-sol
        map = []
        bloc = Porte(0, 2, 2, 0)
        bloc.move_el(0,50)
        map.append(bloc)
        xd = random.randint(0, 16)
        yd = random.randint(0, 12)
        size = random.randint(2,5)
        for x in range(16):
            bloc = Bloc(5)
            bloc.move_el(x*50, 0)
            map.append(bloc)

        for x in range(12):
            bloc = Terre(7)
            bloc.move_el(x*50+4*50, 50)
            map.append(bloc)
        for x in range(16):
            for y in range(10):
                if (random.randint(0, 10)) < 2:
                    rand = random.randint(0,5)
                    if rand < 2:
                        bloc = Coal(14)
                    elif rand == 2:
                        bloc = Copper(15)
                    else:
                        bloc = Stone(1)
                    bloc.move_el(x*50, y*50+100)
                    map.append(bloc)
                elif math.fabs(xd-x)+math.fabs(yd-y) > size:
                    bloc = Terre(7)
                    bloc.move_el(x*50, y*50+100)
                    map.append(bloc)

        save_map("save/{0}/map-1".format(nom), map)
        # Fichier global
        file = open("data/save/{0}/{0}".format(nom), "w")
        file.write("map=0\nid=0\n")
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
                    elif prop[0] == "id" and i == 2:
                        partie.append(int(prop[1]))
                        i = i +1
            file.close()
                    
        except IOError:
            print (path + " : Partie introuvable !")

        return partie


    def save_partie(self):
        file = open("data/save/{0}/{0}".format(self.partie[0]), "w")
        
        tampon = "map={0}\n".format(self.partie[1])
        tampon = tampon +"id={0}\n".format(self.partie[2])
        
        file.write(tampon)
        file.close()

    def set_size(self,new_size):
        self.size = new_size
        print new_size
        print self.size
        self.fenetre = pygame.display.set_mode((self.size[0], self.size[1]), pygame.RESIZABLE)
