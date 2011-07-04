#-*-coding:Utf-8 -*
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
        item = Item_Bloc(bloc)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        prix = Wood(6)
        item.set_prix(prix)
        prix = Wood(6)
        item.set_prix(prix)
        item.nbr = 2
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

        # Echelle
        bloc = Echelle(8)
        item = Item_Bloc(bloc)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        item.set_prix(Item(5,5))
        craft.append(item)

    elif type == "Forge":
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

        # Pelle
        item = Item(2, 1)
        item.element.move_el(-item.element.x+500,-item.element.y+310)
        prix = Item(5,2)
        item.set_prix(prix)
        prix = Stone(1)
        item.set_prix(prix)
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
    item = Item_Bloc(Deco(13))
    item.nbr = 4
    item.element.move_el(-item.element.x+500,-item.element.y+310)
    item.set_prix(Item(5, 1))
    item.set_prix(Coal(14))
    craft.append(item)
    # Stick
    item = Item(5, 8)
    item.element.move_el(-item.element.x+500,-item.element.y+310)
    prix = Wood(6)
    item.set_prix(prix)
    craft.append(item)



    return craft

def atelier(app, perso, type):

    input = range(0, 1000, 1)

    for i in range(len(input)):
        input[i] = 0

    fond = Element()
    fond.changer_image(app.save_screen())
    fond.image.blit(pygame.image.load("img/fond_inv.png").convert_alpha(), (0,0))
    
    if type == "Inventory":
        symb = copy.copy(const.vide)
    if type == "Workbench":
        symb = Atelier(9)
        symb.move_el(520, 170)
    if type == "Forge":
        symb = Forge(10)
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

    description = write(app, "(p) : Put down the item \n      for crafting\n(c) : Craft\n(x) : Cancel\n(ESQ): Resume", 20, 380)
    
    # depot
    depot = Inventaire()

    # Inventaire
    select = Element()
    select.changer_image(pygame.image.load("img/select.png").convert_alpha())
    text_nbr = Element()
    text_nbr.changer_text("", app.font)

    choix = 0

    cmd = 1
    while cmd<>0:


        # Events
        cmd = update_event(input, app)


      
        if input[K_UP]:
            perso.inv.changer_select(-5)

            input[K_UP] = 0
        if input[K_DOWN]:
            perso.inv.changer_select(5)
            input[K_DOWN] = 0
        if input[K_RIGHT]:
            perso.inv.changer_select(1)
            input[K_RIGHT] = 0
        if input[K_LEFT]:
            perso.inv.changer_select(-1)
            input[K_LEFT] = 0
        if (input[K_p]):
            input[K_p] = 0
            if perso.inv.get_item().id != 1:
                depot.add(copy.copy(perso.inv.get_item()), 1)
                perso.inv.delete()
            
        if (input[K_c]):
            for i in craft:
                i.prix.item_sel = 0
                if i.achat(depot):
                    perso.inv.add(i)
                    break
            input[K_c] = 0

        if (input[K_x]):
            # Cancel
            for i in depot.data:
                perso.inv.add(i)

            depot = Inventaire()
            input[K_x] = 0

        if input[K_ESCAPE] or input[K_i]:
            for i in depot.data:
                perso.inv.add(i)

            depot = Inventaire()
            return 0

        # Affichage
        app.blit(fond)
        
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
            if i == perso.inv.get_item():
                select.move_el(-select.x+x,-select.y+y) 
                app.blit(select)
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
            x -= 60
            if x-60 < 400:
                x = 730 
                y += 60
        for i in description:                                
            app.blit(i)
        app.blit(symb)

        app.flip()

    for i in depot.data:
        perso.inv.add(i)
        
