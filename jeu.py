#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

from perso import *
from bloc import *
from element import *
from event import *
from map import *

import pygame
from pygame.locals import *

            
def jeu(app, map):
    input = range(0, 1000, 1)

    for i in range(len(input)):
        input[i] = 0
    perso = Perso()
    for i in map:
        if isinstance(i, Porte):
            if i.etat == 0:
                perso.move_el(i.x,i.y)

    fond = Element()
    fond.changer_image(pygame.image.load(const.path_fond1).convert())


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
        app.blit(fond)
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
        
    
