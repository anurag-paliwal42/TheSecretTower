#-*-coding:Utf-8 -*

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

# Auteur : Pierre Surply

from perso import *
from mob import *
from bloc import *
from element import *
from event import *
from map import *
from menu import *
from char import *
import const

from time import *
import random

import pygame
from pygame.locals import *


def jeu(app, map, perso):

    input = Input()

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

    pointeur = element.Element()
    pointeur.changer_image(pygame.image.load("img/pointeur.png").convert_alpha())

    # Noir
    shadow = []
    shadow = set_shadow(shadow, map, app.perso)
    dark = Element()
    dark.changer_image(pygame.Surface((50, 50)))
    dark_middle = Element()
    dark_middle.changer_image(pygame.Surface((50, 50)))
    dark_middle.image.set_alpha(75)

    mobs = []
    mobs = popmobs(shadow, map)

                    
    particules = []


    # interface 
    coeur = Element()
    coeur.changer_image(pygame.image.load("img/coeur.png").convert_alpha())
    coeur.y = 540
    coeur_vide = Element()
    coeur_vide.changer_image(pygame.image.load("img/coeur_vide.png").convert_alpha())
    coeur_vide.y = 540

    b_fond_barre_energie = Element()
    b_fond_barre_energie.changer_image(pygame.Surface((102,12)))
    b_fond_barre_energie.image.fill(pygame.Color(0,0,0, 255))
    b_fond_barre_energie.move_el(372,568)
    fond_barre_energie = Element()
    fond_barre_energie.changer_image(pygame.Surface((100,10)))
    fond_barre_energie.image.fill(pygame.Color(255,255,255, 255))
    fond_barre_energie.move_el(373,569)
    barre_energie = Element()
    barre_energie.changer_image(pygame.Surface((100,10)))
    barre_energie.image.fill(pygame.Color(255,180,40, 255))
    barre_energie.move_el(373,569)
    energie = Element()
    energie.changer_image(pygame.image.load("img/energie.png").convert_alpha())
    energie.move_el(383,569)
    
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
    
    fps= 0
    info_b_txt = []
    info_b_txt = write(app, "V. "+str(const.version)+"\nFPS : "+str(fps)+"\nGame : "+app.partie[0], 4, 4)
    info_w_txt = []
    info_w_txt = write(app, "V. "+str(const.version)+"\nFPS : "+str(fps)+"\nGame : "+app.partie[0], 0, 0, (255,255,255))

    commandes =  "(Space) : Jump\n(Mouse Left) : Hit\n(TAB) : Sprint\n(Mouse Right) : Use/Put a bloc\n(Mouse scroll) : Scroll inventory\n(i) : Inventory \n(v) : Change View\n(ESC) : Break"
    b_commandes = []
    b_commandes = write(app,commandes, 24, 64)
    w_commandes = []
    w_commandes = write(app, commandes, 20, 60, (255,255,255))


    #>> Multi
    # Nom joueurs
    nom_player_b = Element()
    nom_player_w = Element()
    #last_reset = time()

    
    cmd = 1
    prev = time()+1

    if app.partie[0] == "Multi":
        map = const.map

    while not input.quit:
        if app.partie[0] == "Multi":
            for i in const.msg:
                const.chatbox.add(i)
            const.msg = []
            const.input_udp="set_pos;"+str(perso.x)+";"+str(perso.y)+";"+str(perso.v_x+perso.tend_x)+";"+str(perso.v_y)+";"+str(int(perso.sens))+";"+str(int(perso.hitting))+";"+str(int(perso.fired))+";"+str(int(perso.issprinting))+";"+str(perso.bras[0])+";"+str(perso.bras[1])
            for event in const.events_map:
                buffer = event.split(";")
                const.events_map.remove(event)
                if len(buffer) > 1:
                    print buffer
                    if buffer[1] == "hit_block":
                        x = int(buffer[2])
                        y = int(buffer[3])
                        damage = float(buffer[4])
                        for i in map:
                            if i.x == x and i.y == y:
                                if i.hit(damage, False):
                                    map.remove(i)
                    if buffer[1] == "destroy_block":
                        x = int(buffer[2])
                        y = int(buffer[3])
                        for i in map:
                            if i.x == x and i.y == y:
                                    map.remove(i)
                    if buffer[1] == "set_block":
                        x = int(buffer[2])
                        y = int(buffer[3])
                        for i in map:
                            if i.x == x and i.y == y:
                                    map.remove(i)
                        map.append(char2bloc(buffer[4]))            
                    if buffer[1] == "lock_chest":
                        x = int(buffer[2])
                        y = int(buffer[3])
                        for i in map:
                            if i.x == x and i.y == y:
                                if isinstance(i, Coffre):
                                    i.lock = bool(int(buffer[4]))
                    elif buffer[1] == "add_block":
                        map.append(char2bloc(buffer[2]))
                    

        # controle fps
        fps = int(1/(time() - prev))
        while fps > const.fps: 
            fps = int(1/(time() - prev))

        info_b_txt = []
        info_b_txt = write(app, "V. "+str(const.version)+"\nFPS : "+str(fps)+"\nGame : "+app.partie[0]+"\nPlayer : "+perso.nom, 4, 4)
        info_w_txt = []
        info_w_txt = write(app, "V. "+str(const.version)+"\nFPS : "+str(fps)+"\nGame : "+app.partie[0]+"\nPlayer : "+perso.nom, 0, 0, (255,255,255))
        prev = time()

        barre_energie.image = pygame.transform.scale(barre_energie.image, (int(perso.energie),10))
        if perso.inv.get_item().nbr > 1:
            b_text_item2.changer_text("x" + str(perso.inv.get_item().nbr) , app.font_petit)
            w_text_item2.changer_text("x" + str(perso.inv.get_item().nbr) , app.font_petit, (255,255,255))
        else : 
            b_text_item2.changer_text("" , app.font_petit)
            w_text_item2.changer_text("" , app.font_petit, (255,255,255))

        # Shadow
        shadow = []
        shadow = set_shadow(shadow, map, app.perso)

        # Physique Liquide
        for i in map:
            if isinstance(i, Liquid):
                i.chuter(map)
                #i.put_nbr(app.font)
                if i.unit < 0.1:
                    map.remove(i)
        # Reset Blocs
        #if time()-last_reset > 10:
        #    last_reset = time()
        #    for i in copy.copy(map):
        #        if isinstance(i, Liquid):
        #            i.fixe = False
            

        # Hit perso
        for i in mobs:
            i.collided_perso(0,0, perso)

        # Traitement events
        input.update_event(app)
        
        pointeur.move_el(-pointeur.x+input.mouse[0], -pointeur.y+input.mouse[1])
        if const.chatbox.writing:
            const.chatbox.input = input.write(const.chatbox.input, True)
            
        # Sprint
        """
        if  input.key[K_LSHIFT]:
            if time() > perso.sprint_lock:
                perso.issprinting = True
        else:
            perso.issprinting = False 
            """
        if input.key[K_SPACE] and input.key[K_a] and perso.issprinting and  perso.vie > 0 and not const.chatbox.writing:
            perso.sauter(-5, -15, map)
            input.key[K_SPACE] = 0

        elif input.key[K_SPACE] and input.key[K_d] and perso.issprinting and  perso.vie > 0 and not const.chatbox.writing:
            perso.sauter(5, -15, map)
            input.key[K_SPACE] = 0

        if input.key[K_SPACE] and  perso.vie > 0 and not const.chatbox.writing:
            perso.sauter(0, -15, map)
            input.key[K_SPACE] = 0 

        if input.get_mouse(app)[0] >= perso.x+25:
            perso.sens = True
        else:
            perso.sens = False

        if input.mousebuttons[1] and time()-perso.last_hit > 0.3 and perso.vie >0:
            last_hit = time()
            perso.hit()
            if app.coef == 1:
                coord = (int(input.mouse[0]/50)*50, int(input.mouse[1]/50)*50)
            else:
                coord = (int((input.mouse[0]+app.pos_screen[0])/100)*50, int((input.mouse[1]+app.pos_screen[1])/100)*50)
            if math.sqrt((coord[0]-perso.x)**2 + (coord[1]-perso.y)**2) < 100:
                if not isinstance(perso.inv.get_item(), Item_Bloc):
                    perso.collided_type(-perso.x+coord[0],-perso.y+coord[1],map,Terre, particules)
                    perso.collided_type(-perso.x+coord[0],-perso.y+coord[1],map,Stone, particules)
                    perso.collided_type(-perso.x+coord[0],-perso.y+coord[1],map,Wood, particules)
                    perso.collided_type(-perso.x+coord[0],-perso.y+coord[1], map, Deco)
                    perso.collided_mob(mobs, particules)

                
        if input.mousebuttons[3] and perso.vie >0:
            perso.hit()
            input.mousebuttons[3] = 0
            if app.coef == 1:
                coord = (int(input.mouse[0]/50)*50, int(input.mouse[1]/50)*50)
            else:
                coord = (int((input.mouse[0]+app.pos_screen[0])/100)*50, int((input.mouse[1]+app.pos_screen[1])/100)*50)
            if math.sqrt((coord[0]-perso.x)**2 + (coord[1]-perso.y)**2) < 100:
                if isinstance(perso.inv.get_item(), Item_Bloc):

                    bloc = perso.inv.get_item().type(perso.inv.get_item().bloc.picture)
                    bloc.move_el(coord[0], coord[1])
                    if not perso.collided_bloc(0,0,bloc):
                        collided = False
                        for i in map:
                            if i.x == bloc.x and i.y == bloc.y:
                                collided = True
 
                        if not collided:
                            map.append(bloc) 
                            const.input.append("add_block;"+bloc2char(bloc))
                            perso.inv.delete()
                else:
                    perso.collided_utils(-perso.x+coord[0],-perso.y+coord[1],map, app, input)

        if not input.mousebuttons[1] and not input.mousebuttons[3]:
            perso.hitting = False
        if input.mousebuttons[4]:
            perso.inv.changer_select(-1)
            input.mousebuttons[4] = 0
        if input.mousebuttons[5]:
            perso.inv.changer_select(1)
            input.mousebuttons[5] = 0
        if input.key[K_i] and not const.chatbox.writing:
            atelier(app, perso, "Inventory")
            const.input.append("set_inv;"+perso.inv.save())
            input.key[K_i] = 0
        # Zoom
        if input.key[K_v] and not const.chatbox.writing:
            app.coef+=1
            if app.coef > 2:
                app.coef = 1
            input.key[K_v] = 0
        if perso.vie > 0 and not const.chatbox.writing:
            if input.key[K_w]:
                perso.monter_echelle(map)
            if input.key[K_LSHIFT] and time() > perso.sprint_lock:
                if input.key[K_a]:
                    perso.issprinting = True
                    perso.move(-10,0, map)
                    perso.tend_x = -10
                    perso.anim(True)
                    if not perso.isingrav:
                        for it in range(random.randint(1,5)):
                            new_particule = particule.Particule(6)
                            new_particule.move_el(perso.x+40,perso.y+50)
                            particules.append(new_particule)
                elif input.key[K_d]:
                    perso.issprinting = True
                    perso.move(10,0, map)
                    perso.tend_x = 10
                    perso.anim(True)
                    if not perso.isingrav:
                        for it in range(random.randint(1,5)):
                            new_particule = particule.Particule(7)
                            new_particule.move_el(perso.x+10,perso.y+50)
                            particules.append(new_particule)
                else:
                    perso.issprinting = False 
            else:
                perso.issprinting = False
                if input.key[K_a]:
                    perso.move(-5,0, map)
                    perso.tend_x = -5
                    perso.anim(True)
                    if not perso.isingrav:
                        if random.randint(1,5) == 1:
                            new_particule = particule.Particule(8)
                            new_particule.move_el(perso.x+40,perso.y+50)
                            particules.append(new_particule)
                if input.key[K_d]:
                    perso.move(5,0, map)
                    perso.tend_x = 5
                    perso.anim(True)
                    if not perso.isingrav:
                        if random.randint(1,5) == 1:
                            new_particule = particule.Particule(9)
                            new_particule.move_el(perso.x+10,perso.y+50)
                            particules.append(new_particule)
        if not input.key[K_a] and not input.key[K_d]:
            perso.anim(False)
            perso.tend_x = 0
        if input.key[K_RETURN]:
            input.key[K_RETURN] = 0
            if perso.vie <= 0:
                perso.vie = perso.vie_max
                perso.fired = False
                for i in map:
                    if isinstance(i, Porte):
                        if i.id == perso.id_porte:
                            perso.move_el(-perso.x, -perso.y)
                            perso.move_el(i.x,i.y)
                mobs = popmobs(shadow, map)
            elif not const.chatbox.writing and app.partie[0] == "Multi":
                const.chatbox.writing = True
            elif const.chatbox.writing and app.partie[0] == "Multi":
                const.chatbox.writing = False
                const.chatbox.send()
        if input.key[K_ESCAPE]:
            input.key[K_ESCAPE] = 0
            if app.partie[0] != "Gen" and app.partie[0] != "Multi":
                cmd = menu(app, "Break", ["Resume", "Save game", "Quit"])
            else:
                cmd = menu(app, "Break", ["Resume", "Quit"])
            if cmd == 2:
                app.save_partie()
                save_map("save/"+app.partie[0]+"/map"+str(app.partie[1]), map)
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
            i.update(map, perso)
            creat = True
            for coord_dark in shadow:
                if (int(i.x/50) == int(coord_dark[0]/50) and int(i.y/50) == int(coord_dark[1]/50)):
                    if coord_dark[2]:
                        creat = False
            if creat:
                i.update(map, perso)
                app.blit(i)
        for i in particules:
            i.update()
            app.blit(i)
            if time()-i.time_creat > 0.5:
                particules.remove(i)
 
        if app.partie[0] == "Multi":
            for i in const.persos:
                if i.map == perso.map:
                    i.tendance(map)
                    if i.hitting:
                        i.hit()

                    app.blit(i)


        app.blit(perso)

        for coord_dark in shadow:
            if coord_dark[2]:
                dark_middle.move_el(-dark_middle.x+coord_dark[0], -dark_middle.y+coord_dark[1])
                app.blit(dark_middle)
            else:
                dark.move_el(-dark.x+coord_dark[0], -dark.y+coord_dark[1])
                app.blit(dark)

        if app.coef > 1:
            app.scale(app.coef)

        if app.partie[0] == "Multi":
            for i in const.persos:
                if i.map == perso.map:
                    nom_player_b.changer_text(i.nom, app.font_petit, (0,0,0))
                    nom_player_w.changer_text(i.nom, app.font_petit, (255,255,255))
                    if app.coef == 1:
                        nom_player_b.move_el(-nom_player_b.x+i.x, -nom_player_b.y+i.y-8)
                        nom_player_w.move_el(-nom_player_w.x+i.x-2, -nom_player_w.y+i.y-10)
                    else:
                        nom_player_b.move_el(-nom_player_b.x+i.x*2-app.pos_screen[0], -nom_player_b.y+(i.y-8)*2-app.pos_screen[1])
                        nom_player_w.move_el(-nom_player_w.x+(i.x-2)*2-app.pos_screen[0], -nom_player_w.y+(i.y-10)*2-app.pos_screen[1])

                    app.blit(nom_player_b)
                    app.blit(nom_player_w)

        for i in range(perso.vie_max):
            if i < perso.vie:
                coeur.x = 370 + i*15
                app.blit(coeur)
            else:
                coeur_vide.x = 370 + i*15
                app.blit(coeur_vide)


        app.blit(perso.inv.get_element())
        app.blit(b_fond_barre_energie)
        app.blit(fond_barre_energie)
        app.blit(barre_energie)
        app.blit(energie)
        #app.blit(b_text_item)
        app.blit(b_text_item2)
        #app.blit(w_text_item)
        app.blit(w_text_item2)
        for i in info_b_txt:
            app.blit(i)
        for i in info_w_txt:
            app.blit(i)

        if input.key[K_TAB]:
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

        if  app.partie[0] == "Multi":
            const.chatbox.blit_on(app)

        if perso.vie <= 0:
            b_txt = []
            b_txt = write(app, "Hard luck ! You are dead...\n\n      Press [RETURN] to respawn", 204, 204)
            w_txt = []
            w_txt = write(app, "Hard luck ! You are dead...\n\n      Press [RETURN] to respawn", 200, 200, (255,255,255))
            for i in b_txt:
                app.blit(i)
            for i in w_txt:
                app.blit(i)


        app.blit(pointeur)

        app.flip()



        if perso.map != app.partie[1]:
            if app.partie[0] != "Gen" and app.partie[0] != "Multi":
                save_map("save/"+app.partie[0]+"/map"+str(app.partie[1]), map)
            return 1
        if app.partie[1] == 19:
            if mobs[0].vie <= 0:
                cine(app, 2)
                return 5


    if app.partie[0] != "Gen" and app.partie[0] != "Multi":
        app.save_partie()
        save_map("save/"+app.partie[0]+"/map"+str(app.partie[1]), map)
    return 0

def set_shadow(shadow, map, perso):
    intens_perso = 4
    if perso.inv.get_item().id == 0:
        if perso.inv.get_item().bloc.picture == 13:
            intens_perso = 6
    shadow_new = []
    for x in range(16):
        for y in range(12):
            alpha = 0
            for i in shadow:
                if i.x == x*50 and i.y == y*50:
                    alpha = i.image.get_alpha()
            coord_dark = [x*50,y*50, False]
            if alpha == 75:
                coord_dark[2]=True
            delete = False
            if math.fabs(perso.x-coord_dark[0])+math.fabs(perso.y-coord_dark[1]) < (intens_perso-2)*50:
                delete = True
            elif math.fabs(perso.x-coord_dark[0])+math.fabs(perso.y-coord_dark[1]) < intens_perso*50:
                coord_dark[2] = True
            for i in const.persos:
                if math.fabs(i.x-coord_dark[0])+math.fabs(i.y-coord_dark[1]) < (4-2)*50 and i.map == perso.map:
                    delete = True
                elif math.fabs(i.x-coord_dark[0])+math.fabs(i.y-coord_dark[1]) < 4*50 and i.map == perso.map:
                    coord_dark[2] = True
            for i in map:
                intens = 0
                if i.picture == 2:
                    intens = 4
                if i.picture == 13:
                    intens = 6
                if intens !=0:
                    if math.fabs(i.x-coord_dark[0])+math.fabs(i.y-coord_dark[1]) < (intens-2)*50:
                        delete = True
                    elif math.fabs(i.x-coord_dark[0])+math.fabs(i.y-coord_dark[1]) < intens*50:
                        coord_dark[2] = True
            if delete == False:
                shadow_new.append(coord_dark)                        
    return shadow_new


def popmobs(shadow, map):
    mobs = []
    popmob = False
    for bloc in map:
        if isinstance(bloc, PopMob):
            mob = Mob(3)
            mob.move_el(bloc.x, bloc.y-50)
            mobs.append(mob)
            popmob = True
            
    if const.mobs and not popmob:
        for i in shadow:
            # pop monstre
            if random.randint(1, 5) == 1:
                creat = True
                for bloc in map:
                    if bloc.x == i[0] and bloc.y == i[1]:
                        creat = False
                if creat:
                    mob = Mob(random.randint(0,2))
                    mob.move_el(i[0], i[1])
                    mobs.append(mob)
    return mobs
