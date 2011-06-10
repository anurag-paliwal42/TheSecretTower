#-*-coding:Utf-8 -*
# Auteur : Pierre Surply


from event import *
from element import *
from bloc import *
from item import *
import const

import copy

import pygame
from pygame.locals import *

def load_craft(type):
    
    craft = []
    if type == "Atelier":
        
        # Atelier
        bloc = Atelier(9)
        item = Item_Bloc(bloc)
        item.element.move_el(-item.element.x+400,-item.element.y+100)
        prix = Wood(6)
        item.set_prix(prix)
        craft.append(item)

        # Coffre
        bloc = Coffre(11)
        item = Item_Bloc(bloc)
        item.element.move_el(-item.element.x+400,-item.element.y+100)
        prix = Wood(6)
        item.set_prix(prix)
        prix = Wood(6)
        item.set_prix(prix)
        craft.append(item)

        # Forge
        bloc = Forge(10)
        item = Item_Bloc(bloc)
        item.element.move_el(-item.element.x+400,-item.element.y+100)
        prix = Stone(1)
        item.set_prix(prix)
        prix = Stone(1)
        item.set_prix(prix)
        craft.append(item)

    elif type == "Forge":
        
        # Pelle
        item = Item(2, 1)
        item.element.move_el(-item.element.x+400,-item.element.y+100)
        prix = Wood(6)
        item.set_prix(prix)
        prix = Stone(1)
        item.set_prix(prix)
        craft.append(item)

        # Pioche
        item = Item(3,1)
        item.element.move_el(-item.element.x+400,-item.element.y+100)
        prix = Wood(6)
        item.set_prix(prix)
        prix = Stone(1)
        item.set_prix(prix)
        craft.append(item)

        # Hache
        item = Item(4,1)
        item.element.move_el(-item.element.x+400,-item.element.y+100)
        prix = Wood(6)
        item.set_prix(prix)
        prix = Stone(1)
        item.set_prix(prix)
        craft.append(item)

    return craft

def atelier(app, perso, type):

    input = range(0, 1000, 1)

    for i in range(len(input)):
        input[i] = 0

    fond = Element()
    fond.changer_image(pygame.image.load(const.path_fond2).convert())
    
        
    title = Element()
    title.changer_text(type, app.font)
    title.move_el(50, 50)

    choix = 0

    craft = []
    text_craft = []

    craft = load_craft(type)

    x = 100
    y = 100
    for i in craft:
        buffer = Element()
        buffer.changer_text(i.nom, app.font_petit)
        buffer.move_el(x,y)
        text_craft.append(buffer)
        y = y + 20
    text_craft[choix].move_el(20, 0)
    
    title_craft = Element()
    title_craft.changer_text(craft[choix].nom, app.font)
    title_craft.move_el(500, 110)

    description = Element()
    description.changer_text("(c) : Craft   (e) : Scroll inventary  (ESQ): Leave ", app.font_petit)
    description.move_el(100, 500)

    cout = Element()
    cout.changer_text("Cout : ", app.font_petit)
    cout.move_el(350, 175)
    item_cout = Element()
    text_cout = Element()
    text_cout.changer_text("" , app.font_petit)
    
    # Inventaire

    interface = Element()
    interface.changer_image(pygame.image.load("img/interface.png").convert())
    interface.image.set_alpha(150)
    interface.move_el(310, 530)
    text_item = Element()
    text_item.changer_text(perso.inv.get_item().nom , app.font_petit)
    text_item.move_el(380, 565)
    text_item2 = Element()
    text_item2.changer_text("x" + str(perso.inv.get_item().nbr) , app.font_petit)
    text_item2.move_el(380, 580)

    cmd = 1
    while cmd<>0:
        title_craft.changer_text(craft[choix].nom, app.font)

        text_item.changer_text(perso.inv.get_item().nom, app.font_petit)
        if perso.inv.get_item().nbr > 1:
            text_item2.changer_text("x" + str(perso.inv.get_item().nbr) , app.font_petit)
        else : 
            text_item2.changer_text("" , app.font_petit)

            title_craft.changer_text(craft[choix].nom, app.font)

        # Events
        cmd = update_event(input)


      
        if input[K_UP]:
            if choix > 0:
                choix = choix -1
                text_craft[choix].move_el(20, 0)
                text_craft[choix+1].move_el(-20,0)
            else:
                choix = len(craft)-1
                text_craft[choix].move_el(20, 0)
                text_craft[0].move_el(-20,0)
            input[K_UP] = 0
        if input[K_DOWN]:
            if choix < len(craft)-1:
                choix = choix +1
                text_craft[choix].move_el(20, 0)
                text_craft[choix-1].move_el(-20,0)
            else:
                choix = 0
                text_craft[choix].move_el(20, 0)
                text_craft[-1].move_el(-20,0)
            input[K_DOWN] = 0
        if (input[K_e]):
            perso.inv.changer_select(-1)
            input[K_e] = 0
        if (input[K_r]):
            perso.inv.changer_select(1)
            input[K_r] = 0
        if (input[K_c]):
            if craft[choix].achat(perso.inv):
                perso.inv.add(craft[choix])
            craft = load_craft(type)
            input[K_c] = 0

        if input[K_ESCAPE]:
            return 0

        # Affichage
        app.blit(fond)
        app.blit(title)
        
        app.blit(craft[choix].element)
        
        for i in text_craft:
            app.blit(i)
        
        app.blit(title_craft)
        app.blit(description)
        app.blit(cout)

        x = 375
        y = 200
        craft[choix].prix.item_sel = 0
        for i in range(len(craft[choix].prix.data)):
            item_cout = craft[choix].prix.get_item().element
            item_cout.move_el(-item_cout.x+x, -item_cout.y+y)
            app.blit(item_cout)
            if craft[choix].prix.get_item().nbr > 1: 
                text_cout.changer_text("x"+str(craft[choix].prix.get_item().nbr) , app.font_petit)
                text_cout.move_el(-text_cout.x+x+20, -text_cout.y+y+30)
                app.blit(text_cout)
            craft[choix].prix.changer_select(1)
            x = x +60
            

        app.blit(interface)
        app.blit(perso.inv.get_element())
        app.blit(text_item)
        app.blit(text_item2)

        app.flip()
