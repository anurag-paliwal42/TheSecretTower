#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

from element import *

import pygame
from pygame.locals import *

from time import *

class Bloc(Element):
    
    def __init__(self, picture):
        Element.__init__(self)
        if picture == 1:
            self.changer_image(pygame.image.load("img/bloc1.png").convert())

class BlocDisp(Bloc):
    
    def __init__(self, picture, begin = 0):
        Bloc.__init__(self, picture)
        self.last_change = time()+begin
        self.etat = True

    def disp(self):
        if (time() - self.last_change > 3):
            self.last_change = time()
            if (self.etat == True):
                self.etat = False
            elif (self.etat == False):
                self.etat = True
        
        

class BlocMouvant(Bloc):
    
    def __init__(self, picture, debut_x, debut_y, dep_x, dep_y):
        Bloc.__init__(self, picture)
        self.debut_x = debut_x
        self.debut_y = debut_y
        self.dep_x = dep_x
        self.dep_y = dep_y
        self.move_el(debut_x, debut_y)
        self.aller = True

    def move(self):
        if self.aller:
            if self.x >= (self.debut_x+self.dep_x) and self.y >= (self.debut_y+self.dep_y):
                self.aller = False
            if self.x < self.dep_x+self.debut_x:
                self.move_el(1,0)
            if self.y < self.dep_y+self.debut_y:
                self.move_el(0,1)
            
        else:
            if self.x <= (self.debut_x) and self.y <= (self.debut_y):
                self.aller = True
            if self.x > self.debut_x:
                self.move_el(-1,0)
            if self.y > self.debut_y:
                self.move_el(0,-1)
            
        

            
        
