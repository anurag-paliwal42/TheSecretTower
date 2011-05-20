#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

from element import *
from bloc import *
import const

from time import *

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

        # Propriétés
        self.vie = 3
        self.last_dommage = time()

        # Gravité
        self.v_y = 0
        self.v_x = 0
        self.isingrav = True
    

    def subir_degats(self, degat):
        if (self.vie > 0 and time()-self.last_dommage > 1):
            self.last_dommage = time()
            self.vie = self.vie - 1
            self.sauter(3, -10, True)
            return True
        if (self.vie <= 0):
            return False


    ################### Moteur Physique ###################

    # Faire subir au perso les lois de gravitations
    # map : liste contenant les elements de la map
    def tomber(self, map):
        if self.y < 550 or self.v_y < 0:
           if self.move(self.v_x, self.v_y, map):
               if self.v_y <> 0:
                   self.isingrav = True
               self.v_y = self.v_y + 1


           else:
               self.isingrav = False
               self.v_y = 0
               self.v_x = 0

        else: 
            self.isingrav = False
    
    # Fait sauter notre personnage
    # x : vitesse en x
    # y : vitesse en y
    def sauter(self, x, y, force = False):
        if self.isingrav == False or force:
            self.v_y = y
            self.v_x = x
            self.isingrav = True

    # Déplacer le personnage avec collision
    # x : deplacement en x
    # y : deplacement en y
    #
    # Retour :
    #     True : Deplacement effectué (peut etre modifié)
    #     False : Deplacement non effectué (collision)
    def move(self, x, y, map):
        if self.collided_map(x, y, map) == False:
            if self.y+y < 550: 
                self.move_el(0,y)
            else:
                self.move_el(0, 550-self.y)
                
            if self.x + x > 0 and self.x +x < 750:
                self.move_el(x,0)
                if x > 0:
                    self.changer_image(self.perso_d)
                elif x < 0:
                    self.changer_image(self.perso_g)
            return True
        
        elif self.collided_map(0, y, map) == False:
            if self.y+y < 550: 
                self.move_el(0,y)
            else:
                self.move_el(0, 550-self.y)
            return True
        else:
            return False
             

    # Test la collision du perso avec la map (avant deplacement)
    # dep_x : deplacement en x
    # dep_y : deplacement en y
    # map : liste contenant les élements de la map
    #
    # Retour :
    #     True : Collision
    #     False : Pas de collision
    def collided_map(self, dep_x, dep_y, map):
        future_rect = pygame.Rect(self.rect)
        future_rect = future_rect.move(dep_x, dep_y)
        # Vérification pour chaques éléments de la map
        for i in map:
            if future_rect.colliderect(i.rect):
 
                # Vérif bloc mouvant
                if isinstance(i, BlocMouvant):
                    # Vérif position
                    if (self.y-dep_y) <= i.y-50:
                        if i.aller:
                            if i.x < i.dep_x+i.debut_x:
                                self.move(1,0, map)
           
                        else:
                            if i.x > i.debut_x:
                                self.move(-1,0, map)
                            if i.y > i.debut_y:
                                self.move(0,-1, map)
                        return True
                    else:
                        return False
                elif isinstance(i, BlocDisp):
                    if (i.etat):
                        return True
                    return False
                elif isinstance(i, BlocDanger):
                    self.subir_degats(i.atk)
                    return True
                else:
                    return True
            
        return False



            
        
        
