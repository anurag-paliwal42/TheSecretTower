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


from event import *
from element import *
from bloc import *
from item import *
from char import *
import const

import copy

import pygame
from pygame.locals import *

def load_craft(type):
    
    craft = []

    if type == "Workbench":
        # Coffre
        bloc = Coffre(11)
        Coffre.inv = Inventaire()
        item = Item_Bloc(bloc)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        prix = Wood(6)
        item.set_prix(prix)
        prix = Wood(6)
        item.set_prix(prix)
        craft.append(item)

        # Sign
        bloc = Sign(22)
        item = Item_Bloc(bloc)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Wood(6))
        item.set_prix(Item(5,1))
        craft.append(item)

        # Forge
        bloc = Forge(10)
        item = Item_Bloc(bloc)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        prix = Stone(6)
        item.set_prix(prix)
        prix = Stone(6)
        item.set_prix(prix)
        craft.append(item)

        # Four
        bloc = Furnace(23)
        item = Item_Bloc(bloc)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        prix = Stone(6)
        item.set_prix(prix)
        craft.append(item)

        # Echelle
        bloc = Echelle(8)
        item = Item_Bloc(bloc)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(5,5))
        craft.append(item)

    elif type == "Forge":
        # ---- Stone
        # Hache
        item = Item(4,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Stone(1))
        item.set_prix(Stone(1))
        item.set_prix(Stone(1))
        item.set_prix(Item(5,2))
        craft.append(item)

        # Pioche
        item = Item(3,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Stone(1))
        item.set_prix(Stone(1))
        item.set_prix(Item(5,2))
        craft.append(item)

        # Epee
        item = Item(1,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Stone(1))
        item.set_prix(Stone(1))
        item.set_prix(Item(5,1))
        craft.append(item)

        # Pelle
        item = Item(2, 1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        prix = Item(5,2)
        item.set_prix(prix)
        prix = Stone(1)
        item.set_prix(prix)
        craft.append(item)

        # ---- Bronze
        # Hache
        item = Item(9,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(10,3))
        item.set_prix(Item(5,2))
        craft.append(item)

        # Pioche
        item = Item(8,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(10,2))
        item.set_prix(Item(5,2))
        craft.append(item)

        # Epee
        item = Item(6,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(10,2))
        item.set_prix(Item(5,1))
        craft.append(item)

        # Pelle
        item = Item(7, 1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        prix = Item(5,2)
        item.set_prix(prix)
        item.set_prix(Item(10,1))
        craft.append(item)

        # ---- Fer
        # Hache
        item = Item(14,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(15,3))
        item.set_prix(Item(5,2))
        craft.append(item)

        # Pioche
        item = Item(13,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(15,2))
        item.set_prix(Item(5,2))
        craft.append(item)

        # Epee
        item = Item(11,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(15,2))
        item.set_prix(Item(5,1))
        craft.append(item)

        # Pelle
        item = Item(12, 1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        prix = Item(5,2)
        item.set_prix(prix)
        item.set_prix(Item(15,1))
        craft.append(item)

        # ---- Steel
        # Hache
        item = Item(19,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(20,3))
        item.set_prix(Item(5,2))
        craft.append(item)

        # Pioche
        item = Item(18,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(20,2))
        item.set_prix(Item(5,2))
        craft.append(item)

        # Epee
        item = Item(16,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(20,2))
        item.set_prix(Item(5,1))
        craft.append(item)

        # Pelle
        item = Item(17, 1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        prix = Item(5,2)
        item.set_prix(prix)
        item.set_prix(Item(20,1))
        craft.append(item)

        # ---- Titane
        # Hache
        item = Item(24,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(25,3))
        item.set_prix(Item(5,2))
        craft.append(item)

        # Pioche
        item = Item(23,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(25,2))
        item.set_prix(Item(5,2))
        craft.append(item)

        # Epee
        item = Item(21,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(25,2))
        item.set_prix(Item(5,1))
        craft.append(item)

        # Pelle
        item = Item(22, 1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        prix = Item(5,2)
        item.set_prix(prix)
        item.set_prix(Item(25,1))
        craft.append(item)

        # ---- Uranium
        # Hache
        item = Item(29,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(30,3))
        item.set_prix(Item(5,2))
        craft.append(item)

        # Pioche
        item = Item(28,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(30,2))
        item.set_prix(Item(5,2))
        craft.append(item)

        # Epee
        item = Item(26,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(30,2))
        item.set_prix(Item(5,1))
        craft.append(item)

        # Pelle
        item = Item(27, 1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        prix = Item(5,2)
        item.set_prix(prix)
        item.set_prix(Item(30,1))
        craft.append(item)



    elif type == "Furnace":
        # Cuivre
        item = Item(31,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item_Bloc(Copper(15)))
        craft.append(item)

        # Etain
        item = Item(32,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item_Bloc(Tin(20)))
        craft.append(item)

        # Bronze
        item = Item(10,3)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(31,2))
        item.set_prix(Item(32,1))
        craft.append(item)

        # Fer
        item = Item(15,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item_Bloc(Iron(16)))
        craft.append(item)

        # Steel
        item = Item(20,2)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(15,1))
        item.set_prix(Item(34,1))
        craft.append(item)

        # Titane
        item = Item(25,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item_Bloc(Titanium(17)))
        craft.append(item)
        # Uranium
        item = Item(30,1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item_Bloc(Uranium(21)))
        craft.append(item)


        

    # Atelier
    bloc = Atelier(9)
    item = Item_Bloc(bloc)
    item.element.move_el(-item.element.x+500,-item.element.y+310)
    prix = Wood(6)
    item.set_prix(prix)
    prix = Wood(6)
    item.set_prix(prix)
    craft.append(item)
    # Torch
    item = Item_Bloc(Torch(13))
    item.nbr = 4
    item.element.move_el(-item.element.x+500,-item.element.y+310)
    item.set_prix(Item(5, 1))
    item.set_prix(Item(34,1))
    craft.append(item)
    # Stick
    item = Item(5, 8)
    item.element.move_el(-item.element.x+500,-item.element.y+310)
    prix = Wood(6)
    item.set_prix(prix)
    craft.append(item)



    return craft

def atelier(app, perso, type, chest = None):

    input = Input()

    fond = Element()
    fond.changer_image(app.save_screen())
    pointeur = Element()
    pointeur.changer_image(pygame.image.load("img/pointeur.png").convert_alpha())
    if type != "Chest":
        fond.image.blit(pygame.image.load("img/fond_inv.png").convert_alpha(), (0,0))
    else:
        fond.image.blit(pygame.image.load("img/fond_chest.png").convert_alpha(), (0,0))
    
    if type == "Inventory":
        symb = copy.copy(const.vide)
    if type == "Chest":
        symb = copy.copy(const.vide)
    if type == "Workbench":
        symb = Atelier(9)
        symb.move_el(520, 170)
    if type == "Forge":
        symb = Forge(10)
        symb.move_el(520, 170)
    if type == "Furnace":
        symb = Furnace(23)
        symb.last = chest.last
        symb.fire = chest.fire
        symb.move_el(520, 170)
    

    craft = []
    text_craft = []

    craft = load_craft(type)

    
    title_craft = Element()
    title_craft.changer_text("", app.font)
    title_craft.move_el(560, 320)
    title_craft2 = Element()
    title_craft2.changer_text("", app.font)
    title_craft2.move_el(560, 335)

    if type != "Chest" and type != "Furnace":
        description = write(app, "(p) : Put down the item \n      for crafting\n(c) : Craft\n(x) : Cancel\n(ESQ): Resume", 20, 380)
    elif type == "Chest":
        description = write(app, "(p) : Swap the Item\n(TAB) : Switch the cursor\n(ESQ): Resume", 20, 380)
    elif type == "Furnace":
        description = write(app, "(p) : Put down the item \n      for crafting\n(b) : Use as fuel\n(c) : Craft\n(x) : Cancel\n(ESQ): Resume", 20, 380)
    # depot
    if type != "Chest":
        depot = Inventaire(2)
    else:
        depot = chest.inv

    # Inventaire
    select = Element()
    select.changer_image(pygame.image.load("img/select.png").convert_alpha())
    text_nbr = Element()
    text_nbr.changer_text("", app.font)

    choix = 0
    side = True

    cmd = 1
    while not input.quit:
        # Events
        input.update_event(app)
        pointeur.move_el(-pointeur.x+input.mouse[0], -pointeur.y+input.mouse[1])
        
        for i in range(len(perso.inv.data)):
            if input.mouse[1] > 100+(int(i/5)*60) and input.mouse[1] < 150+(int(i/5)*60) and input.mouse[0] > 20+((i%5)*60) and input.mouse[0] < 70+((i%5)*60):
                perso.inv.item_sel = 0
                perso.inv.changer_select(i)
                if not side:
                    side = True
        if type == "Chest":
            for i in range(len(depot.data)):
                if input.mouse[1] > 100+(int(i/5)*60) and input.mouse[1] < 150+(int(i/5)*60) and input.mouse[0] > 730-((i%5)*60) and input.mouse[0] < 780-((i%5)*60):
                    depot.item_sel = 0
                    depot.changer_select(i)
                    if side:
                        side = False

        if input.key[K_UP]:
            if side:
                perso.inv.changer_select(-5)
            else:
                depot.changer_select(-5)
            input.key[K_UP] = 0
        if input.key[K_DOWN]:
            if side:
                perso.inv.changer_select(5)
            else:
                depot.changer_select(5)
            input.key[K_DOWN] = 0
        if input.key[K_RIGHT]:
            if side:
                perso.inv.changer_select(1)
            else:
                depot.changer_select(-1)
            input.key[K_RIGHT] = 0
        if input.key[K_LEFT]:
            if side:
                perso.inv.changer_select(-1)
            else:
                depot.changer_select(1)
            input.key[K_LEFT] = 0
        if input.key[K_p] or (input.mousebuttons[1] and input.mouse[1] > 90 and input.mouse[1] < 340 and ((side and input.mouse[0] > 10 and input.mouse[0] < 320) or (not side and input.mouse[0] > 480 and input.mouse[0] < 790))):
            input.key[K_p] = 0
            input.mousebuttons[1] = 0
            if side:
                if perso.inv.get_item().id != 1 and not depot.isfull(perso.inv.get_item()):
                    depot.add(copy.copy(perso.inv.get_item()), 1)
                    perso.inv.delete()
            else:
                if not perso.inv.isfull(depot.get_item()):
                    perso.inv.add(copy.copy(depot.get_item()), 1)
                    depot.delete()
                    if depot.isempty():
                        side = True
            
        if (input.key[K_c] or (input.mousebuttons[1] and input.mouse[0] > 480 and input.mouse[0] < 790 and input.mouse[1] > 300 and input.mouse[1] < 370)):
            if type != "Chest":
                if type == "Furnace":
                    if chest.fire:
                        for i in craft:
                            i.prix.item_sel = 0
                            if not perso.inv.isfull(i):
                                if i.achat(depot):
                                    perso.inv.add(i)
                                    break
                else:        
                    for i in craft:
                        i.prix.item_sel = 0
                        if not perso.inv.isfull(i):
                            if i.achat(depot):
                                perso.inv.add(i)
                                break
            input.key[K_c] = 0

        if (input.key[K_b] or (input.mousebuttons[3] and input.mouse[0] > 10 and input.mouse[0] < 320 and input.mouse[1] > 90 and input.mouse[1] < 340)):
            if type == "Furnace":
                if perso.inv.get_item().id ==34:
                    perso.inv.delete()
                    chest.last = time() + 120
                    symb.last = time() + 120
            input.key[K_b] = 0
            input.mousebuttons[3] = 0

        if (input.key[K_s] or input.key[K_TAB]):
            if type == "Chest":
                if side and not depot.isempty():
                    side = False
                else:
                    side = True
                depot.item_sel = 0
                perso.inv.item_sel=0
            input.key[K_s] = 0
            input.key[K_TAB] = 0

        if (input.key[K_x] or (input.mousebuttons[1] and input.mouse[0] > 480 and input.mouse[0] < 790 and input.mouse[1] > 90 and input.mouse[1] < 160)):
            if type != "Chest":
                for i in depot.data:
                    perso.inv.add(i)

                depot = Inventaire()
            input.key[K_x] = 0

        if input.key[K_ESCAPE] or input.key[K_i]:
            if type != "Chest":
                for i in depot.data:
                    perso.inv.add(i)

                depot = Inventaire(2)
            return 0

        # Affichage
        app.blit(fond)
        
        if type != "Chest":
            for i in craft:

                inv_temp = copy.deepcopy(depot)
                i.prix.item_sel = 0
                if i.achat(inv_temp):
                    title_craft.changer_text(i.nom, app.font)
                    if i.nbr > 1:
                        title_craft2.changer_text("x" + str(i.nbr) , app.font)
                    else : 
                        title_craft2.changer_text("" , app.font)

                    app.blit(i.element)
                    app.blit(title_craft)
                    app.blit(title_craft2)
                    choix = i 
                    break
            craft = load_craft(type)
            

        # Affichage inventaire
        x = 20
        y = 100
        for i in perso.inv.data:
            i.element.move_el(-i.element.x+x,-i.element.y+y)
            app.blit(i.element)
            if i.nbr > 1:
                text_nbr.changer_text(str(i.nbr) , app.font_petit)
                text_nbr.move_el(-text_nbr.x+x+27,-text_nbr.y+y+32)
                app.blit(text_nbr)
                text_nbr.changer_text(str(i.nbr) , app.font_petit, (255,255,255))
                text_nbr.move_el(-text_nbr.x+x+25,-text_nbr.y+y+30)
                app.blit(text_nbr)
            if i == perso.inv.get_item() and side:
                select.move_el(-select.x+x,-select.y+y) 
                app.blit(select)
                b_txt = []
                b_txt = write(app,i.nom, x, y+45)
                w_txt = []
                w_txt = write(app,i.nom, x+2, y+47, (255,255,255))
                for i in w_txt:
                    app.blit(i)
                for i in b_txt:
                    app.blit(i)

            x += 60
            if x+60 > 360:
                x = 20 
                y += 60

        x = 730
        y = 100
        for i in depot.data:
            i.element.move_el(-i.element.x+x,-i.element.y+y)
            app.blit(i.element)
            if i.nbr > 1:
                text_nbr.changer_text(str(i.nbr) , app.font_petit)
                text_nbr.move_el(-text_nbr.x+x+27,-text_nbr.y+y+32)
                app.blit(text_nbr)
                text_nbr.changer_text(str(i.nbr) , app.font_petit, (255,255,255))
                text_nbr.move_el(-text_nbr.x+x+25,-text_nbr.y+y+30)
                app.blit(text_nbr)
            if i == depot.get_item() and not side:
                select.move_el(-select.x+x,-select.y+y) 
                app.blit(select)
                b_txt = []
                b_txt = write(app,i.nom, x, y+45)
                w_txt = []
                w_txt = write(app,i.nom, x+2, y+47, (255,255,255))
                for i in w_txt:
                    app.blit(i)
                for i in b_txt:
                    app.blit(i)
            x -= 60
            if x-60 < 400:
                x = 730 
                y += 60
        for i in description:                                
            app.blit(i)
        if type == "Furnace":
            symb.anim()
            chest.anim()
        app.blit(symb)
        app.blit(pointeur)
        app.flip()

    for i in depot.data:
        perso.inv.add(i)
        
