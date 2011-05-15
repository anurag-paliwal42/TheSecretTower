#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

import pygame
from pygame.locals import *

from app import *

def menu(app):
    fond_menu = Element()
    fond_menu.changer_image(pygame.image.load(const.path_fond_menu).convert())

    img_choix = Element()
    img_choix.changer_image(pygame.image.load(const.path_choix).convert_alpha())
    img_choix.x = 30
    img_choix.y = 300
    
    entry = Element()
    entry.changer_text("Nouvelle Partie", app.font)

    menu = []
    menu.append(entry)

    entry = Element()
    entry.changer_text("Charger Partie", app.font)
    menu.append(entry)


    cmd = 1

    while cmd<>0:
        # Evenement
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    img_choix.y = 350
                    cmd = 2
                if event.key == K_UP:
                    img_choix.y = 300
                    cmd = 1
                if event.key == K_RETURN or event.key == K_SPACE:
                    return cmd
            if event.type == QUIT:
                cmd = 0
                return cmd
        
        # Affichage
        app.blit(fond_menu)
                
        x = 100
        y = 300
        for entry in menu:
            entry.x = x
            entry.y = y
            app.blit(entry)
            y = y + 50
        
        app.blit(img_choix)
            
        app.flip()
