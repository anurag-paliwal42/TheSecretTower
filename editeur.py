#-*-coding:Utf-8 -*
# Auteur : Pierre Surply
import pygame
from pygame.locals import *

from app import *

from event import *
from map import *
from menu import *
from jeu import *
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
    coord = Element()
    coord.changer_text("("+str(select.x)+";"+str(select.y)+")", app.font)
    coord.move_el(0,0)
    cmd = 1

    while cmd<>0: 
        cmd = update_event(input)
        if input[K_UP]:
            input[K_UP] = 0
            if select.y > 0:
                select.move_el(0,-50)
        if input[K_DOWN]:
            input[K_DOWN] = 0
            if select.y < 550 :
                select.move_el(0,50)
        if input[K_LEFT]:
            input[K_LEFT] = 0 
            if select.x > 0 :
                select.move_el(-50,0)
        if input[K_RIGHT]:
            input[K_RIGHT] = 0
            if select.x < 750 :
                select.move_el(50,0)
        if input[K_KP0]:
            input[K_KP0] = 0
            bloc = Porte(0, 0)
            for i in map:
                if (i.x == select.x and i.y == select.y):
                    map.remove(i)
                elif isinstance(i, Porte):
                    if i.etat == 0:
                        map.remove(i)
            bloc.move_el(select.x, select.y)
            map.append(bloc)
        if input[K_KP1]:
            input[K_KP1] = 0
            for i in map:
                if (i.x == select.x and i.y == select.y):
                    map.remove(i)
            bloc = Bloc(1)
            bloc.move_el(select.x, select.y)
            map.append(bloc) 

        if input[K_KP2]:
            input[K_KP2] = 0
            for i in map:
                if (i.x == select.x and i.y == select.y):
                    map.remove(i)
            bloc = Bloc(5)
            bloc.move_el(select.x, select.y)
            map.append(bloc) 

        if input[K_KP3]:
            input[K_KP3] = 0
            for i in map:
                if (i.x == select.x and i.y == select.y):
                    map.remove(i)
            bloc = Bloc(6)
            bloc.move_el(select.x, select.y)
            map.append(bloc)
        if input[K_KP4]:
            input[K_KP4] = 0
            for i in map:
                if (i.x == select.x and i.y == select.y):
                    map.remove(i)
            bloc = BlocDanger(2, 10)
            bloc.move_el(select.x, select.y)
            map.append(bloc)
        
        if input[K_KP5]:
            input[K_KP5] = 0
            for i in map:
                if (i.x == select.x and i.y == select.y):
                    map.remove(i)
            bloc = BlocDanger(4, 1)
            bloc.move_el(select.x, select.y)
            map.append(bloc)

        if input[K_KP6]:
            input[K_KP6] = 0
            for i in map:
                if (i.x == select.x and i.y == select.y):
                    map.remove(i)
                elif isinstance(i, Porte):
                    if i.etat == 1:
                        map.remove(i)
            bloc = Porte(0, 1)
            bloc.move_el(select.x, select.y)
            map.append(bloc)

        if input[K_DELETE]:
            input[K_DELETE] = 0
            for i in map:
                if (i.x == select.x and i.y == select.y):
                    map.remove(i)
        if input[K_ESCAPE]:
            input[K_ESCAPE] = 0
            cmd = menu(app, "Editeur de map", ["Sauvegarder", "Charger","Tester", "Quitter"])
            if cmd == 1:
                save_map(ask(app, "Sauvegarder la map :"), map)
            elif cmd == 2:
                map = open_map(ask(app,"Entrez le nom de la map : "))
                cmd =1
            elif cmd == 3:
                jeu(app, map)
            elif cmd == 0:
                return 5
            
        coord.changer_text("("+str(select.x)+";"+str(select.y)+")", app.font)
        app.blit(fond)
        for i in map:
            app.blit(i)
        app.blit(select)
        app.blit(coord)
        app.flip()

    return cmd
