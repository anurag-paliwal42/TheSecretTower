#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

from bloc import *

# Pygame
import pygame
from pygame.locals import *
 
class Inventaire():
    def __init__(self):
        self.data = []
        self.item_sel = 0

    def add(self,objet):
        if isinstance(objet, Item):
            item = Item(1,1)
            item = objet
            for i in self.data:
                if i.id == item.id:
                    i.nbr = i.nbr + item.nbr
                    return True
        elif isinstance(objet, Bloc):
            item = Item_Bloc(objet)
            for i in self.data:
                if isinstance(i, Item_Bloc):
                    if i.type == item.type:
                        i.nbr = i.nbr + item.nbr
                        return True
        self.data.append(item)
        return True
    def delete(self):
        if self.data[self.item_sel].nbr > 1:
            self.data[self.item_sel].nbr = self.data[self.item_sel].nbr - 1
        else:
            self.data.remove(self.data[self.item_sel])
            self.item_sel = 0

    def get_element(self):
        return self.data[self.item_sel].element

    def get_item(self):
        return self.data[self.item_sel]

    def changer_select(self, step):
        if self.item_sel +1 < len(self.data): 
            self.item_sel = self.item_sel + 1
        else:
            self.item_sel = 0
  
class Item():
    
    def __init__(self, id, nbr):
        self.id = id
        self.element = Element()
        if (id != 0):
            self.element.changer_image(pygame.image.load("img/bloc{0}.png".format(id)).convert())
            self.element.image.set_alpha(200)
            self.element.move_el(320,540)
        if id == 1:
            self.nom = "Epee"
        elif id == 2:
            self.nom = "Pelle"
        elif id == 3:
            self.nom = "Pioche"
        self.nbr = nbr
        
class Item_Bloc(Item):
    
    def __init__(self, bloc):
        Item.__init__(self,0, 1)
        self.element.changer_image(pygame.image.load("img/bloc{0}.png".format(bloc.picture)).convert())
        self.element.image.set_alpha(200)
        self.bloc = bloc
        self.type = bloc.__class__
        self.element.move_el(320,540)
        if self.type == Terre:
            self.nom = "Terre"
