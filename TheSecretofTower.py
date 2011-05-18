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

app = App()

if menu(app) == 1:
    jeu(app)

pygame.quit()
