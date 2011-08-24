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


import os
import random
import math
import copy
import threading

# Pygame
import pygame
from pygame.locals import *

import element
import menu
import char
from jeu import *
from map import *
from editeur import *
import client

# Constante
import const
class App:
    """ Classe définissant l'application The Secret Tower"""

    def __init__(self):
        """Initialisation de l'application"""

        # Initialisation de pygame
        pygame.init()
        
        # création de la fenetre
        self.size = (800, 600)
        self.fenetre = pygame.display.set_mode(self.size, pygame.DOUBLEBUF)
        pygame.display.set_icon(pygame.image.load("img/perso_small.png").convert_alpha())
        pygame.display.set_caption(const.fenetre_titre)
        
        pygame.mouse.set_visible(False)

        # font
        self.font = pygame.font.Font("img/font.ttf", 20)
        self.font_petit = pygame.font.Font("img/font.ttf", 15)

        const.sprite_bloc = pygame.image.load("img/bloc.png").convert_alpha()
        const.sprite_lave = pygame.image.load("img/lave.png").convert_alpha()
        const.sprite_torch = pygame.image.load("img/torch.png").convert_alpha()
        const.sprite_perso = pygame.image.load("img/perso.png").convert_alpha()
        const.sprite_arm = pygame.image.load("img/arm_perso.png").convert_alpha()
        const.sprite_item = pygame.image.load("img/item.png").convert_alpha()
        const.sprite_mobs = pygame.image.load("img/mobs.png").convert_alpha()
        const.sprite_degats = pygame.image.load("img/degats.png").convert_alpha()
        const.sprite_fire = pygame.image.load("img/fire.png").convert_alpha()
        const.vide = pygame.image.load("img/vide.png").convert_alpha()

        self.perso = Perso()
        self.partie = []
        self.coef = 2

        self.pos_screen = (0,0)

        const.chatbox = char.Chatbox()
        
        
    def main(self):
        cmd = 1
        while cmd:
            cmd =  menu(self, "Main Menu", ["Play", "Edit Level", "Quit"])
            if cmd == 2:
                self.perso.reset()
                self.perso.set_org_color()
                self.partie = ["Gen", 0]
                self.perso.map = 0
                cmd = menu(self, "Edit Level", ["New level", "Load level"])
                if cmd == 1:
                    cmd = editeur(self, [], "Unnamed")
                elif cmd == 2:
                    nom = ask(self, "Edit Level] Level's name :")
                    cmd = editeur(self, open_map("map/custom/"+nom), nom)
            elif cmd == 1:
                if not os.path.isdir("data/perso/"):
                    os.mkdir("data/perso/")
                characters = os.listdir("data/perso")[:5]
                while len(characters) < 5:
                    characters.append("Empty")
                characters.append("Cancel")
                cmd = menu(self, "Choose a Character", characters)
                
                if cmd > len(os.listdir("data/perso/")) and cmd != 6:
                    self.perso.set_org_color()
                    self.perso.nom = ask(self, "Enter a name for the Character")
                    while cmd != 6:
                        cmd = menu(self, "Choose "+self.perso.nom+"'s colors", ["Shirt", "Pants", "Hair", "Skin", "Other", "Done"], self.perso)
                        if cmd != 6:
                            menu_color(self, cmd-1, self.perso)
                    self.perso.save()
                elif cmd < 6:
                    self.perso.load(os.listdir("data/perso")[cmd-1])
                    cmd =  menu(self, "Play", ["Single Player", "Multi Player", "Delete Character", "Edit Character", "Cancel"], self.perso)
                    if cmd == 1:
                        cmd =  menu(self, "Single Player", ["Entering the Tower !", "Play Custom Level", "Cancel"], self.perso)
            
                        if cmd == 1:
                            if not os.path.isdir("data/save"):
                                os.mkdir("data/save/")
                            saves = os.listdir("data/save")[:5]
                            while len(saves) < 5:
                                saves.append("Empty")
                            saves.append("Cancel")
                            cmd = menu(self, "Choose a Game", saves)
                            if cmd < 6:
                                self.perso.reset()
                                if cmd > len(os.listdir("data/save/")) and cmd != 6:
                                    self.partie = []
                                    self.partie = self.nouvelle_partie(ask(self, "New Game] Game's name : "))
                                else:
                                    self.partie = self.charger_partie(os.listdir("data/save")[cmd-1])
                                self.perso.map = self.partie[1]
                                self.perso.id_porte = self.partie[2]
                                cmd = 1
                                while open_map("save/"+self.partie[0]+"/map"+str(self.partie[1])) != [] and cmd == 1:
                                    cmd = jeu(self, open_map("save/"+self.partie[0]+"/map"+str(self.partie[1])), self.perso)
                                    self.partie[1] = self.perso.map
                                    if self.partie[1] < 0:
                                        if open_map("save/"+self.partie[0]+"/map"+str(self.partie[1])) == []:
                                            save_map("save/"+self.partie[0]+"/map"+str(self.partie[1]), self.gen_map(self.partie[1]))
                            

                        elif cmd == 2:
                            self.perso.reset()
                            self.partie = ["Gen", 0]
                            self.perso.map = 0
                            cmd = jeu(self, open_map("map/custom/" + ask(self, "Load Level] Level's name :")), self.perso)
                    elif cmd == 2:
                        cmd = self.multiplayer()
                    elif cmd == 3:
                        cmd =  menu(self, "Are you sure ?", ["Yes, delete "+self.perso.nom+" definitely !", "No, I want to keep "+self.perso.nom], self.perso)
                        if cmd == 1:
                            os.remove("data/perso/"+self.perso.nom)
                    elif cmd == 4:
                        old_name = self.perso.nom
                        while cmd != 3:
                            cmd =  menu(self, "Edit Character", ["Rename", "Change colors", "Done"], self.perso)
                            if cmd == 1:
                                self.perso.nom = ask(self, "Enter a name")
                            elif cmd == 2:
                                while cmd != 6:
                                    cmd = menu(self, "Choose "+self.perso.nom+"'s colors", ["Shirt", "Pants", "Hair", "Skin", "Other", "Done"], self.perso)
                                    if cmd != 6:
                                        menu_color(self, cmd-1, self.perso)
                        os.remove("data/perso/"+old_name)
                        self.perso.save()
        const.runned = False
        pygame.quit()

    def multiplayer(self):
        self.perso.reset()
        self.partie = ["Multi", 0]
        self.perso.map = 0
        const.runned = True
        const.input = []
        const.output == ""
        const.host = ask(self, "Enter the IP of the server :")
        thread=threading.Thread(target=client.connect)
        const.input.append("co_perso;"+self.perso.get_char(";"))
        const.input_udp = "set_adr_udp;"+self.perso.nom
        thread.start()
        tps_connect = 0
        cmd = 1
        while const.output == "":
            tps_connect +=1
        if const.output != "Connected":
            cmd = menu(self, const.output, ["Ok"])
            const.output = ""
        else:
            const.output = ""
            const.input.append("get_inv")
            while const.output == "":
                tps_connect +=1
            self.perso.inv.empty()
            self.perso.inv.load(const.output)
            const.output = ""
            const.input.append("get_welcome")
            while not cmd in [5,0]:
                const.input.append("set_map;"+str(self.partie[1]))
                const.input.append("get_map;"+str(self.partie[1]))
                const.input.append("get_last_event_map;"+str(self.partie[1]))
                const.input.append("get_last_event")
                while const.map == []:
                    tps_connect +=1
            
                cmd = jeu(self, const.map, self.perso)
                const.map = []
                self.partie[1] = self.perso.map

        const.runned = False
        return cmd

    def blit(self, element, coef=1):
        """Ajoute Element à l'écran"""
        if isinstance(element, Perso):
            if not element.sens:
                self.fenetre.blit(pygame.transform.scale(element.image, (element.image.get_width()*coef,element.image.get_height()*coef)), (element.x-(element.image.get_width()-50), element.y))
            else:
                self.fenetre.blit(pygame.transform.scale(element.image, (element.image.get_width()*coef,element.image.get_height()*coef)), (element.x,element.y))
        elif isinstance(element, Element):
            self.fenetre.blit(element.image, (element.x,element.y))
    
    def scale(self, coef):
        x = self.perso.x*coef-((800-50*coef)/2)
        y = self.perso.y*coef-((600-50*coef)/2)
        if x < 0:
            x=0
        if x+800 >800*coef:
            x = 800*coef-800
        if y < 0:
            y = 0
        if y+600 >600*coef:
            y = 600*coef-600

        self.pos_screen = (x,y)
        self.fenetre.blit(pygame.transform.scale(self.fenetre, (800*coef, 600*coef)), (0,0), (x,y, self.size[0],self.size[1]))
            

    def flip(self):
        """Rafraichissement"""
        if self.size[0] != 800 or self.size[1] != 600:
            new_size = (self.size[0]*(float(self.size[0])/800.0),self.size[1]*(float(self.size[1])/600.0))
            print new_size, self.size
            self.fenetre.blit(pygame.transform.scale(self.fenetre, new_size), (0,0))
        pygame.display.flip()

    def save_screen(self):
        return copy.copy(self.fenetre)

    def nouvelle_partie(self, nom):
        partie = [nom, 0, 0]
        self.perso.inv.empty()
        self.perso.inv.add(Item(1,1))
        # Copie map std
        i = 0

        while True:
            if not os.path.isdir("data/save/"):
                os.mkdir("data/save/")
            if not os.path.isdir("data/save/"+nom+"/"):
                os.mkdir("data/save/"+nom+"/")
                break
            elif menu(self, "Warning : Erase existing game ?", ["Yes", "No"]) == 1:
                for entry in os.listdir("data/save/"+nom+"/"):
                    os.remove("data/save/"+nom+"/"+entry)
                os.rmdir("data/save/"+nom+"/")
                os.mkdir("data/save/"+nom+"/")
                break
            else:
                nom = ask(self, "New Game] Game's name : ")
                
       
        while open_map("map/std/map"+str(i)) != []:
            save_map("save/"+nom+"/map"+str(i),open_map("map/std/map"+str(i)))
            i = i+1

        # Génération sous-sol
        save_map("save/"+nom+"/map-1", self.gen_map(-1))
       
        # Fichier global
        file = open("data/save/"+nom+"/"+nom, "w")
        file.write("map=0\nid=0\n")
        file.close()
        return partie

    def charger_partie(self, nom):
        partie = []
        partie.append(nom)
        try:
            file = open("data/save/"+nom+"/"+nom)
            tampon = file.read()
            elements = tampon.split("\n")
            i = 1
            for element in elements:
                if element != "":
                    prop = element.split("=")
                    if prop[0] == "map" and i == 1:
                        partie.append(int(prop[1]))
                        i = i+1
                    elif prop[0] == "id" and i == 2:
                        partie.append(int(prop[1]))
                        self.perso.id_porte = int(prop[1])
                        i = i +1
                    elif prop[0] == "inv":
                        self.perso.inv.empty()
                        self.perso.inv.load(prop[1])
            file.close()
                    
        except IOError:
            print (path + " : Partie introuvable !")

        return partie


    def save_partie(self):
        file = open("data/save/"+self.partie[0]+"/"+self.partie[0], "w")
        
        tampon = "map="+str(self.partie[1])+"\n"
        tampon = tampon +"id="+str(self.perso.id_porte)+"\n"
        tampon +=  "inv="+self.perso.inv.save()+"\n"
        
        file.write(tampon)
        file.close()

    def set_size(self,new_size):
        self.size = new_size
        self.fenetre = pygame.display.set_mode(self.size, pygame.DOUBLEBUF | pygame.RESIZABLE)


    def gen_map(self, level):
        map = []
        bloc = Porte(0, 1, int(math.fabs(level-1)), 0)
        xent= random.randint(0, 15)
        yent=1
        bloc.move_el(xent*50,yent*50)
        map.append(bloc)
        bloc = Porte(0, 0,int(math.fabs(level-2)), 0)
        xsor= random.randint(0, 15)
        ysor=10
        bloc.move_el(xsor*50,ysor*50)
        map.append(bloc)
        xd = random.randint(0, 16)
        yd = random.randint(0, 12)
        size = random.randint(2,5)

        for x in range(16):
            bloc = Bloc(5)
            bloc.move_el(x*50, 0)
            map.append(bloc)
            bloc = Bloc(5)
            bloc.move_el(x*50, 550)
            map.append(bloc)

        for x in range(16):
            for y in range(10):
                if (math.fabs(xent-x) > 2 or math.fabs(y+2-yent) > 1) and (math.fabs(xsor-x) > 2 or math.fabs(y-ysor) > 1):
                    
                    if int(10+(level/10)) < 4:
                        rand_max = 4
                    else:
                        rand_max = int(10+(level/10))
                    if (random.randint(0, rand_max)) < 2:
                        rand = random.randint(0,200)
                        if rand < 20:
                            bloc = Coal(14)
                        elif rand < 40 and level >= -10:
                            bloc =Tin(20)
                        elif rand < 60 and level >= -10:
                            bloc = Copper(15)
                        elif rand < 70 and level < -10:
                            bloc = Iron(16)
                        elif rand < 75 and level < -20:
                            bloc = Gold(18)
                        elif rand < 80 and level < -30:
                            bloc = Diamond(19)
                        elif rand < 90 and level < -20:
                            bloc = Titanium(17)
                        elif rand < 95 and level < -30:
                            bloc = Uranium(21)
                        else:
                            bloc = Stone(1)
                        bloc.move_el(x*50, y*50+50)
                        map.append(bloc)
                    elif math.fabs(xd-x)+math.fabs(yd-y) > size:
                        bloc = Terre(7)
                        bloc.move_el(x*50, y*50+50)
                        map.append(bloc)


        return map
        

