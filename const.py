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

"""Constantes du jeu The Scret of Tower"""

version = "Beta 0.2.0"

# Constante de fps
fps = 30

fenetre_size_x = 800
fenetre_size_y = 600
fenetre_titre = "The Secret Tower"
title = "The Secret Tower"
path_fond_menu = "img/fond_menu.png"
path_fond1 = "img/fond1.png"
path_fond2 = "img/fond2.png"
path_choix = "img/choix.png"
display = True

# chatbox
color_basic = (255,255,255)
color_annonce = (255,180,40)
color_important = (255,60,60)

global sprite_bloc
global sprite_lave
global sprite_perso
global sprite_arm
global sprite_item
global sprite_mobs
global sprite_torch
global sprite_degats
global sprite_fire
global vide

# Thread
port = 2345
global host
global output
global input
global input_udp
global map
global events_map
global events
global persos
global runned
global msg
global id_last_event_map
global id_last_event
runned = False
input = []
output = ""
input_udp = ""
map = []
persos = []
events = []
events_map = []
msg = []
id_last_event_map = 0
id_last_event = 0

global chatbox





