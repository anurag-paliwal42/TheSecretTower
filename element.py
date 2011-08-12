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

# Pygame
import pygame
from pygame.locals import *

import const

class Element:
    """ Définit l'élément de base de la fentre """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.rect = None

    def changer_image(self, src):
        if const.display:
            self.image = src
            if self.rect == None:
                self.rect = self.image.get_rect()

    def changer_text(self, text, font, color = (0,0,0)):
        if const.display:
            if isinstance(text, str):
                self.image = font.render(text, 1, color)
            if self.rect == None:
                self.rect = self.image.get_rect()

    def move_el(self, x, y):
        self.x = self.x+x
        self.y = self.y+y
        if const.display:
            self.rect = self.rect.move(x,y)
        
            
        
