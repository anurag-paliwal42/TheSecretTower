#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

from perso import *
from bloc import *
from element import *
from event import *

import pygame
from pygame.locals import *

            
def jeu(app):
    input = range(0, 1000, 1)

    for i in range(len(input)):
        input[i] = 0
    perso = Perso()
    perso.move_el(100,100)

    fond_menu = Element()
    fond_menu.changer_image(pygame.image.load(const.path_fond_menu).convert())


    # Map
    map = []

    bloc = Bloc(1)
    bloc.move_el(200,550)

    map.append(bloc)

    bloc2 = Bloc(1)
    bloc2.move_el(250,500)
    map.append(bloc2)

    bloc3 = Bloc(1)
    bloc3.move_el(350,400)
    map.append(bloc3)

    bloc4 = Bloc(1)
    bloc4.move_el(450,300)
    map.append(bloc4)

    bloc5 = Bloc(1)
    bloc5.move_el(350,200)
    map.append(bloc5)

    bloc5 = Bloc(1)
    bloc5.move_el(200,150)
    map.append(bloc5)

    bloc7 = Bloc(1)
    bloc7.move_el(0,450)
    map.append(bloc7)

    bloc6 = BlocMouvant(1, 60, 200, 0, 350)
    map.append(bloc6)

    bloc8 = BlocMouvant(1, 450, 200, 100, 0)
    map.append(bloc8)

    bloc9 = BlocDisp(1)
    bloc9.move_el(450,500)
    map.append(bloc9)
    
    bloc10 = BlocDisp(1, 5)
    bloc10.move_el(500,500)
    map.append(bloc10)

    

    cmd = 1
    while cmd<>0:
        
        # Traitement events
        cmd = update_event(input)
  
        if (input[K_SPACE] or input[K_UP]) and input[K_LEFT]:
            perso.sauter(-5, -15)
            input[K_SPACE] = 0
            input[K_UP] = 0

        if (input[K_SPACE] or input[K_UP]) and input[K_RIGHT]:
            perso.sauter(5, -15)
            input[K_SPACE] = 0
            input[K_UP]

        if (input[K_SPACE] or input[K_UP]):
            perso.sauter(0, -15)
            input[K_SPACE] = 0
            input[K_UP] = 0
        if input[K_LEFT]:
            perso.move(-5,0, map)
        if input[K_RIGHT]:
            perso.move(5,0, map)
        if input[K_RETURN]:
            perso.subir_degats(1)

        
        perso.tomber(map)

        # Affichage
        app.blit(fond_menu)
        for i in map:
            if isinstance(i, BlocMouvant):
                i.move()
                app.blit(i)
            elif isinstance(i, BlocDisp):
                i.disp()
                if (i.etat):
                    app.blit(i)
            else:
                app.blit(i)
        app.blit(perso)
        app.flip()


        if perso.vie <= 0:
            return 2

    return 0
        
    
