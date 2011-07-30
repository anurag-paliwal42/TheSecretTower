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

def editeur(app, map, nom):

    input = range(0, 1000, 1)

    for i in range(len(input)):
        input[i] = 0
    
    fond = Element()
    fond.changer_image(pygame.image.load(const.path_fond1).convert())

    select = Element()
    select.changer_image(pygame.image.load("img/select.png").convert_alpha())
    select.move_el(0,0)
    b_txt = []
    b_txt = write(app, "("+str(select.x)+";"+str(select.y)+")", 0, 0)
    w_txt = []
    w_txt = write(app, "("+str(select.x)+";"+str(select.y)+")", 0, 0, (255,255,255))
    cmd = 1

    while cmd<>0: 
        cmd = update_event(input, app)
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

        if input[K_KP7]:
            input[K_KP7] = 0
            bloc = Torch(13)
            bloc.move_el(select.x, select.y)
            map.append(bloc)

        if input[K_DELETE]:
            input[K_DELETE] = 0
            for i in map:
                if (i.x == select.x and i.y == select.y):
                    map.remove(i)
        if input[K_ESCAPE]:
            input[K_ESCAPE] = 0
            cmd = menu(app, "Edit Level", ["Save Level","Save Level as", "Load Level","Try Level", "Quit"])
            if cmd == 2:
                nom = ask(app, "Save as :")
            if cmd == 2 or cmd == 1:
                save_map("map/custom/"+nom, map)
            elif cmd == 3:
                nom = ask(app,"Load Level] Level's name : ")
                map = open_map("map/custom/"+nom)
                cmd =1
            elif cmd == 4:
                jeu(app, map, app.perso)
            elif cmd == 0:
                return 5
            
        b_txt = []
        b_txt = write(app, "("+str(select.x)+";"+str(select.y)+")\n"+nom, 0, 0)
        w_txt = []
        w_txt = write(app, "("+str(select.x)+";"+str(select.y)+")\n"+nom, 2, 2, (255,255,255))
        app.blit(fond)
        for i in map:
            app.blit(i)
        app.blit(select)
        for i in w_txt:
            app.blit(i)
        for i in b_txt:
            app.blit(i)

        app.flip()

    return cmd
