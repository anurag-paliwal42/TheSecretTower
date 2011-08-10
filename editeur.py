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
import pygame
from pygame.locals import *

from app import *

from event import *
from map import *
from menu import *
from jeu import *
import const

def editeur(app, map, nom):

    input = Input()
    
    fond = Element()
    fond.changer_image(pygame.image.load(const.path_fond1).convert())

    pointeur = element.Element()
    pointeur.changer_image(pygame.image.load("img/pointeur.png").convert_alpha())

    b_txt = []
    b_txt = write(app, "()", 0, 0)
    w_txt = []
    w_txt = write(app, "()", 0, 0, (255,255,255))
    
    blocs = []
    blocs.append(Porte(0,0))
    blocs.append(Bloc(1))
    blocs.append(Bloc(5))
    blocs.append(Bloc(6))
    blocs.append(Lava())
    blocs.append(BlocDanger(4,1))
    blocs.append(Torch(13))
    blocs.append(Terre(7))

    choix=0
    while not input.quit: 
        input.update_event(app)
        pointeur.move_el(-pointeur.x+input.mouse[0], -pointeur.y+input.mouse[1])
        if input.key[K_ESCAPE]:
            input.key[K_ESCAPE] = 0
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
        if input.mousebuttons[4]:
            choix-=1
            if choix < 0:
                choix = len(blocs)-1
            input.mousebuttons[4] = 0
        if input.mousebuttons[5]:
            choix+=1
            if choix > len(blocs)-1:
                choix = 0
            input.mousebuttons[5] = 0
        if input.mousebuttons[1]:
            input.mousebuttons[1] = 0
            for i in map:
                if (i.x == input.get_mouse_bloc()[0] and i.y == input.get_mouse_bloc()[1]):
                    map.remove(i)
            bloc = copy.copy(blocs[choix])
            bloc.move_el(-bloc.x+input.get_mouse_bloc()[0], -bloc.y+input.get_mouse_bloc()[1])
            map.append(bloc)
        if input.mousebuttons[3]:
            input.mousebuttons[3] = 0
            for i in map:
                if (i.x == input.get_mouse_bloc()[0] and i.y == input.get_mouse_bloc()[1]):
                    map.remove(i)

            
        b_txt = []
        b_txt = write(app, str(input.get_mouse_bloc())+"\n"+nom, 0, 0)
        w_txt = []
        w_txt = write(app, str(input.get_mouse_bloc())+"\n"+nom, 2, 2, (255,255,255))
        app.blit(fond)
        for i in map:
            app.blit(i)
        for i in w_txt:
            app.blit(i)
        for i in b_txt:
            app.blit(i)
        blocs[choix].move_el(-blocs[choix].x+pointeur.x+25, -blocs[choix].y+pointeur.y+25) 
        app.blit(blocs[choix])
        app.blit(pointeur)
        app.flip()

    return 0
