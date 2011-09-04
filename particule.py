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

import element

import random
from time import *
# Pygame
import pygame
from pygame.locals import *

class Particule(element.Element):
    def __init__(self, id):
        element.Element.__init__(self)
        self.id = id
        if id == 1:
            self.taille = random.randint(1, 10)
            self.color=pygame.Color(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),255)
            self.v_x = random.randint(-10,10)
            self.v_y = random.randint(-10,10)
        # Blood
        elif id == 2:
            self.taille = random.randint(1, 5)
            self.color=pygame.Color(random.randint(100, 255),0,0)
            self.v_x = random.randint(-5,5)
            self.v_y = random.randint(-10,0)
        # Stone
        elif id == 3:
            self.taille = random.randint(1, 5)
            rand = random.randint(50, 200)
            self.color=pygame.Color(rand,rand,rand)
            self.v_x = random.randint(-5,5)
            self.v_y = random.randint(-8,0)
        # Wood
        elif id == 4:
            self.taille = random.randint(1, 5)
            self.color=pygame.Color(random.randint(150, 255),100,0)
            self.v_x = random.randint(-5,5)
            self.v_y = random.randint(-8,0)
        # Dirt
        elif id == 5:
            self.taille = random.randint(1, 5)
            self.color=pygame.Color(random.randint(50, 100),30,0)
            self.v_x = random.randint(-5,5)
            self.v_y = random.randint(-8,0)
        # Sprint left
        elif id == 6:
            self.taille = 1
            rand = random.randint(100, 200)
            self.color=pygame.Color(rand,rand,rand)
            self.v_x = random.randint(0,5)
            self.v_y = random.randint(-5,-3)
        # Sprint right
        elif id == 7:
            self.taille = 1
            rand = random.randint(100, 200)
            self.color=pygame.Color(rand,rand,rand)
            self.v_x = random.randint(-5,0)
            self.v_y = random.randint(-5,-3)
        # walk left
        elif id == 8:
            self.taille = 1
            rand = random.randint(100, 200)
            self.color=pygame.Color(rand,rand,rand)
            self.v_x = 1
            self.v_y = random.randint(-5,-3)
        # Walk right
        elif id == 9:
            self.taille = 1
            rand = random.randint(100, 200)
            self.color=pygame.Color(rand,rand,rand)
            self.v_x = -1
            self.v_y = random.randint(-3,-1)
        img = pygame.Surface((self.taille, self.taille))
        img.fill(self.color)
        self.changer_image(img)

        self.hauteur_fire = random.randint(50, 300)
        self.time_creat = time()

    def update(self):
        self.move_el(self.v_x, self.v_y)
        if not self.id in [6,7,8,9]:
            self.v_y += 1
        else:
            self.taille += 1
            img = pygame.Surface((self.taille, self.taille))
            img.fill(self.color)
            self.changer_image(img)

