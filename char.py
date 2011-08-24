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

from element import *

# Pygame
import pygame
from pygame.locals import *

from time import *
import re

last_color = (-1,-1,-1)

def write(app, string, x, y, pcolor = (0,0,0), pas=15):
    global last_color
    strings = string.split("\n")
    texte = []
    for i in strings:
        temp = Element()
        if pcolor == "Auto": 
            if re.search(".*>.", i):
                color = const.color_basic
            elif re.search("\[Server\].", i):
                color = const.color_important
            elif last_color != (-1,-1,-1):
                color = last_color
                last_color = (-1,-1,-1)
            else:
                color = const.color_annonce
            if re.search("-$", i):
                last_color = color
        else:
            color = pcolor
        temp.changer_text(i, app.font_petit, color)

        temp.move_el(x, y)
        texte.append(temp)
        y += pas

    return texte

class Chatbox():
    
    def __init__(self):
        self.x = 5
        self.y = 400
        self.len = 25
        self.time_appear = 20
        
        self.line_b = []
        self.line_w = []
        self.input_line_w = Element()
        self.input_line_b = Element()
        self.input = ""
        self.output = ""
        self.writing = False
        self.time_line = [0]*10
        self.last_blink = time()

        # Background
        self.background = Element()
        self.background.changer_image(pygame.Surface((350, 205)))
        self.background.image.set_alpha(200)
        self.background.move_el(0,395)

        self.add(" \n \n \n \n \n \n \n \n \n \n")

    def blit_on(self,app):
        self.draw(app)
        if self.writing:
            app.blit(self.background)
            app.blit(self.input_line_b)
            app.blit(self.input_line_w)
        for i in range(len(self.line_b)):
            if time()-self.time_line[i] < self.time_appear or self.writing:
                app.blit(self.line_b[i])
                app.blit(self.line_w[i])

    def send(self, prefixe=""):
        if self.input != "":
            const.input.append("say;"+prefixe+self.input)
            self.input = ""

    def add(self,buffer):
        if buffer != "":
            if len(buffer) > self.len:
                buffer_s = buffer.split("\n")
                buffer_s = [self.split(i) for i in buffer_s]
                buffer = "\n".join(buffer_s)
            self.output += "\n"+buffer
        line = self.output.split("\n")
        while len(line)>10:
            del line[0]
            self.output = "\n".join(line)
            del self.time_line[0]
            self.time_line.append(time())
            line = self.output.split("\n")
 
    def split(self, buffer):
        if len(buffer) > self.len:
            buffer = buffer[:self.len]+"-\n"+self.split(buffer[self.len:])
        return buffer

    def draw(self, app):
        self.line_w = write(app, self.output, self.x, self.y, "Auto")
        self.line_b = write(app, self.output, self.x+2, self.y+2, (0,0,0))
        if time() >= self.last_blink:
            suffixe = "|"  
        else:
            suffixe = ""            
        if time()-self.last_blink > 0.5:
            self.last_blink = time()+0.5

        self.input_line_w.changer_text("> "+self.input+suffixe, app.font_petit, (255,255,255))
        self.input_line_b.changer_text("> "+self.input+suffixe, app.font_petit, (0,0,0))
        self.input_line_w.move_el(-self.input_line_w.x+5,-self.input_line_w.y+580)
        self.input_line_b.move_el(-self.input_line_b.x+7,-self.input_line_b.y+582)
        
        
                
        
        
