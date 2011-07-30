#    TheSecretTower
#    Copyright (C) 2011 Pierre SURPLY
#
#    This file is part of TheSecretTower.
#
#    TheSecretTower is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    TheSecretTower is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with TheSecretTower.  If not, see <http://www.gnu.org/licenses/>.

#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

from perso import *
from mob import *
from bloc import *
from element import *
from event import *
from map import *
from menu import *
from char import *

from time import *
import random

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
    if app.partie[1] >= 0:
        fond.changer_image(pygame.image.load(const.path_fond1).convert())
    else:
        fond.changer_image(pygame.image.load(const.path_fond2).convert())

    # Noir
    shadow = []
    for x in range(16):
        for y in range(12):
            dark = Element()
            dark.changer_image(pygame.Surface((50, 50)))
            dark.move_el(x*50,y*50)
            delete = False
            for i in map:
                intens = 0
                if i.picture == 2:
                    intens = 4
                if i.picture == 13:
                    intens = 6
                if math.fabs(i.x-dark.x)+math.fabs(i.y-dark.y) < (intens-2)*50:
                    delete = True
                elif math.fabs(i.x-dark.x)+math.fabs(i.y-dark.y) < intens*50:
                    dark.image.set_alpha(75)
            if delete == False:
                shadow.append(dark)

    mobs = []
    for i in shadow:
        # pop monstre
        if (i.image.get_alpha() == 75 or i.image.get_alpha() == None) and random.randint(1, 5) == 1:
            creat = True
            for bloc in map:
                if bloc.x == i.x and bloc.y == i.y:
                    creat = False
            if creat:
                mob = Mob(random.randint(0,2))
                mob.move_el(i.x, i.y)
                mobs.append(mob)


    # interface 
    coeur = Element()
    coeur.changer_image(pygame.image.load("img/coeur.png").convert_alpha())
    coeur.y = 540
    coeur_vide = Element()
    coeur_vide.changer_image(pygame.image.load("img/coeur_vide.png").convert_alpha())
    coeur_vide.y = 540
    
    b_text_item = Element()
    b_text_item.changer_text(perso.inv.get_item().nom , app.font_petit)
    b_text_item.move_el(384, 569)
    w_text_item = Element()
    w_text_item.changer_text(perso.inv.get_item().nom , app.font_petit)
    w_text_item.move_el(380, 565)
    b_text_item2 = Element()
    b_text_item2.changer_text("x" + str(perso.inv.get_item().nbr) , app.font_petit)
    b_text_item2.move_el(384, 584)
    w_text_item2 = Element()
    w_text_item2.changer_text("x" + str(perso.inv.get_item().nbr) , app.font_petit)
    w_text_item2.move_el(380, 580)
  
    imgversion = Element()
    imgversion.changer_text(str(const.version), app.font)
    imgversion.move_el(0, 0)
    
    fps= 0
    info_b_txt = []
    info_b_txt = write(app, "V. "+str(const.version)+"\nFPS : "+str(fps)+"\nGame : "+app.partie[0], 4, 4)
    info_w_txt = []
    info_w_txt = write(app, "V. "+str(const.version)+"\nFPS : "+str(fps)+"\nGame : "+app.partie[0], 0, 0, (255,255,255))

    commandes =  "(a) : Jump\n(z) : Use\n(e/r) : Scroll inventory\n(i) : Inventory \n(v) : Change View\n(ESC) : Break"
    b_commandes = []
    b_commandes = write(app,commandes, 24, 54)
    w_commandes = []
    w_commandes = write(app, commandes, 20, 50, (255,255,255))
    
    cmd = 1
    prev = time()+1

    while cmd<>0:
        

        # controle fps
        fps = int(1/(time() - prev))
        while fps > const.fps: 
            fps = int(1/(time() - prev))

        info_b_txt = []
        info_b_txt = write(app, "V. "+str(const.version)+"\nFPS : "+str(fps)+"\nGame : "+app.partie[0], 4, 4)
        info_w_txt = []
        info_w_txt = write(app, "V. "+str(const.version)+"\nFPS : "+str(fps)+"\nGame : "+app.partie[0], 0, 0, (255,255,255))
        prev = time()

        b_text_item.changer_text(perso.inv.get_item().nom, app.font_petit)
        w_text_item.changer_text(perso.inv.get_item().nom, app.font_petit, (255,255,255))
        if perso.inv.get_item().nbr > 1:
            b_text_item2.changer_text("x" + str(perso.inv.get_item().nbr) , app.font_petit)
            w_text_item2.changer_text("x" + str(perso.inv.get_item().nbr) , app.font_petit, (255,255,255))
        else : 
            b_text_item2.changer_text("" , app.font_petit)
            w_text_item2.changer_text("" , app.font_petit, (255,255,255))

        # Shadow
        for i in shadow:
            if i.image.get_alpha() == 0:
                i.image.set_alpha(255)

        # Hit perso
        for i in mobs:
            i.collided_perso(0,0, perso)


                
        
        # Traitement events
        cmd = update_event(input, app)
  
        if (input[K_SPACE] or input[K_a] or input[K_q]) and input[K_LEFT] and  perso.vie > 0:
            perso.sauter(-5, -15)
            input[K_SPACE] = 0
            input[K_a] = 0
            input[K_q] = 0

        if (input[K_SPACE] or input[K_a] or input[K_q]) and input[K_RIGHT] and  perso.vie > 0:
            perso.sauter(5, -15)
            input[K_SPACE] = 0
            input[K_a] = 0
            input[K_q] = 0

        if (input[K_SPACE] or input[K_a] or input[K_q]) and  perso.vie > 0:
            perso.sauter(0, -15)
            input[K_SPACE] = 0
            input[K_a] = 0
            input[K_q] = 0

        if input[K_UP]:
            perso.collided_type(0,0,map,Porte)

        if (input[K_z] or  input[K_w]) and  perso.vie > 0 and time()-perso.last_hit > 0.3:

            perso.hit()

            #Destruction bloc + atk
            if perso.sens == False:
                s=-1
            else:
                s=1
            perso.collided_type(s*10,0,map,Terre)
            perso.collided_type(s*10,0,map,Stone, app, input)
            perso.collided_type(s*10,0,map,Wood, app, input)
            if perso.collided_type(s*10, 0, map, Deco, app):
                shadow_new = []
                for x in range(16):
                    for y in range(12):
                        alpha = 0
                        for i in shadow:
                            if i.x == x*50 and i.y == y*50:
                                alpha = i.image.get_alpha()
                        dark = Element()
                        dark.changer_image(pygame.Surface((50, 50)))
                        dark.move_el(x*50,y*50)
                        if alpha == 75:
                            dark.image.set_alpha(75)
                        delete = False
                        for i in map:
                            intens = 0
                            if i.picture == 2:
                                intens = 4
                            if i.picture == 13:
                                intens = 6
                            if math.fabs(i.x-dark.x)+math.fabs(i.y-dark.y) < (intens-2)*50:
                                delete = True
                            elif math.fabs(i.x-dark.x)+math.fabs(i.y-dark.y) < intens*50:
                                dark.image.set_alpha(75)
                        if delete == False:
                            shadow_new.append(dark)

                shadow = shadow_new
            perso.collided_mob(0,0,mobs)


                                
                                

            if not input[K_DOWN] and not input[K_UP]:
                # Placement bloc

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
                            if isinstance(bloc, Deco):
                                shadow_new = []
                                for x in range(16):
                                    for y in range(12):
                                        alpha = 0
                                        for i in shadow:
                                            if i.x == x*50 and i.y == y*50:
                                                alpha = i.image.get_alpha()
                                        dark = Element()
                                        dark.changer_image(pygame.Surface((50, 50)))
                                        dark.move_el(x*50,y*50)
                                        if alpha == 75:
                                            dark.image.set_alpha(75)
                                        delete = False
                                        for i in map:
                                            intens = 0
                                            if i.picture == 2:
                                                intens = 4
                                            if i.picture == 13:
                                                intens = 6
                                            if math.fabs(i.x-dark.x)+math.fabs(i.y-dark.y) < (intens-2)*50:
                                                delete = True
                                            elif math.fabs(i.x-dark.x)+math.fabs(i.y-dark.y) < intens*50:
                                                dark.image.set_alpha(75)
                                        if delete == False:
                                            shadow_new.append(dark)
                                shadow = shadow_new
                            perso.inv.delete()
                            
            if input[K_DOWN]:
                if not (perso.collided_type(0,10,map,Terre) or perso.collided_type(0,10,map,Stone, app, input) or perso.collided_type(0,10,map,Wood, app, input)):
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
                                if isinstance(bloc, Deco):
                                    shadow_new = []
                                    for x in range(16):
                                        for y in range(12):
                                            alpha = 0
                                            for i in shadow:
                                                if i.x == x*50 and i.y == y*50:
                                                    alpha = i.image.get_alpha()
                                            dark = Element()
                                            dark.changer_image(pygame.Surface((50, 50)))
                                            dark.move_el(x*50,y*50)
                                            if alpha == 75:
                                                dark.image.set_alpha(75)
                                            delete = False
                                            for i in map:
                                                intens = 0
                                            if i.picture == 2:
                                                intens = 4
                                            if i.picture == 13:
                                                intens = 6
                                            if math.fabs(i.x-dark.x)+math.fabs(i.y-dark.y) < (intens-2)*50:
                                                delete = True
                                            elif math.fabs(i.x-dark.x)+math.fabs(i.y-dark.y) < intens*50:
                                                dark.image.set_alpha(75)
                                    if delete == False:
                                        shadow_new.append(dark)
                                    shadow = shadow_new
                                perso.inv.delete()

            if input[K_UP]:
                if not perso.collided_type(0,-50,map,Terre):
                    if not perso.collided_type(0,-50,map,Stone, app, input):
                        perso.collided_type(0,-50,map,Wood, app, input)


            #input[K_z] = 0
            #input[K_w] = 0


        if (input[K_e]):
            perso.inv.changer_select(-1)
            input[K_e] = 0
        if (input[K_r]):
            perso.inv.changer_select(1)
            input[K_r] = 0
        if (input[K_i]):
            atelier(app, perso, "Inventory")
            input[K_i] = 0
        # Zoom
        if (input[K_v]):
            app.coef+=1
            if app.coef > 2:
                app.coef = 1
            input[K_v] = 0
        if input[K_UP] and  perso.vie > 0:
            perso.monter_echelle(map)
        if input[K_LEFT] and  perso.vie > 0:
            perso.move(-5,0, map)
            perso.sens = False
            perso.anim(True)
        if input[K_RIGHT] and  perso.vie > 0:
            perso.move(5,0, map)
            perso.sens = True
            perso.anim(True)
        if not input[K_RIGHT] and not input[K_LEFT]:
            perso.anim(False)
        if input[K_RETURN]:
            if perso.vie <= 0:
                perso.vie = 6
                for i in map:
                    if isinstance(i, Porte):
                        if i.id == perso.id_porte:
                            perso.move_el(-perso.x, -perso.y)
                            perso.move_el(i.x,i.y)
        if input[K_ESCAPE]:
            input[K_ESCAPE] = 0
            if app.partie[0] != "Gen":
                cmd = menu(app, "Break", ["Resume", "Save game", "Quit"])
            else:
                 cmd = menu(app, "Break", ["Resume", "Quit"])
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
                i.anim()
                app.blit(i)

        for i in mobs:
            i.update(map)
            creat = True
            for dark in shadow:
                if (int(i.x/50) == int(dark.x/50) and int(i.y/50) == int(dark.y/50)):
                    if dark.image.get_alpha() < 255:
                        creat = False
            if creat and i.vie > 0:
                i.update(map)
                app.blit(i)
 
        app.blit(perso)

        src_x = app.perso.x
        src_y = app.perso.y
        intens = 4
        if app.perso.inv.get_item().id == 0:
            if app.perso.inv.get_item().bloc.picture == 13:
                intens = 6
        for dark in shadow:
            if math.fabs(src_x-dark.x)+math.fabs(src_y-dark.y) < (intens-2)*50:
                dark.image.set_alpha(0)
            elif math.fabs(src_x-dark.x)+math.fabs(src_y-dark.y) < intens*50 and dark.image.get_alpha != 75:
                dark.image.set_alpha(75)
            app.blit(dark)

        if app.coef > 1:
            app.scale(app.coef)

        for i in range(6):
            if i < perso.vie:
                coeur.x = 370 + i*15
                app.blit(coeur)
            else:
                coeur_vide.x = 370 + i*15
                app.blit(coeur_vide)


        app.blit(perso.inv.get_element())
        app.blit(b_text_item)
        app.blit(b_text_item2)
        app.blit(w_text_item)
        app.blit(w_text_item2)
        for i in info_b_txt:
            app.blit(i)
        for i in info_w_txt:
            app.blit(i)

        if input[K_TAB]:
            for i in b_commandes:
                app.blit(i)
            for i in w_commandes:
                app.blit(i)

        for i in map:
            if isinstance(i, Sign):
                if perso.collided_bloc(0,0, i):
                    b_txt = []
                    b_txt = write(app,"Sign :\n\n     "+i.txt, 24, 204)
                    w_txt = []
                    w_txt = write(app, "Sign : \n\n     "+i.txt, 20, 200, (255,255,255))
                    for i in b_txt:
                        app.blit(i)
                    for i in w_txt:
                        app.blit(i)

        if perso.vie <= 0:
            b_txt = []
            b_txt = write(app, "Hard luck ! You are dead...\n\n      Press [RETURN] to respawn", 204, 204)
            w_txt = []
            w_txt = write(app, "Hard luck ! You are dead...\n\n      Press [RETURN] to respawn", 200, 200, (255,255,255))
            for i in b_txt:
                app.blit(i)
            for i in w_txt:
                app.blit(i)

        app.flip()



        if perso.map != app.partie[1]:
            if app.partie[0] != "Gen":
                save_map("save/{0}/map{1}".format(app.partie[0], app.partie[1]), map)
            return 1

    return 0
