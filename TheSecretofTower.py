#!/usr/bin/python

#-*-coding:Utf-8 -*

################################################
#                                              #
#      The Secret of Tower                     #
#                                              #
#          Auteur : Pierre Surply              #
#     2011                                     #
#                                              # 
################################################


# Pygame
import pygame
from pygame.locals import *

# App
from app import *

# Element
from element import *

# Const
import const

from menu import *
from jeu import *
from map import *

app = App()

cmd = 1
while cmd:
    cmd =  menu(app, "Menu principal", ["Nouvelle Partie", "Charger Partie", "Quitter"])

    if cmd == 1:
        cmd = jeu(app, open_map(0))

    if cmd == 2:
        cmd = menu(app, "Game Over", ["Rejouer", "Quitter"])

pygame.quit()
