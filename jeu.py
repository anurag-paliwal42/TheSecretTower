#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

from perso import *
from bloc import *
from element import *
from event import *
from map import *
from menu import *

from time import *

import pygame
from pygame.locals import *

            
def jeu(app, map, x = -1, y = -1):
    input = range(0, 1000, 1)

    for i in range(len(input)):
        input[i] = 0
    perso = Perso()
    if x == -1:
        for i in map:
            if isinstance(i, Porte):
                if i.etat == 0:
                    perso.move_el(i.x,i.y)
    else:
        perso.move_el(x, y)
    
    fond = Element()
    fond.changer_image(pygame.image.load(const.path_fond1).convert())

    coeur = Element()
    coeur.changer_image(pygame.image.load("img/coeur.png").convert_alpha())
    coeur.y = 10
    
    fps= 0
    imgfps = Element()
    imgfps.changer_text("FPS : " + str(fps), app.font)
    imgfps.move_el(10, 30)
    
    cmd = 1
    prev = time()+1

    while cmd<>0:
        

        # controle fps
        fps = int(1/(time() - prev))
        while fps > const.fps: 
            fps = int(1/(time() - prev))

        imgfps.changer_text("FPS : " +str(fps), app.font)
        prev = time()
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
        if input[K_ESCAPE]:
            input[K_ESCAPE] = 0
            cmd = menu(app, "Pause", ["Reprendre", "Recommencer", "Quitter"])
            if cmd == 2:
                for i in map:
                    if isinstance(i, Porte):
                        if i.etat == 0:
                            perso.move_el(i.x-perso.x,i.y-perso.y)
                cmd = 1
            if cmd == 0:
                return 5
                

        
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
        for i in range(perso.vie):
            coeur.x = 10 + i*30
            app.blit(coeur)
            app.blit(imgfps)
        app.flip()


        if perso.vie <= 0:
            perso.vie = 3
            for i in map:
                if isinstance(i, Porte):
                    if i.etat == 0:
                        perso.move_el(i.x - perso.x,i.y-perso.y)
        if perso.win:
            return 1

    return 0
        
    
