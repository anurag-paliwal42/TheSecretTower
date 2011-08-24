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

from bloc import *

import copy
import const

# Pygame
import pygame
from pygame.locals import *
 
class Inventaire():
    def __init__(self, limit=20, ctrl=False):
        self.data = []
        self.item_sel = 0
        self.limit = limit
        self.ctrl = ctrl

    def add(self,objet, nbr = 0):
        if isinstance(objet, Item_Bloc):
            for i in self.data:
                if isinstance(i, Item_Bloc):
                    if i.type == objet.type and i.nbr<8:
                        if nbr == 0:
                            i.nbr = i.nbr + objet.nbr
                        else:
                            i.nbr += nbr
                        return True
            item = objet
            if nbr != 0:
                item.nbr = nbr

        elif isinstance(objet, Item):
            item = Item(1,1)
            item = objet
            if nbr != 0:
                item.nbr = nbr
            for i in self.data:
                if i.id == item.id and i.nbr<8:
                    if nbr == 0:
                        i.nbr = i.nbr + item.nbr
                    else:
                        i.nbr += nbr
                    return True

        elif isinstance(objet, Bloc):
            item = Item_Bloc(objet)
            if nbr != 0:
                item.nbr = nbr
            for i in self.data:
                if isinstance(i, Item_Bloc):
                    if i.type == item.type and i.nbr<8:
                        if nbr == 0:
                            i.nbr = i.nbr + item.nbr
                        else:
                            i.nbr += nbr
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
        elif step < 0:
            self.item_sel =len(self.data)-1

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
        if len(self.data) == 0:
            return True
        else:
            return False

    def empty(self):
        self.data[:] = []
        self.item_sel = 0

    def isfull(self, item):
        if isinstance(item, Bloc):
            item = Item_Bloc(item)
        if len(self.data) >= self.limit:
            for i in self.data:
                if i.id == item.id and i.nbr < 8:
                    if item.id == 0:
                        if item.type == i.type:
                            return False
                    else:
                        return False
                    
            return True
        else:
            return False

    def load(self, buffer):
        if len(buffer) > 0: 
            items = buffer.split("/")
            for item in items:
                param = item.split("-")
                param = [int(i) for i in param]
                if param[0] == 0:
                    if param[1] == 1:
                        bloc = Terre(7)
                    elif param[1] == 2:
                        bloc = Stone(1)
                    elif param[1] == 3:
                        bloc = Wood(6)
                    elif param[1] == 4:
                        bloc = Echelle(8)
                    elif param[1] == 5:
                        bloc = Atelier(9)
                    elif param[1] == 6:
                        bloc = Forge(10)
                    elif param[1] == 7:
                        bloc = Coffre(11)
                    elif param[1] == 8:
                        bloc = Coal(14)
                    elif param[1] == 9:
                        bloc = Copper(15)
                    elif param[1] == 10:
                        bloc = Iron(16)
                    elif param[1] == 11:
                        bloc = Titanium(17)
                    elif param[1] == 12:
                        bloc = Gold(18)
                    elif param[1] == 13:
                        bloc = Diamond(19)
                    elif param[1] == 14:
                        bloc = Torch(13)
                    elif param[1] == 15:
                        bloc = Furnace(23)
                    elif param[1] == 16:
                        bloc = Tin(20)
                    elif param[1] == 17:
                        bloc = Uranium(21)
                    elif param[1] == 18:
                        bloc = Sign(22)
                    new_item = Item_Bloc(bloc)

                    new_item.nbr = param[2]
                else:
                    new_item = Item(param[1], param[2])

                self.add(new_item)


    def save(self):
        buffer = ""
        for i in self.data:
            buffer = buffer + str(i.id)+ "-"
            if i.id == 0:
                if i.type == Terre:
                    buffer += "1"
                elif i.type == Stone:
                    buffer += "2"
                elif i.type == Echelle:
                    buffer += "4"
                elif i.type == Wood:
                    buffer += "3"
                elif i.type == Atelier:
                    buffer += "5"
                elif i.type == Forge:
                    buffer += "6"
                elif i.type == Coffre:
                    buffer += "7"
                elif i.type == Torch:
                    buffer += "14"
                elif i.type == Coal:
                    buffer += "8"
                elif i.type == Copper:
                    buffer += "9"
                elif i.type == Iron:
                    buffer += "10"
                elif i.type == Titanium:
                    buffer += "11"
                elif i.type == Gold:
                    buffer += "12"
                elif i.type == Diamond:
                    buffer += "13"
                elif i.type == Furnace:
                    buffer += "15"
                elif i.type == Tin:
                    buffer += "16"
                elif i.type == Uranium:
                    buffer += "17"
                elif i.type == Sign:
                    buffer += "18"

            else:
                buffer += str(i.id)
                
            buffer += "-" + str(i.nbr) + "/"
        
        if len(buffer) > 2:
            buffer = buffer[0:-1]
        return buffer

class Coffre(Wood):
    def __init__(self, picture):
        Bloc.__init__(self, picture)
        self.inv = Inventaire()
        self.lock = False
  
class Item():
    
    def __init__(self, id, nbr):
        self.id = id
        self.atk = 0
        self.element = Element()
        if (id != 0):
            if const.display:
                image = copy.copy(const.vide)
                if id%5 != 0:
                    rect = pygame.Rect((id%5)*50-50,int(id/5)*50, 50,50)
                else:
                    rect = pygame.Rect(200,int(id/5)*50-50, 50,50)
                image.blit(const.sprite_item, (0,0), rect)
                self.element.changer_image(image)
                self.element.move_el(320,540)
            self.atk = 1
            self.damage = 0
        if id == 1:
            self.nom = "Stone Sword"
            self.atk = 4
            self.damage = 0.2 
        elif id == 2:
            self.nom = "Stone Shovel"
            self.atk = 0.5
            self.damage = 1
        elif id == 3:
            self.nom = "Stone Pickaxe"
            self.atk = 2
            self.damage=0.4
        elif id == 4:
            self.nom = "Stone Axe"
            self.atk = 3
            self.damage=0.4
        elif id == 5:
            self.nom = "Stick"
            self.atk = 1
        elif id == 6:
            self.nom = "Bronze Sword"
            self.atk = 5
            self.damage = 0.2
        elif id == 7:
            self.nom = "Bronze Shovel"
            self.atk = 2
            self.damage = 0.7
        elif id == 8:
            self.nom = "Bronze Pickaxe"
            self.atk = 3
            self.damage=0.5
        elif id == 9:
            self.nom = "Bronze Axe"
            self.atk = 4
            self.damage=0.5
        elif id == 10:
            self.nom = "Bronze Ingot"
        elif id == 11:
            self.nom = "Iron Sword"
            self.atk = 8
            self.damage = 0.2
        elif id == 12:
            self.nom = "Iron Shovel"
            self.atk = 3
            self.damage = 1
        elif id == 13:
            self.nom = "Iron Pickaxe"
            self.atk = 4
            self.damage=0.7
        elif id == 14:
            self.nom = "Iron Axe"
            self.atk = 5
            self.damage=0.7
        elif id == 15:
            self.nom = "Iron Ingot"
        elif id == 16:
            self.nom = "Steel Sword"
            self.atk = 10
            self.damage = 0.2
        elif id == 17:
            self.nom = "Steel Shovel"
            self.atk = 4
            self.damage = 2
        elif id == 18:
            self.nom = "Steel Pickaxe"
            self.atk = 5
            self.damage=1
        elif id == 19:
            self.nom = "Steel Axe"
            self.atk = 6
            self.damage=1
        elif id == 20:
            self.nom = "Steel Ingot"
        elif id == 21:
            self.nom = "Titanium Sword"
            self.atk = 15
            self.damage = 0.2
        elif id == 22:
            self.nom = "Titanium Shovel"
            self.atk = 5
            self.damage = 2.5
        elif id == 23:
            self.nom = "Titanium Pickaxe"
            self.atk = 6
            self.damage=2
        elif id == 24:
            self.nom = "Titanium Axe"
            self.atk = 7
            self.damage=2
        elif id == 25:
            self.nom = "Titanium Ingot"
        elif id == 26:
            self.nom = "Uranium Sword"
            self.atk = 50
            self.damage = 0.2
        elif id == 27:
            self.nom = "Uranium Shovel"
            self.atk = 6
            self.damage = 5
        elif id == 28:
            self.nom = "Uranium Pickaxe"
            self.atk = 7
            self.damage=2.5
        elif id == 29:
            self.nom = "Uranium Axe"
            self.atk = 8
            self.damage=2.5
        elif id == 30:
            self.nom = "Uranium Ingot"
        elif id == 31:
            self.nom = "Copper Ingot"
        elif id == 32:
            self.nom = "Tin Ingot"
        elif id == 33:
            self.nom = "Gloden Ingot"
        elif id == 34:
            self.nom = "Coal"
        elif id == 35:
            self.nom = "Diamond"

        self.nbr = nbr
        self.prix = Inventaire()

    def set_prix(self, bloc):
        self.prix.add(bloc)

    def achat(self, inv):

        prix = Inventaire()
        prix = copy.copy(self.prix)
        prix.item_sel = 0
        item_sel = inv.item_sel
        item_del = []
        while prix.isempty() == False:
            id_prix = inv.search(prix.get_item())
            inv.item_sel = 0
            if id_prix >= 0:
                inv.changer_select(id_prix)
                item_del.append(inv.get_item())
                inv.delete()
                prix.delete()
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
        if const.display:
            self.element.changer_image(bloc.image)
        self.bloc = bloc
        self.type = bloc.__class__
        self.element.move_el(320,540)
        if self.type == Terre:
            self.nom = "Dirt"
        elif self.type == Stone:
            self.nom = "Stone"
        elif self.type == Echelle:
            self.nom = "Ladder"
        elif self.type == Wood:
            self.nom = "Wood"
        elif self.type == Atelier:
            self.nom = "Workbench"
        elif self.type == Forge:
            self.nom = "Forge"
        elif self.type == Coffre:
            self.nom = "Chest"
        elif self.type == Torch:
            self.nom = "Torch"
        elif self.type == Sign:
            self.nom = "Sign"
        elif self.type == Coal:
            self.nom = "Coal"
        elif self.type == Copper:
            self.nom = "Copper"
        elif self.type == Iron:
            self.nom = "Iron"
        elif self.type == Titanium:
            self.nom = "Titanium"
        elif self.type == Gold:
            self.nom = "Gold"
        elif self.type == Diamond:
            self.nom = "Diamond"
        elif self.type == Tin:
            self.nom = "Tin"
        elif self.type == Uranium:
            self.nom = "Uranium"
        elif self.type == Furnace:
            self.nom = "Furnace"
