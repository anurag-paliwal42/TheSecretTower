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

class Input:
    def __init__(self):
        self.key = [0]*1000
        self.mouse = (0,0)
        self.mouserel = (0,0)
        self.mousebuttons= [0]*9
        self.quit = False

    # Met à jour les events
    def update_event(self, app):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                self.key[event.key] = 1;
            if event.type == KEYUP:
                self.key[event.key] = 0;
            if event.type == MOUSEMOTION:
                self.mouse = event.pos
                self.mouserel = event.rel
            if event.type == MOUSEBUTTONDOWN:
                self.mousebuttons[event.button] = 1
            if event.type == MOUSEBUTTONUP:
                if event.button != 4 and event.button != 5:
                    self.mousebuttons[event.button] = 0
            if event.type == QUIT:
                self.quit = True
                return False
            if event.type == VIDEORESIZE:
                app.set_size(event.size)
                app.size = event.size

        return True

    def write(self, preponse):
        if self.key[K_a]:
            preponse += "a"
            self.key[K_a] = 0
        elif self.key[K_z]:
            preponse +="z"
            self.key[K_z] = 0
        elif self.key[K_e]:
            preponse +="e"
            self.key[K_e] = 0
        elif self.key[K_r]:
            preponse += "r"
            self.key[K_r] = 0
        elif self.key[K_t]:
            preponse += "t"
            self.key[K_t] = 0
        elif self.key[K_y]:
            preponse += "y"
            self.key[K_y] = 0
        elif self.key[K_u]:
            preponse += "u"
            self.key[K_u] = 0
        elif self.key[K_i]:
            preponse += "i"
            self.key[K_i] = 0
        elif self.key[K_o]:
            preponse += "o"
            self.key[K_o] = 0
        elif self.key[K_p]:
            preponse += "p"
            self.key[K_p] = 0
        elif self.key[K_q]:
            preponse += "q"
            self.key[K_q] = 0
        elif self.key[K_s]:
            preponse += "s"
            self.key[K_s] = 0
        elif self.key[K_d]:
            preponse += "d"
            self.key[K_d] = 0
        elif self.key[K_f]:
            preponse += "f"
            self.key[K_f] = 0
        elif self.key[K_g]:
            preponse += "g"
            self.key[K_g] = 0
        elif self.key[K_h]:
            preponse += "h"
            self.key[K_h] = 0
        elif self.key[K_j]:
            preponse += "j"
            self.key[K_j] = 0
        elif self.key[K_k]:
            preponse += "k"
            self.key[K_k] = 0
        elif self.key[K_l]:
            preponse += "l"
            self.key[K_l] = 0
        elif self.key[K_m]:
            preponse += "m"
            self.key[K_m] = 0
        elif self.key[K_w]:
            preponse += "w"
            self.key[K_w] = 0
        elif self.key[K_x]:
            preponse += "x"
            self.key[K_x] = 0
        elif self.key[K_c]:
            preponse += "c"
            self.key[K_c] = 0
        elif self.key[K_v]:
            preponse += "v"
            self.key[K_v] = 0
        elif self.key[K_b]:
            preponse += "b"
            self.key[K_b] = 0
        elif self.key[K_n]:
            preponse += "n"
            self.key[K_n] = 0
        elif self.key[K_KP0]:
            preponse += "0"
            self.key[K_KP0] = 0
        elif self.key[K_KP1]:
            preponse += "1"
            self.key[K_KP1] = 0
        elif self.key[K_KP2]:
            preponse += "2"
            self.key[K_KP2] = 0
        elif self.key[K_KP3]:
            preponse += "3"
            self.key[K_KP3] = 0
        elif self.key[K_KP4]:
            preponse += "4"
            self.key[K_KP4] = 0
        elif self.key[K_KP5]:
            preponse += "5"
            self.key[K_KP5] = 0
        elif self.key[K_KP6]:
            preponse += "6"
            self.key[K_KP6] = 0
        elif self.key[K_KP7]:
            preponse += "7"
            self.key[K_KP7] = 0
        elif self.key[K_KP8]:
            preponse += "8"
            self.key[K_KP8] = 0
        elif self.key[K_KP9]:
            preponse += "9"
            self.key[K_KP9] = 0
        elif self.key[K_0]:
            preponse += "0"
            self.key[K_0] = 0
        elif self.key[K_1]:
            preponse += "1"
            self.key[K_1] = 0
        elif self.key[K_2]:
            preponse += "2"
            self.key[K_2] = 0
        elif self.key[K_3]:
            preponse += "3"
            self.key[K_3] = 0
        elif self.key[K_4]:
            preponse += "4"
            self.key[K_4] = 0
        elif self.key[K_5]:
            preponse += "5"
            self.key[K_5] = 0
        elif self.key[K_6]:
            preponse += "6"
            self.key[K_6] = 0
        elif self.key[K_7]:
            preponse += "7"
            self.key[K_7] = 0
        elif self.key[K_8]:
            preponse += "8"
            self.key[K_8] = 0
        elif self.key[K_9]:
            preponse += "9"
            self.key[K_9] = 0
        elif self.key[K_BACKSPACE]:
            preponse = preponse[0:-1]
            self.key[K_BACKSPACE] = 0
        return preponse

    def get_mouse(self, app):
        if app.coef != 1:
            return ((self.mouse[0]+app.pos_screen[0])/2, (self.mouse[1]+app.pos_screen[1])/2)
        else:
            return self.mouse

    def get_mouse_bloc(self):
        return (int(self.mouse[0]/50)*50, int(self.mouse[1]/50)*50)

    def reset(self):
        self.key = [0]*1000
        self.mouse = (0,0)
        self.mouserel = (0,0)
        self.mousebuttons= [0]*9
        self.quit = False
