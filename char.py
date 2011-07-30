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

#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

from element import *

# Pygame
import pygame
from pygame.locals import *

def write(app, string, x, y, color = (0,0,0), pas=15):
    strings = string.split("\n")
    texte = []
    for i in strings:
        temp = Element()
        temp.changer_text(i, app.font_petit, color)
        temp.move_el(x, y)
        texte.append(temp)
        y += pas

    return texte
