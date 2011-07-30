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

import pygame
from pygame.locals import *


# Met à jour les events
def update_event(input, app):
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            input[event.key] = 1;
        if event.type == KEYUP:
            input[event.key] = 0;
        if event.type == QUIT:
            return False
        if event.type == VIDEORESIZE:
            app.set_size(event.size)
            app.size = event.size

    return True
