#-*-coding:Utf-8 -*
# Auteur : Pierre Surply
import pygame
from pygame.locals import *

from app import *

from event import *
from map import *
import const

def editeur(app, map):

    input = range(0, 1000, 1)

    for i in range(len(input)):
        input[i] = 0
    
    fond = Element()
    fond.changer_image(pygame.image.load(const.path_fond1).convert())

    select = Element()
    select.changer_image(pygame.image.load("img/select.png").convert_alpha())
    select.move_el(0,0)
    cmd = 1

    while cmd<>0: 
        cmd = update_event(input)
        if input[K_UP]:
            if select.y > 0:
                select.move_el(0,-50)
        if input[K_DOWN]:
            if select.y < 550 :
                select.move_el(0,50)
        if input[K_LEFT]:
            if select.x > 0 :
                select.move_el(-50,0)
        if input[K_RIGHT]:
            if select.x < 750 :
                select.move_el(50,0)
        if input[K_ESCAPE]:
            save_map(ask(app, "Sauvarder la map :"), map)
            input[K_ESCAPE] = 0

        app.blit(fond)
        for i in map:
            app.blit(i)
        app.blit(select)
        app.flip()

    return cmd
