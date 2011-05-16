#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

from perso import *

import pygame
from pygame.locals import *

def jeu(app):
    perso = Perso()
    perso.x = 100
    perso.y = 500

    fond_menu = Element()
    fond_menu.changer_image(pygame.image.load(const.path_fond_menu).convert())

    pygame.key.set_repeat(30, 30)
    
    cmd = 1
    while cmd<>0:
        # Evenement
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    perso.x = perso.x - 10
                    perso.changer_image(perso.perso_g)
                if event.key == K_RIGHT:
                    perso.x = perso.x + 10
                    perso.changer_image(perso.perso_d)
                if event.key == K_SPACE:
                    perso.sauter()
            if event.type == QUIT:
                cmd = 0
                return cmd
        
        perso.tomber()

        app.blit(fond_menu)
        app.blit(perso)
            
        app.flip()
        
    
