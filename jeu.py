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

            
def jeu(app, map, perso):
    input = range(0, 1000, 1)

    for i in range(len(input)):
        input[i] = 0

    for i in map:
        if isinstance(i, Porte):
            if i.id == perso.id_porte:
                perso.move_el(-perso.x, -perso.y)
                perso.move_el(i.x,i.y)
    
    fond = Element()
    fond.changer_image(pygame.image.load(const.path_fond1).convert())


    # interface 
    coeur = Element()
    coeur.changer_image(pygame.image.load("img/coeur.png").convert_alpha())
    coeur.y = 540

    interface = Element()
    interface.changer_image(pygame.image.load("img/interface.png").convert())
    interface.image.set_alpha(75)
    interface.move_el(310, 530)
    
    text_item = Element()
    text_item.changer_text(perso.inv.get_item().nom + " (x" + str(perso.inv.get_item().nbr)+")" , app.font)
    text_item.move_el(380, 560)

    fps= 0
    imgfps = Element()
    imgfps.changer_text("FPS : " + str(fps), app.font)
    imgfps.move_el(0, 0)
    
    cmd = 1
    prev = time()+1

    while cmd<>0:
        

        # controle fps
        fps = int(1/(time() - prev))
        while fps > const.fps: 
            fps = int(1/(time() - prev))

        imgfps.changer_text("FPS : " +str(fps), app.font)
        prev = time()

        if perso.inv.get_item().nbr > 1:
            text_item.changer_text(perso.inv.get_item().nom + " (x" + str(perso.inv.get_item().nbr)+")" , app.font)
        else : 
            text_item.changer_text(perso.inv.get_item().nom , app.font)
        
        # Traitement events
        cmd = update_event(input)
  
        if (input[K_SPACE] or input[K_a] or input[K_q]) and input[K_LEFT]:
            perso.sauter(-5, -15)
            input[K_SPACE] = 0
            input[K_a] = 0
            input[K_q] = 0

        if (input[K_SPACE] or input[K_a] or input[K_q]) and input[K_RIGHT]:
            perso.sauter(5, -15)
            input[K_SPACE] = 0
            input[K_a] = 0
            input[K_q] = 0

        if (input[K_SPACE] or input[K_a] or input[K_q]):
            perso.sauter(0, -15)
            input[K_SPACE] = 0
            input[K_a] = 0
            input[K_q] = 0

        if (input[K_z] or input[K_w]) and input[K_DOWN]:
            if not perso.collided_type(0,10,map,Terre):
                if isinstance(perso.inv.get_item(), Item_Bloc):
                    bloc = perso.inv.get_item().type(perso.inv.get_item().bloc.picture)
                    bloc.move_el(-bloc.x+50*int((perso.x+10)/50), -bloc.y+50*int((perso.y+75)/50))
                    if not perso.collided_bloc(0,0, bloc):
                        collided = False
                        for i in map:
                            if i.x == bloc.x and i.y == bloc.y:
                                collided = True

                        if not collided:
                            map.append(bloc) 
                            perso.inv.delete()
            input[K_z] = 0
            input[K_w] = 0
        if (input[K_z] or  input[K_w]) and input[K_UP]:
            perso.collided_type(0,-50,map,Terre)
            input[K_z] = 0
            input[K_w] = 0
        if (input[K_z] or  input[K_w]) and input[K_LEFT]:
            perso.collided_type(-10,0,map,Terre)
            input[K_z] = 0
            input[K_w] = 0
        if (input[K_z] or  input[K_w]) and input[K_RIGHT]:
            perso.collided_type(10,0,map,Terre)
            input[K_z] = 0
            input[K_w] = 0
        if (input[K_z] or  input[K_w]):
            if not perso.collided_type(0,0,map,Porte):
                if isinstance(perso.inv.get_item(), Item_Bloc):
                    bloc = perso.inv.get_item().type(perso.inv.get_item().bloc.picture)
                    if perso.sens:
                        bloc.move_el(-bloc.x+50*int((perso.x+75)/50), -bloc.y+50*int((perso.y+25)/50))
                    if perso.sens == False:
                        bloc.move_el(-bloc.x+50*int((perso.x-50)/50), -bloc.y+50*int((perso.y+10)/50))
                    if not perso.collided_bloc(0,0, bloc):
                        collided = False
                        for i in map:
                            if i.x == bloc.x and i.y == bloc.y:
                                collided = True

                        if not collided:
                            map.append(bloc) 
                            perso.inv.delete()

            input[K_z] = 0
            input[K_w] = 0
        if (input[K_e]):
            perso.inv.changer_select(1)
            input[K_e] = 0
        if input[K_UP]:
            perso.monter_echelle(map)
        if input[K_LEFT]:
            perso.move(-5,0, map)
        if input[K_RIGHT]:
            perso.move(5,0, map)
        if input[K_RETURN]:
            perso.subir_degats(1)
        if input[K_ESCAPE]:
            input[K_ESCAPE] = 0
            if app.partie[0] != "Gen":
                cmd = menu(app, "Pause", ["Reprendre", "Sauvegarder", "Quitter"])
            else:
                 cmd = menu(app, "Pause", ["Reprendre", "Quitter"])
            if cmd == 2:
                app.save_partie()
                save_map("save/{0}/map{1}".format(app.partie[0], app.partie[1]), map)
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
        app.blit(interface)
        for i in range(perso.vie):
            coeur.x = 380 + i*30
            app.blit(coeur)
        app.blit(perso.inv.get_element())
        app.blit(text_item)
        app.blit(imgfps)
        app.flip()


        if perso.vie <= 0:
            perso.vie = 3
            for i in map:
                if isinstance(i, Porte):
                    if i.id == perso.id_porte:
                        perso.move_el(-perso.x, -perso.y)
                        perso.move_el(i.x,i.y)

        if perso.map != app.partie[1]:
            if app.partie[0] != "Gen":
                save_map("save/{0}/map{1}".format(app.partie[0], app.partie[1]), map)
            return 1

    return 0
