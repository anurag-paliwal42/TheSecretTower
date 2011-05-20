#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

import pygame
from pygame.locals import *

from app import *

from event import *

def menu(app, ptitle, pmenu):

    input = range(0, 1000, 1)

    for i in range(len(input)):
        input[i] = 0

    fond_menu = Element()
    fond_menu.changer_image(pygame.image.load(const.path_fond_menu).convert())

    img_choix = Element()
    img_choix.changer_image(pygame.image.load(const.path_choix).convert_alpha())
    img_choix.x = 30
    img_choix.y = 300

    title = Element()
    title.changer_text(ptitle, app.font)
    title.move_el(80,250)
    
    menu = []

    for i in pmenu:
        entry = Element()
        entry.changer_text(i, app.font)
        menu.append(entry)


    cmd = 1

    while update_event(input):
        # Evenement

        if input[K_UP]:
            if cmd-1 > 0:
                cmd = cmd - 1
            input[K_UP] = 0
        if input[K_DOWN]:
            if cmd+1 <= len(menu):
                cmd = cmd + 1
            input[K_DOWN] = 0
        if input[K_SPACE] or input[K_RETURN]:
            if pmenu[cmd-1] == "Quitter":
                return 0
            return cmd
        
        # Affichage

        img_choix.y = 250 + (cmd*50)
        app.blit(fond_menu)
        app.blit(title)
                
        x = 100
        y = 300
        for entry in menu:
            entry.x = x
            entry.y = y
            app.blit(entry)
            y = y + 50
        
        app.blit(img_choix)
            
        app.flip()

    return 0

