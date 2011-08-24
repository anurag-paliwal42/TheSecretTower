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

import re

class Input:
    def __init__(self):
        self.key = [0]*1000
        self.mouse = (0,0)
        self.mouserel = (0,0)
        self.mousebuttons= [0]*9
        self.last_pressed = ""
        self.quit = False

        self.regex_NUMPAD = re.compile("^\[.\]$")

    # Met Ã  jour les events
    def update_event(self, app):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                self.key[event.key] = 1;
                self.last_pressed = pygame.key.name(event.key)
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

    def write(self, preponse, spec = False):
        if self.key[K_BACKSPACE]:
            preponse = preponse[0:-1]
            self.key[K_BACKSPACE] = 0
        buffer = ""
        if self.regex_NUMPAD.search(self.last_pressed):
            buffer = self.last_pressed.replace("[","").replace("]","")
        elif (len(self.last_pressed) == 1 or self.last_pressed in ["space"]) and spec:
            buffer = self.last_pressed.replace("space", " ").replace(";", ":")
        elif (len(self.last_pressed) == 1) and not spec:
            buffer = self.last_pressed.replace(";", "m")
        if self.key[K_RALT] and spec:
            if buffer == "e" or buffer == "2":
                buffer = "é"
            elif buffer == "a" or buffer == "0":
                buffer = "à"
            elif buffer == "q":
                buffer = "â"
            elif buffer == "r" or buffer == "7":
                buffer = "è"
            elif buffer == "f":
                buffer = "ê"
            elif buffer == "d":
                buffer = "ë"
            elif buffer == "h":
                buffer = "ù"
            elif buffer == "j":
                buffer = "ü"
            elif buffer == "k":
                buffer = "ï"
            elif buffer == "u":
                buffer = "û"
            elif buffer == "i":
                buffer = "î"
            elif buffer == "c" or buffer == "9":
                buffer = "ç"
        if self.key[K_LSHIFT] or self.key[K_RSHIFT]:
            if buffer == "1":
                buffer = "!"
            elif buffer == "2":
                buffer = "@"
            elif buffer == "3":
                buffer = "#"
            elif buffer == "4":
                buffer = "$"
            elif buffer == "5":
                buffer = "%"
            elif buffer == "6":
                buffer = "^"
            elif buffer == "7":
                buffer = "&"
            elif buffer == "8":
                buffer = "*"
            elif buffer == "9":
                buffer = "("
            elif buffer == "0":
                buffer = ")"
            elif buffer == "-":
                buffer = "_"
            elif buffer == "=":
                buffer = "+"
            elif buffer == "[":
                buffer = "{"
            elif buffer == "]":
                buffer = "}"
            elif buffer == "'":
                buffer = "\""
            elif buffer == ",":
                buffer = "<"
            elif buffer == ".":
                buffer = ">"
            elif buffer == "/":
                buffer = "?"
            elif buffer == "`":
                buffer = "~"
            else:
                buffer = buffer.upper()

        preponse += buffer
        self.last_pressed = ""
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
