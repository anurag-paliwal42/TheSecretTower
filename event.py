#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

import pygame
from pygame.locals import *


# Met à jour les events
def update_event(input):
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            input[event.key] = 1;
        if event.type == KEYUP:
            input[event.key] = 0;
        if event.type == QUIT:
            return False
    return True
