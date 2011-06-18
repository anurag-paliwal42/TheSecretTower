#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

from bloc import *

import copy
import const

# Pygame
import pygame
from pygame.locals import *
 
class Inventaire():
    def __init__(self):
        self.data = []
        self.item_sel = 0

    def add(self,objet):
        if isinstance(objet, Item_Bloc):
            for i in self.data:
                if isinstance(i, Item_Bloc):
                    if i.type == objet.type:
                        i.nbr = i.nbr + objet.nbr
                        return True
            item = objet

        elif isinstance(objet, Item):
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
        self.data[self.item_sel].element.move_el(-self.data[self.item_sel].element.x+320,-self.data[self.item_sel].element.y+540)
        return self.data[self.item_sel].element

    def get_item(self):
        return self.data[self.item_sel]

    def changer_select(self, step):
        if self.item_sel + step < len(self.data) and step > 0: 
            self.item_sel = self.item_sel + step
        elif self.item_sel + step >= 0 and step < 0:
            self.item_sel = self.item_sel + step
        elif step > 0:
            self.item_sel = 0
        else:
            self.item_sel = len(self.data)-1

    def search(self, item):
        for i in range(len(self.data)):
            if self.data[i].id == item.id:
                if item.id == 0:
                    if item.type == self.data[i].type:
                        return i
                else:
                    return i
        return -1

    def isempty(self):
        if self.data == []:
            return True
        else:
            return False
  
class Item():
    
    def __init__(self, id, nbr):
        self.id = id
        self.element = Element()
        if (id != 0):
            image = copy.copy(const.vide)
            rect = pygame.Rect(id*50-50,0, 50,50)
            image.blit(const.sprite_item, (0,0), rect)
            self.element.changer_image(image)
            self.element.move_el(320,540)
        if id == 1:
            self.nom = "Epee"
        elif id == 2:
            self.nom = "Pelle"
        elif id == 3:
            self.nom = "Pioche"
        elif id == 4:
            self.nom = "Hache"
        self.nbr = nbr
        self.prix = Inventaire()

    def set_prix(self, bloc):
        self.prix.add(bloc)

    def achat(self, inv):

        prix = Inventaire()
        prix = copy.copy(self.prix)
        item_sel = inv.item_sel
        item_del = []

        while prix.isempty() == False:
            id_prix = inv.search(prix.get_item())
            inv.item_sel = 0
            if id_prix >= 0:
                inv.changer_select(id_prix)
                item_del.append(inv.get_item())
                inv.delete()
                self.prix.delete()
            else:
                inv.item_sel = item_sel
                for i in item_del:
                    inv.add(i)
                return False
                
            prix.changer_select(1)

        inv.item_sel = item_sel
        return True
        
class Item_Bloc(Item):
    
    def __init__(self, bloc):
        Item.__init__(self,0, 1)
        self.element.changer_image(bloc.image)
        self.bloc = bloc
        self.type = bloc.__class__
        self.element.move_el(320,540)
        if self.type == Terre:
            self.nom = "Terre"
        elif self.type == Stone:
            self.nom = "Pierre"
        elif self.type == Echelle:
            self.nom = "Echelle"
        elif self.type == Wood:
            self.nom = "Bois"
        elif self.type == Atelier:
            self.nom = "Atelier"
        elif self.type == Forge:
            self.nom = "Forge"
        elif self.type == Coffre:
            self.nom = "Coffre"
