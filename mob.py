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
import const

from time import *

# Pygame
import pygame
from pygame.locals import *


class Mob(Element):
    
    def __init__(self, id):
        Element.__init__(self)
        self.id = id
        if id == 0:
            self.vie = 20
            self.atk = 1
            self.vitesse = 1
        if id == 1:
            self.vie = 10
            self.atk = 1
            self.vitesse = 1
        if id == 2:
            self.vie = 10
            self.atk = 1
            self.vitesse = 2

        self.sens = True
        self.changement = 0
        self.rang_image = 0
        self.last_degats = 0

        self.fired = False
        self.fired_time_stop = 0
        self.last_dommage_fire = time()

        self.isingrav=False
        self.v_y = 0
        
        self.anim()
        self.rect.width = 20
        self.rect.height = 40
        self.rect = self.rect.move(15, 10)

    def update(self, map):
        if self.vie > 0:
            self.tomber(map)
            if self.sens:
                if self.move(self.vitesse, 0, map) != True:
                    if random.randint(0,3) == 0 and not self.isingrav:
                        self.sens = False
                    else:
                        self.sauter(-10)
            elif not self.sens:
                if self.move(-self.vitesse, 0, map) != True:
                    if random.randint(0,3) == 0 and not self.isingrav:
                        self.sens = True
                    else:
                        self.sauter(-10)
            self.anim()
            

    def subir_degats(self, degat):
        if (self.vie > 0):
            self.vie = self.vie - degat
            self.sauter(-5)
            self.last_degats = time()
            return True
        if (self.vie <= 0):
            return False


    def anim(self):
        image = copy.copy(const.vide)

        # fire
        if self.fired:
            rect = pygame.Rect(0,random.randint(0, 3)*50, 50,50)
            image.blit(const.sprite_fire, (0,0), rect)
            if time()-self.last_dommage_fire > 4:
                self.subir_degats(5)
                self.last_dommage_fire = time()
            if time() > self.fired_time_stop:
                self.fired = False

        rect = pygame.Rect(self.rang_image*50,self.id*50, 50,50)

        if time() - self.changement > 0.1 and not self.isingrav:
            self.changement = time()
            if self.rang_image < 2:
                self.rang_image += 1
            else:
                self.rang_image = 0
            rect = pygame.Rect(self.rang_image*50,self.id*50, 50,50)
        elif self.isingrav:
            rect = pygame.Rect(100, self.id*50, 50,50)
        
        image.blit(const.sprite_mobs, (0,0), rect)
        if not self.sens:
            image = pygame.transform.flip(image, True, False)


        ecart_mod = 0.2
        ecart = time() -self.last_degats
        if ecart < ecart_mod:
            if ecart < 0.05:
                rect = pygame.Rect(50,0, 50,50)
            elif ecart < 0.1:
                rect = pygame.Rect(50,50, 50,50)
            elif ecart < 0.15:
                rect = pygame.Rect(50,100, 50,50)
            else:
                rect = pygame.Rect(50,150, 50,50)
            image.blit(const.sprite_degats, (0,0), rect)
                
        self.changer_image(image)


    def sauter(self, y, force = False):
        if self.isingrav == False or force:
            self.v_y = y
            self.isingrav = True

    def tomber(self, map):
        if self.y < 550 or self.v_y:
           if self.move(0, self.v_y, map):
               if self.v_y <> 0:
                   self.isingrav = True
               self.v_y = self.v_y + 1


           else:
               self.isingrav = False
               self.v_y = 0

        else: 
            self.isingrav = False

    def move(self, x, y, map):
        if self.collided_map(x, y, map) == False:
            if self.x + x > 0 and self.x +x < 750:
                self.move_el(x,0)
            else:
                return False

            if self.y+y < 550: 
                self.move_el(0,y)
            else:
                self.move_el(0, 550-self.y)
                return False
                

            return True
        else:
            return False
        

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
                    if i.atk >= 10:
                        self.subir_degats(i.atk)
                    collided=True
                elif isinstance(i, Lava):
                    self.fired = True
                    self.fired_time_stop = time()+(i.unit*0.4)
                elif not isinstance(i, Porte) and not isinstance(i, Echelle) and not isinstance(i, Deco) and not isinstance(i, Liquid):
                    collided=True
            
        return collided

    def collided_perso(self, dep_x, dep_y, perso):
        future_rect = pygame.Rect(self.rect)
        future_rect = future_rect.move(dep_x, dep_y)

        if future_rect.colliderect(perso.rect) and self.vie > 0:
            perso.subir_degats(self.atk)
            return True

        return False
        
