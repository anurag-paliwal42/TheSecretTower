#!/usr/bin/python
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

################################################
#                                              #
#      The Secret of Tower                     #
#                                              #
#          Auteur : Pierre Surply              #
#     2011                                     #
#                                              # 
################################################

# www.secrettower.net

import socket
import select
import os
import math

import jeu
import map
import perso
import const
from bloc import *

class Server:
    def __init__(self):
        const.display = False
        self.runned = False
        self.clients = []
        self.maps = []

        # Network
        self.host = '127.0.0.1'
        self.port = 234
        
        self.new_game("test_srv")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.sock.bind((self.host,self.port))
        self.sock.listen(3)
        self.runned = True
        self.main()

    def main(self):
        while self.runned:
            self.check_connection()
            self.read()

    def check_connection(self):
        asked, wlist, xlist = select.select([self.sock], [], [], 0.05)
        for i in asked:
            connection, adresse = self.sock.accept() 
            client = Client(connection, adresse)
            self.clients.append(client)
            print "L'adresse",client.adr,"vient de se connecter au serveur !", "\a"

    def break_connection(self, client):
               print self.get_client(client).adr," disconnected"
               self.clients.remove(self.get_client(client))

    def get_clients(self):
        clients = []
        for i in self.clients:
            clients.append(i.connection)
        return clients

    def get_client(self, client):
        for i in self.clients:
           if i.connection == client:
               return i

    def get_map(self, id):
        for i in self.maps:
           if i.id == id:
               return i.map

    def read(self):
        clients_to_read = []
        try:
            clients_to_read, wlist, xlist = select.select(self.get_clients(), [], [], 0.05)
        except select.error:
            pass
        else:
            for client in clients_to_read: 
                buffer = client.recv(1024)
                buffer_ret = " "
                print self.get_client(client).adr, buffer
                if buffer == "exit":
                    self.runned = False
                buffer = buffer.split("/s")
                if buffer[0] == "get_map":
                    nbr_map=int(buffer[1])
                    buffer_ret(map.map2char(self.get_map(nbr_map)))
                try:
                    client.send(buffer_ret)
                except socket.error:
                    self.break_connection(client)
                    

    def close(self):
        for client in clients:
            client.close()
        sock.close()

    def load_game(self, nom):
        i = 0
        while map.open_map("save_srv/"+nom+"/map"+str(i)) != []:
            self.maps.append(map.Map(map.open_map("map/std/map"+str(i)),i))
            i = i+1
        i = -1
        while map.open_map("save_srv/"+nom+"/map"+str(i)) != []:
            self.maps.append(map.Map(map.open_map("map/std/map"+str(i)),i))
            i = i-1

    def new_game(self, nom):
        # Copie map std
        i = 0

        if not os.path.isdir("data/save_srv/"):
            os.mkdir("data/save_srv/")
        if not os.path.isdir("data/save_srv/"+nom+"/"):
            os.mkdir("data/save_srv/"+nom+"/")

        while map.open_map("map/std/map"+str(i)) != []:
            map.save_map("save_srv/"+nom+"/map"+str(i),map.open_map("map/std/map"+str(i)))
            i = i+1

        # Génération sous-sol
        map.save_map("save_srv/"+nom+"/map-1", self.gen_map(-1))
       
        # Fichier global
        file = open("data/save_srv/"+nom+"/perso", "w")
        file.write("")
        file.close()

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
        

        

class Client():
    def __init__(self, connection, adr):
        self.connection = connection
        self.adr = adr
        
        """self.map = 0
        self.id_porte = 0
        self.vie = 6
        #self.last_dommage = time()
        #self.last_dommage_ur = time()
        self.last_hit = 0
        self.inv = Inventaire()
        item = Item(1, 1)
        self.inv.add(item)"""
        


server = Server()
#server.start()        
        
