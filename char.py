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
