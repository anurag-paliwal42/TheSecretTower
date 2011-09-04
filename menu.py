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

import pygame
from pygame.locals import *


import app
import element
import const
import event
import char
import bloc
import mob
import particule

import random
from time import *


def menu(app, ptitle, pmenu, perso=None):

    input = event.Input()

    fond_menu = element.Element()
    fond_menu.changer_image(pygame.image.load(const.path_fond_menu).convert())

    img_choix = element.Element()
    img_choix.changer_image(pygame.image.load(const.path_choix).convert_alpha())
    img_choix.x = 30
    img_choix.y = 300

    pointeur = element.Element()
    pointeur.changer_image(pygame.image.load("img/pointeur.png").convert_alpha())


    w_title = element.Element()
    w_title.changer_text(ptitle, app.font, (255,255,255))
    w_title.move_el(84,254)
    title = element.Element()
    title.changer_text(ptitle, app.font)
    title.move_el(80,250)
    
    menu = []
    w_menu = []

    

    for i in pmenu:
        # White
        entry = element.Element()
        entry.changer_text(i, app.font, (255,255,255))
        w_menu.append(entry)
        # Black
        entry = element.Element()
        entry.changer_text(i, app.font)
        menu.append(entry)


    cmd = 1

    while input.update_event(app):
        # Evenement
        pointeur.move_el(-pointeur.x+input.mouse[0], -pointeur.y+input.mouse[1])
        for i in range(1,1+len(menu)):
            if input.mouse[1] > 250+(i*50) and input.mouse[1] < 300+(i*50):
                cmd = i
                img_choix.y= 250+(cmd*50)
        if input.key[K_SPACE] or input.key[K_RETURN] or input.mousebuttons[1]:
            input.key[K_RETURN] = 0
            const.click.play()
            if pmenu[cmd-1] == "Quit":
                return 0
            return cmd
        
        # Affichage
        app.blit(fond_menu)
        if perso != None:
            perso.move_el(-perso.x+400, -perso.y+300)
            app.blit(perso, 3)
        app.blit(w_title)
        app.blit(title)

        x = 104
        y = 304
        for entry in w_menu:
            entry.x = x
            entry.y = y
            app.blit(entry)
            y = y + 50
                
        x = 100
        y = 300
        for entry in menu:
            entry.x = x
            entry.y = y
            app.blit(entry)
            y = y + 50
        
        app.blit(img_choix)
        app.blit(pointeur)
            
        app.flip()

    return 0

def menu_color(app, id_color, perso):

    input = event.Input()

    fond_menu = element.Element()
    fond_menu.changer_image(pygame.image.load(const.path_fond_menu).convert())

    img_choix = element.Element()
    img_choix.changer_image(pygame.image.load(const.path_choix).convert_alpha())
    img_choix.x = 30
    img_choix.y = 300

    pointeur = element.Element()
    pointeur.changer_image(pygame.image.load("img/pointeur.png").convert_alpha())

    ptitle = ""
    if id_color == 0:
        ptitle = "Shirt's color"
    if id_color == 1:
        ptitle = "Pants's color"
    if id_color == 2:
        ptitle = "Hair's color"
    if id_color == 3:
        ptitle = "Skin's color"
    if id_color == 4:
        ptitle = "Other colors"
    w_title = element.Element()
    w_title.changer_text(ptitle, app.font, (255,255,255))
    w_title.move_el(84,254)
    title = element.Element()
    title.changer_text(ptitle, app.font)
    title.move_el(80,250)
    
    apercu = element.Element()
    apercu.image = pygame.Surface((150, 30))
    apercu.image.fill(perso.color[id_color])
    apercu.x = 400
    apercu.y = 460

    cmd = 1

    while input.update_event(app):
        apercu.image.fill(perso.color[id_color])
        pmenu = ["Red : "+str(perso.color[id_color].r),"Green : "+str(perso.color[id_color].g),"Blue : "+str(perso.color[id_color].b), "Apply","Reset", "Done"]
        menu = []
        w_menu = []
        for i in pmenu:
            # White
            entry = element.Element()
            entry.changer_text(i, app.font, (255,255,255))
            w_menu.append(entry)
            # Black
            entry = element.Element()
            entry.changer_text(i, app.font)
            menu.append(entry)

        # Evenement
        pointeur.move_el(-pointeur.x+input.mouse[0], -pointeur.y+input.mouse[1])
        for i in range(1,1+len(menu)):
            if input.mouse[1] > 250+(i*50) and input.mouse[1] < 300+(i*50):
                cmd = i
                img_choix.y= 250+(cmd*50)
        if input.key[K_SPACE] or input.key[K_RETURN] or input.mousebuttons[1]:
            input.key[K_RETURN] = 0
            if cmd == 4:
                perso.update_color()
            if cmd == 5:
                perso.set_org_color(id_color)
            elif cmd == 6:
                return 0
            elif cmd == 1 and perso.color[id_color].r < 255:
                perso.color[id_color].r+=1
            elif cmd == 2 and perso.color[id_color].g < 255:
                perso.color[id_color].g+=1
            elif cmd == 3 and perso.color[id_color].b < 255:
                perso.color[id_color].b+=1
        if input.mousebuttons[3]:
            if cmd == 1 and perso.color[id_color].r > 0:
                perso.color[id_color].r-=1
            elif cmd == 2 and perso.color[id_color].g > 0:
                perso.color[id_color].g-=1
            elif cmd == 3 and perso.color[id_color].b > 0:
                perso.color[id_color].b-=1

        
        # Affichage
        app.blit(fond_menu)
        perso.move_el(-perso.x+400, -perso.y+300)
        app.blit(perso, 3)
        app.blit(w_title)
        app.blit(title)

        x = 104
        y = 304
        for entry in w_menu:
            entry.x = x
            entry.y = y
            app.blit(entry)
            y = y + 50
                
        x = 100
        y = 300
        for entry in menu:
            entry.x = x
            entry.y = y
            app.blit(entry)
            y = y + 50
        
        app.blit(img_choix)
        app.blit(apercu)
        app.blit(pointeur)
            
        app.flip()

    return 0


def ask(app, ptitle):
    
    input = event.Input()

    fond_menu = element.Element()
    fond_menu.changer_image(pygame.image.load(const.path_fond_menu).convert())

    w_title = element.Element()
    w_title.changer_text(ptitle, app.font, (255,255,255))
    w_title.move_el(84,254)
    title = element.Element()
    title.changer_text(ptitle, app.font)
    title.move_el(80,250)

    preponse = ""
    w_reponse = element.Element()
    w_reponse.changer_text(preponse, app.font, (255,255,255))
    w_reponse.move_el(104, 304)
    reponse = element.Element()
    reponse.changer_text(preponse, app.font)
    reponse.move_el(100, 300)

    last_blink = time()

    while 1:
        input.update_event(app)
        preponse = input.write(preponse).capitalize()

        if input.key[K_RETURN]:
            input.key[K_RETURN] = 0
            if preponse != "":
                return preponse.strip()

        if time() >= last_blink:
            suffixe = "|"  
        else:
            suffixe = ""            
        if time()-last_blink > 0.5:
            last_blink = time()+0.5
        w_reponse.changer_text(preponse+suffixe, app.font, (255,255,255))
        reponse.changer_text(preponse+suffixe, app.font)
        app.blit(fond_menu)
        app.blit(w_title)
        app.blit(title)
        app.blit(w_reponse)
        app.blit(reponse)

        app.flip()

def cine(app, id):
    input = event.Input()

    fond = element.Element()
    if id == 1:
        fond.changer_image(pygame.image.load(const.path_fond_menu).convert())
    elif id == 2:
        fond.changer_image(pygame.image.load(const.path_fond1).convert())
    img_choix = element.Element()
    img_choix.changer_image(pygame.image.load(const.path_choix).convert_alpha())
    img_choix.x = 30
    img_choix.y = 300

    pointeur = element.Element()
    pointeur.changer_image(pygame.image.load("img/pointeur.png").convert_alpha())
    fps= 0
    prev = time()+1
    pos_txt = (0,0)

    if id==1:
        txt = "dfgdgdfgdgdf\ngfdgfdfgfg\nfdgfdgfdgfgdfg\n"
        app.perso.move_el(-app.perso.x+10, -app.perso.y+500)
        pos_txt = (80,200)
    elif id == 2:
        txt = "\n\nThank you for playing !\nPlease, send me your feedback !\n\n-Ptishell (programer)\npierre.surply@gmail.com"
        pos_txt = (80,50)
        bloc_stone = bloc.Stone(1)
        bloc_stone.move_el(0,500)
        app.perso.move_el(-app.perso.x+10, -app.perso.y+400)
        mobs = []
        for i in range(20):
            new_mob = mob.Mob(random.randint(0, 2))
            new_mob.move_el(random.randint(100,700),500)
            new_mob.sens = False
            mobs.append(new_mob)
        fireworks = []
        txt_mobs = []

    coef = 2
    rang_txt = 0
    app.perso.isingrav = False
    app.perso.sens = True
    while 1:
        fps = int(1/(time() - prev))
        while fps > 30: 
            fps = int(1/(time() - prev))
        prev = time()
        # Evenement
        input.update_event(app)
        if input.key[K_RETURN]:
            break
            input.key[K_RETURN] = 0
        
        
        pointeur.move_el(-pointeur.x+input.mouse[0], -pointeur.y+input.mouse[1])


        # White
        sur_txt = char.write(app,txt[:rang_txt],pos_txt[0]+2,pos_txt[1]+2,(255,255,255))
        # Black
        sur_txt_b = char.write(app,txt[:rang_txt],pos_txt[0],pos_txt[1])

        app.blit(fond)

        for i in sur_txt:
            app.blit(i)
        for i in sur_txt_b:
            app.blit(i)
        app.perso.anim(False)
        if rang_txt < len(txt):
            rang_txt += 1
        if id==1:
            if coef > 0.5:
                app.perso.anim(True)
                if app.perso.x > 300:
                    app.perso.move_el(int(2.5*coef),int(-1.4*coef))
                    coef -= 0.012
                else:
                    app.perso.move_el(5,0)

                app.blit(app.perso, coef)

        if id==2:
            app.blit(bloc_stone, 2)
            for i in mobs:
                i.anim()
                app.blit(i,2)
            app.blit(app.perso, 2)
            for i in fireworks:
                i.update()
                app.blit(i)
                if time()-i.time_creat > 3:
                    fireworks.remove(i)
            for i in txt_mobs:
                app.blit(i)
                if time()-i.time > 1:
                    txt_mobs.remove(i)
            if random.randint(1,20) == 1:
                txt_mobs.append(TxtMob(app.perso.nom, app.font_petit))
                rand = random.randint(1,3)
                if rand==1:
                    const.keeper[random.randint(0,2)].play()
                elif rand==2:
                    const.goblin[random.randint(0,1)].play()
                else:
                    const.zombie[0].play()
            if random.randint(1,10) == 1:
                x = random.randint(10,790)
                y = random.randint(10,300)
                for i in range(random.randint(10,50)):
                    new_fire = particule.Particule(1)
                    new_fire.move_el(x,y)
                    fireworks.append(new_fire)
                    const.fireworks[random.randint(0,1)].play()
            
        app.blit(pointeur)
        app.flip()
    if id == 1:
        const.door.play()
    app.perso.move_el(-app.perso.x, -app.perso.y)



class TxtMob(element.Element):
    def __init__(self, name, font):
        element.Element.__init__(self)
        rand = random.randint(1,3)
        if rand == 1:
            txt = "Long life the king "+name+" !"
        elif rand == 2:
            txt = "Glory to "+name+"  !"
        else:
            txt = "Hail "+name+"  !"
        self.changer_text(txt, font)
        self.move_el(random.randint(100, 700), random.randint(430, 480))
        self.time = time()
    
