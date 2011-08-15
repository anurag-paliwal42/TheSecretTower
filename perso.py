#-*-coding:Utf-8 -*

#    TheSecretTower
#    Copyright (C) 2011 Pierre SURPLY
#
#    This file is part of TheSecretTower.
#
#    TheSecretTower is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    TheSecretTower is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with TheSecretTower.  If not, see <http://www.gnu.org/licenses/>.

# Auteur : Pierre Surply

from element import *
from bloc import *
from atelier import *
import const
from item import *

from time import *
import os
import copy
import math

# Pygame
import pygame
from pygame.locals import *


class Perso(Element):
    """ Personnnage principal """
    
    def __init__(self):
        Element.__init__(self)

        

        # Propriétés
        self.nom = "Unknown"

        self.map = 0
        self.id_porte = 0
        self.vie = 6
        self.last_dommage = time()
        self.last_dommage_ur = time()
        self.last_dommage_fire = time()
        self.last_hit = 0
        self.inv = Inventaire()
        item = Item(1, 1)
        self.inv.add(item)
        self.fired = False
        self.fired_time_stop = 0

        self.color = []

        # Multi-joueur
        self.ctrl = True
        self.hitting = False

        # changer_image

        self.sens = True
        self.changement = 0
        self.angle_arm = 0
        self.changement_angle = 0
        self.rang_image = 0
        self.set_org_color()
        self.anim(False)
        self.rect.width = 20
        self.rect.height = 40
        self.rect = self.rect.move(15, 10)


        # Gravité
        self.v_y = 0
        self.v_x = 0
        self.tend_x = 0
        self.isingrav = True
    

    def subir_degats(self, degat):
        if self.ctrl:
            if (self.vie > 0 and time()-self.last_dommage > 1):
                self.last_dommage = time()
                self.vie = self.vie - degat
                self.sauter(0,-5, True)
                return True
            if (self.vie <= 0):
                return False

    def anim(self, etat):

        image = copy.copy(const.vide)

        # Bras
        rect = pygame.Rect(0,0, 50,50)
        if self.inv.get_item().id%5 !=0 and self.inv.get_item().id < 30:
            rect = pygame.Rect((self.inv.get_item().id%5)*50-50,(self.inv.get_item().id/5)*50+50, 50,50)
        elif self.inv.get_item().id == 0:
            if self.inv.get_item().bloc.picture == 13:
                rect = pygame.Rect(50,0, 50,50)
        """if self.inv.get_item().id == 1:
            rect = pygame.Rect(0,50, 50,50)
        elif self.inv.get_item().id == 2:
            rect = pygame.Rect(50,50, 50,50)
        elif self.inv.get_item().id == 3:
            rect = pygame.Rect(100,50, 50,50)
        elif self.inv.get_item().id == 4:
            rect = pygame.Rect(150,50, 50,50)
        elif self.inv.get_item().id == 6:
            rect = pygame.Rect(150,50, 50,50)"""

        image.blit(self.sprite_arm, (0,0), rect)
        if self.angle_arm != 0:

            image = pygame.transform.rotate(image, self.angle_arm)
            if time() - self.changement_angle > 0.1:
                if self.angle_arm == 70:
                    self.angle_arm = -70
                else:
                    self.angle_arm = 0
                self.changement_angle = time()


        # fire
        if self.fired:
            rect = pygame.Rect(0,random.randint(0, 3)*50, 50,50)
            image.blit(const.sprite_fire, (0,0), rect)
        # corps
        rect = pygame.Rect(self.rang_image*50,0, 50,50)
        if time() - self.changement > 0.1 and etat and not self.isingrav:
            self.changement = time()
            if self.rang_image < 2:
                self.rang_image += 1
            else:
                self.rang_image = 0
            rect = pygame.Rect(self.rang_image*50,0, 50,50)
        elif not etat:
            rect = pygame.Rect(0,0, 50,50)
        elif self.isingrav:
            rect = pygame.Rect(100,0, 50,50)
        image.blit(self.sprite_perso, (0,0), rect)
        if not self.sens:
            image = pygame.transform.flip(image, True, False)
        if self.vie <= 0:
            ecart_mod = 0.4
            coef = 1
            ecart = time() -self.last_dommage
            if ecart < 0.1:
                rect = pygame.Rect(50,0, 50,50)
            elif ecart < 0.2:
                rect = pygame.Rect(50,50, 50,50)
            elif ecart < 0.3:
                rect = pygame.Rect(50,100, 50,50)
            else:
                rect = pygame.Rect(50,150, 50,50)
            image = copy.copy(const.vide)
            image.blit(const.sprite_degats, (0,0), rect)


        self.changer_image(image)

        # fire
        if self.fired and self.ctrl:
            if time()-self.last_dommage_fire > 5:
                self.subir_degats(1)
                self.last_dommage_fire = time()
            if time() > self.fired_time_stop:
                self.fired = False
        # Uranium
        if self.inv.get_item().id in [26,27,28,29,30] and self.ctrl:
            if time()-self.last_dommage_ur > 15:
                self.subir_degats(1)
                self.last_dommage_ur = time()


    def set_org_color(self, id_color=-1):
        if id_color == -1:
            self.color = []
            self.color.append(pygame.Color(0,128,0,255))
            self.color.append(pygame.Color(0,93,0,255))
            self.color.append(pygame.Color(0,0,0,255))
            self.color.append(pygame.Color(255,221,212,255))
            self.color.append(pygame.Color(145,72,0,255))
        elif id_color == 0:
            self.color[0] = pygame.Color(0,128,0,255)
        elif id_color == 1:
            self.color[1] = pygame.Color(0,93,0,255)
        elif id_color == 2:
            self.color[2] = pygame.Color(0,0,0,255)
        elif id_color == 3:
            self.color[3] = pygame.Color(255,221,212,255)
        elif id_color == 4:
            self.color[4] = pygame.Color(145,72,0,255)
        self.update_color()

    def set_color(self, surface):
        new_surface = copy.copy(surface)
        for x in range(surface.get_width()):
            for y in range(surface.get_height()):
                # corps
                if str(surface.get_at((x,y))) == "(0, 255, 0, 255)":
                    new_surface.set_at((x,y), self.color[0])
                # pants
                elif str(surface.get_at((x,y))) == "(0, 0, 255, 255)":
                    new_surface.set_at((x,y), self.color[1])
                # cheveux
                elif str(surface.get_at((x,y))) == "(255, 0, 0, 255)":
                    new_surface.set_at((x,y), self.color[2])
                # skin
                elif str(surface.get_at((x,y))) == "(255, 220, 220, 255)":
                    new_surface.set_at((x,y), self.color[3])
                # other
                elif str(surface.get_at((x,y))) == "(150, 100, 0, 255)":
                    new_surface.set_at((x,y), self.color[4])
        return new_surface
        
        
    def hit(self):
        if self.ctrl:
            self.hitting = True
        self.last_hit = time()
        if self.angle_arm == 0:
            self.angle_arm = 70
            self.changement_angle = time()

    def get_char(self, sep="\n"):
        buffer = self.nom+sep
        for i in self.color:
            buffer += str(i.r)+","
            buffer += str(i.g)+","
            buffer += str(i.b)
            buffer += sep
        return buffer

    def from_char(self, buffer, sep="\n"):
        buffer = buffer.split(sep)
        self.nom = buffer[0]
        buffer.remove(buffer[0])
        for i in range(5):
            self.char2color(buffer[i], i)
            
    def char2color(self, buffer, nbr_color):
        rgb = buffer.split(",")
        self.color[nbr_color] = pygame.Color(int(rgb[0]), int(rgb[1]), int(rgb[2]), 255)


    def save(self):
        if not os.path.isdir("data/perso"):
            os.mkdir("data/perso")
        file = open("data/perso/"+self.nom, "w")
        file.write(self.get_char())
        file.close()

    def load(self, nom):
        file = open("data/perso/"+nom, 'r')
        self.from_char(file.read())
        self.update_color()

    
    def update_color(self, fast=False):
        self.vie = 6
        self.sprite_perso = self.set_color(const.sprite_perso)
        if not fast:
            self.sprite_arm = self.set_color(const.sprite_arm) 
        self.anim(False)

    def reset(self):
        self.move_el(-self.x, -self.y)
        self.map = 0
        self.id_porte = 0
        self.vie = 6
        self.last_dommage = time()
        self.last_dommage_ur = time()
        self.last_hit = 0
        self.inv = Inventaire()
        item = Item(1, 1)
        self.inv.add(item)
        self.fired = False
        self.fired_time_stop = 0

        self.v_y = 0
        self.v_x = 0
        self.isingrav = True

    def tendance(self, map):
        if self.v_x != 0:
            self.anim(True)
        else:
            self.anim(False)
        if self.isingrav:
            self.move_el(0, self.v_y)
        self.move_el(self.v_x, 0)
            

    ################### Moteur Physique ###################

    # Faire subir au perso les lois de gravitations
    # map : liste contenant les elements de la map
    def tomber(self, map):
        if self.y < 550 or self.v_y < 0:
           if self.move(self.v_x, self.v_y, map):
               if self.v_y != 0:
                   self.isingrav = True
               self.v_y = self.v_y + 1


           else:
               self.isingrav = False
               const.input.append("stop_jump")
               self.v_y = 0
               self.v_x = 0

        else: 
            self.isingrav = False
            const.input.append("stop_jump")
    
    # Fait sauter notre personnage
    # x : vitesse en x
    # y : vitesse en y
    def sauter(self, x, y, force = False):
        if self.isingrav == False or force:
            self.v_y = y
            self.v_x = x
            self.isingrav = True
            const.input.append("jump")

    # Déplacer le personnage avec collision
    # x : deplacement en x
    # y : deplacement en y
    #
    # Retour :
    #     True : Deplacement effectué (peut etre modaifié)
    #     False : Deplacement non effectué (collision)
    def move(self, x, y, map):
        if self.collided_map(x, y, map) == False:
            if self.y+y < 550: 
                self.move_el(0,y)
            else:
                self.move_el(0, 550-self.y)
                
            if self.x + x > 0 and self.x +x < 750:
                self.move_el(x,0)
            return True
        
        elif self.collided_map(0, y, map) == False:
            if self.y+y < 550: 
                self.move_el(0,y)
            else:
                self.move_el(0, 550-self.y)
            return True
        else:
            return False

    def monter_echelle(self, map):
        if self.collided_type(0,0, map, Echelle):
                self.move(0,-5, map)
                self.isingrav = False
                const.input.append("stop_jump")
                self.v_y = 0
                self.v_x = 0


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
        collided = False
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
                        collided=True
                elif isinstance(i, BlocDisp):
                    if (i.etat):
                        collided=True
                elif isinstance(i, BlocDanger):
                    self.subir_degats(i.atk)
                    collided=True
                elif isinstance(i, Lava):
                    self.fired = True
                    self.fired_time_stop = time()+(i.unit*0.4)
                elif not isinstance(i, Porte) and not isinstance(i, Echelle) and not isinstance(i, Deco) and not isinstance(i,Liquid):
                    collided=True
            
        return collided


    def collided_type(self, dep_x, dep_y, map, type):
        future_rect = pygame.Rect(self.rect)
        future_rect = future_rect.move(dep_x, dep_y)
        # Vérification pour chaques éléments de la map
        for i in map:
            if future_rect.colliderect(i.rect):
                if isinstance(i, type):
                    if type == Terre:
                        if (self.inv.get_item().id in [1,2,7,12,17,22,27]) and not self.inv.isfull(i):
                            if i.hit(self.inv.get_item().damage):
                                self.inv.add(i)
                                map.remove(i)
                    elif type == Stone:
                        if (self.inv.get_item().id in [1,3,8,13,18,23,28]) and not self.inv.isfull(i):
                            if i.hit(self.inv.get_item().damage):
                                if isinstance(i, Coal):
                                    self.inv.add(Item(34, 4))
                                else:
                                    self.inv.add(i)
                                map.remove(i)
                    elif type == Wood:
                        if (self.inv.get_item().id in [1,4,9,14,19,24,29]) and not self.inv.isfull(i):
                            if i.hit(self.inv.get_item().damage):
                                self.inv.add(i)
                                map.remove(i)
                    elif type == Deco:
                        if (self.inv.get_item().id in [2,3,4,7,8,9,12,13,14,17,18,19,22,23,24,27,28,29]) and not self.inv.isfull(i):
                            self.inv.add(i)
                            map.remove(i)
                    return True
            
        return False

    def collided_utils(self, dep_x, dep_y, map, app, input):
        future_rect = pygame.Rect(self.rect)
        future_rect = future_rect.move(dep_x, dep_y)
        # Vérification pour chaques éléments de la map
        for i in map:
            if future_rect.colliderect(i.rect):
                if isinstance(i,Porte):
                    if i.etat == 1:
                        self.map = self.map+1
                    elif i.etat == 0:
                        self.map = self.map-1
                    elif i.etat == 2:
                        self.map = i.target 
                    self.id_porte = i.id
                elif isinstance(i, Forge):
                    atelier(app, self, "Forge")
                    input.reset()
                elif isinstance(i, Furnace):
                    atelier(app, self, "Furnace", i)
                    input.reset()
                elif isinstance(i, Atelier):
                    atelier(app, self, "Workbench")
                    input.reset()
                elif isinstance(i, Coffre):
                    atelier(app, self, "Chest", i)
                    input.reset()


    def collided_bloc(self, dep_x, dep_y, element):
        future_rect = pygame.Rect(self.rect)
        future_rect = future_rect.move(dep_x, dep_y)
        if future_rect.colliderect(element.rect):
            return True
        return False

    def collided_mob(self, mob):
        future_rect = pygame.Rect(self.rect)
        future_rect.width = 100
        future_rect.height = 100
        if self.sens:
            future_rect = future_rect.move(-future_rect.x+self.x,-future_rect.y+self.y-50)
        else:
            future_rect = future_rect.move(-future_rect.x+self.x-50,-future_rect.y+self.y-50)
        # Vérification pour chaques mobs
        collided = False
        for i in mob:
            if future_rect.colliderect(i.rect):
                i.subir_degats(self.inv.get_item().atk)
                collided = True

        return collided




            
        
        
