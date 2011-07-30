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

import pygame
from pygame.locals import *

from app import *
import const
from event import *


def menu(app, ptitle, pmenu):

    input = range(0, 1000, 1)

    for i in range(len(input)):
        input[i] = 0

    fond_menu = Element()
    fond_menu.changer_image(pygame.image.load(const.path_fond_menu).convert())

    img_choix = Element()
    img_choix.changer_image(pygame.image.load(const.path_choix).convert_alpha())
    img_choix.x = 30
    img_choix.y = 300


    w_title = Element()
    w_title.changer_text(ptitle, app.font, (255,255,255))
    w_title.move_el(84,254)
    title = Element()
    title.changer_text(ptitle, app.font)
    title.move_el(80,250)
    
    menu = []
    w_menu = []

    for i in pmenu:
        # White
        entry = Element()
        entry.changer_text(i, app.font, (255,255,255))
        w_menu.append(entry)
        # Black
        entry = Element()
        entry.changer_text(i, app.font)
        menu.append(entry)


    cmd = 1

    while update_event(input, app):
        # Evenement

        if input[K_UP]:
            if cmd-1 > 0:
                cmd = cmd - 1
            input[K_UP] = 0
        if input[K_DOWN]:
            if cmd+1 <= len(menu):
                cmd = cmd + 1
            input[K_DOWN] = 0
        if input[K_SPACE] or input[K_RETURN]:
            if pmenu[cmd-1] == "Quit":
                return 0
            return cmd
        
        # Affichage

        img_choix.y = 250 + (cmd*50)
        app.blit(fond_menu)
        app.blit(w_title)
        app.blit(title)

        x = 104
        y = 304
        for entry in w_menu:
            entry.x = x
            entry.y = y
            app.blit(entry)
            y = y + 50
                
        x = 100
        y = 300
        for entry in menu:
            entry.x = x
            entry.y = y
            app.blit(entry)
            y = y + 50
        
        app.blit(img_choix)
            
        app.flip()

    return 0

def ask(app, ptitle):
    
    input = range(0, 1000, 1)

    for i in range(len(input)):
        input[i] = 0

    fond_menu = Element()
    fond_menu.changer_image(pygame.image.load(const.path_fond_menu).convert())

    w_title = Element()
    w_title.changer_text(ptitle, app.font, (255,255,255))
    w_title.move_el(84,254)
    title = Element()
    title.changer_text(ptitle, app.font)
    title.move_el(80,250)

    preponse = ""
    w_reponse = Element()
    w_reponse.changer_text(preponse, app.font, (255,255,255))
    w_reponse.move_el(104, 304)
    reponse = Element()
    reponse.changer_text(preponse, app.font)
    reponse.move_el(100, 300)

    while 1:
        update_event(input, app)
        if input[K_a]:
            preponse = preponse+"a"
            input[K_a] = 0
        elif input[K_z]:
            preponse = preponse+"z"
            input[K_z] = 0
        elif input[K_e]:
            preponse = preponse+"e"
            input[K_e] = 0
        elif input[K_r]:
            preponse = preponse+"r"
            input[K_r] = 0
        elif input[K_t]:
            preponse = preponse+"t"
            input[K_t] = 0
        elif input[K_y]:
            preponse = preponse+"y"
            input[K_y] = 0
        elif input[K_u]:
            preponse = preponse+"u"
            input[K_u] = 0
        elif input[K_i]:
            preponse = preponse+"i"
            input[K_i] = 0
        elif input[K_o]:
            preponse = preponse+"o"
            input[K_o] = 0
        elif input[K_p]:
            preponse = preponse+"p"
            input[K_p] = 0
        elif input[K_q]:
            preponse = preponse+"q"
            input[K_q] = 0
        elif input[K_s]:
            preponse = preponse+"s"
            input[K_s] = 0
        elif input[K_d]:
            preponse = preponse+"d"
            input[K_d] = 0
        elif input[K_f]:
            preponse = preponse+"f"
            input[K_f] = 0
        elif input[K_g]:
            preponse = preponse+"g"
            input[K_g] = 0
        elif input[K_h]:
            preponse = preponse+"h"
            input[K_h] = 0
        elif input[K_j]:
            preponse = preponse+"j"
            input[K_j] = 0
        elif input[K_k]:
            preponse = preponse+"k"
            input[K_k] = 0
        elif input[K_l]:
            preponse = preponse+"l"
            input[K_l] = 0
        elif input[K_m]:
            preponse = preponse+"m"
            input[K_m] = 0
        elif input[K_w]:
            preponse = preponse+"w"
            input[K_w] = 0
        elif input[K_x]:
            preponse = preponse+"x"
            input[K_x] = 0
        elif input[K_c]:
            preponse = preponse+"c"
            input[K_c] = 0
        elif input[K_v]:
            preponse = preponse+"v"
            input[K_v] = 0
        elif input[K_b]:
            preponse = preponse+"b"
            input[K_b] = 0
        elif input[K_n]:
            preponse = preponse+"n"
            input[K_n] = 0
        elif input[K_KP0]:
            preponse = preponse+"0"
            input[K_KP0] = 0
        elif input[K_KP1]:
            preponse = preponse+"1"
            input[K_KP1] = 0
        elif input[K_KP2]:
            preponse = preponse+"2"
            input[K_KP2] = 0
        elif input[K_KP3]:
            preponse = preponse+"3"
            input[K_KP3] = 0
        elif input[K_KP4]:
            preponse = preponse+"4"
            input[K_KP4] = 0
        elif input[K_KP5]:
            preponse = preponse+"5"
            input[K_KP5] = 0
        elif input[K_KP6]:
            preponse = preponse+"6"
            input[K_KP6] = 0
        elif input[K_KP7]:
            preponse = preponse+"7"
            input[K_KP7] = 0
        elif input[K_KP8]:
            preponse = preponse+"8"
            input[K_KP8] = 0
        elif input[K_KP9]:
            preponse = preponse+"9"
            input[K_KP9] = 0
        elif input[K_0]:
            preponse = preponse+"0"
            input[K_0] = 0
        elif input[K_1]:
            preponse = preponse+"1"
            input[K_1] = 0
        elif input[K_2]:
            preponse = preponse+"2"
            input[K_2] = 0
        elif input[K_3]:
            preponse = preponse+"3"
            input[K_3] = 0
        elif input[K_4]:
            preponse = preponse+"4"
            input[K_4] = 0
        elif input[K_5]:
            preponse = preponse+"5"
            input[K_5] = 0
        elif input[K_6]:
            preponse = preponse+"6"
            input[K_6] = 0
        elif input[K_7]:
            preponse = preponse+"7"
            input[K_7] = 0
        elif input[K_8]:
            preponse = preponse+"8"
            input[K_8] = 0
        elif input[K_9]:
            preponse = preponse+"9"
            input[K_9] = 0
        elif input[K_BACKSPACE]:
            preponse = preponse[0:-1]
            input[K_BACKSPACE] = 0
        elif input[K_RETURN]:
            return preponse

        w_reponse.changer_text(preponse, app.font, (255,255,255))
        reponse.changer_text(preponse, app.font)
        app.blit(fond_menu)
        app.blit(w_title)
        app.blit(title)
        app.blit(w_reponse)
        app.blit(reponse)

        app.flip()
