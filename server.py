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
from time import *

import jeu
import map
import perso
import const
import item
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
        self.load_game("test_srv")

        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        self.tcp.bind((self.host,self.port))
        self.tcp.listen(3)

        self.udp.bind((self.host,self.port))

        self.runned = True
        self.main()

    def main(self):
        while self.runned:
            self.check_connection()
            self.read()

    def check_connection(self):
        asked, wlist, xlist = select.select([self.tcp,self.udp], [], [], 0.05)
        for i in asked:
            if i == self.tcp:
                connection, adresse = self.tcp.accept() 
                client = Client(connection, adresse)
                self.clients.append(client)
                print "L'adresse",client.adr,"vient de se connecter au serveur !", "\a"
            elif i == self.udp:
                self.process_udp(i)

    def process_udp(self, sock):
        buffer,adr = sock.recvfrom(8000)
        buffer = buffer.split(";")

        buffer_ret = ""
        if buffer[0] == "set_adr_udp":
            print buffer
            self.get_client_nom(buffer[1]).adr_udp = adr
        elif buffer[0] == "set_pos":
            self.get_client_adr(adr).x = int(buffer[1])
            self.get_client_adr(adr).y = int(buffer[2])
            self.get_client_adr(adr).v_x = int(buffer[3])
            self.get_client_adr(adr).v_y = int(buffer[4])
            self.get_client_adr(adr).sens = int(buffer[5])
            self.get_client_adr(adr).hitting = int(buffer[6])
        elif buffer[0] == "get_pos":
            for i in self.clients:
                if i != self.get_client_adr(adr):
                    buffer_ret += i.nom+";"+str(i.map)+";"+str(i.x)+";"+str(i.y)+";"+str(i.v_x)+";"+str(i.v_y)+";"+str(int(i.sens))+";"+str(int(i.isingrav))+";"+str(int(i.hitting))+";"+str(int(i.fired))+"\n"
        
        sock.sendto(buffer_ret,adr)        


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

    def get_client_adr(self, adr):
        for i in self.clients:
           if i.adr_udp == adr:
               return i

    def get_client_nom(self, nom):
        for i in self.clients:
           if i.nom == nom:
               return i

    def get_map(self, id):
        for i in self.maps:
           if i.id == id:
               return i

    def read(self):
        clients_to_read = []
        try:
            clients_to_read, wlist, xlist = select.select(self.get_clients(), [], [], 0.05)
        except select.error:
            pass
        else:
            for client in clients_to_read: 
                pbuffer = client.recv(1024)
                buffer_ret = " "
                if pbuffer == "exit":
                    self.runned = False
                buffer = pbuffer.split(";")
                if buffer[0] == "co_perso":
                    self.get_client(client).nom = buffer[1]
                    self.get_client(client).color = []
                    self.get_client(client).color.append(buffer[2])
                    self.get_client(client).color.append(buffer[3])
                    self.get_client(client).color.append(buffer[4])
                    self.get_client(client).color.append(buffer[5])
                    self.get_client(client).color.append(buffer[6])
                elif buffer[0] == "get_perso":
                    for i in self.clients:
                        if i != self.get_client(client):
                            buffer_ret = i.get_char()
                elif buffer[0] == "set_map_perso":
                    self.get_client(client).map = int(buffer[1])
                    self.get_client(client).id_porte = int(buffer[2])
                elif buffer[0] == "get_map":
                    buffer_ret=map.map2char(self.get_map(self.get_client(client).map).map)
                elif buffer[0] == "set_vie":
                    self.get_client(client).vie = int(buffer[1])
                elif buffer[0] == "nbr_player":
                    buffer_ret = str(len(self.clients))
                elif buffer[0] == "get_last_event":
                    buffer_ret=str(len(self.get_map(self.get_client(client).map).event))
                elif buffer[0] == "get_event":
                    #print "----------------"
                    #print self.get_map(self.get_client(client).map).event
                    buffer_ret=self.get_map(self.get_client(client).map).send_event(int(buffer[1]), self.get_client(client).nom)
                    #print "RET > "+buffer_ret
                elif buffer[0] == "jump":
                    self.get_client(client).isingrav = True
                elif buffer[0] == "stop_jump":
                    self.get_client(client).isingrav = False
                elif buffer[0] == "hit_block":
                    print self.get_client(client).nom+";"+pbuffer
                    self.get_map(self.get_client(client).map).event.append(self.get_client(client).nom+";"+pbuffer)
                    x = int(buffer[1])
                    y = int(buffer[2])
                    damage = float(buffer[3])
                    for i in self.get_map(self.get_client(client).map).map:
                        if i.x == x and i.y == y:
                            if i.hit(damage):
                                self.get_map(self.get_client(client).map).map.remove(i)
                            
                try:
                    client.send(buffer_ret)
                except socket.error:
                    self.break_connection(client)
                    

    def close(self):
        for client in self.clients:
            client.connection.close()
        self.sock.close()

    def load_game(self, nom):
        i = 0
        while map.open_map("save_srv/"+nom+"/map"+str(i)) != []:
            self.maps.append(map.Map(map.open_map("save_srv/"+nom+"/map"+str(i)),i))
            i = i+1
        i = -1
        while map.open_map("save_srv/"+nom+"/map"+str(i)) != []:
            self.maps.append(map.Map(map.open_map("save_srv/"+nom+"/map"+str(i)),i))
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
        self.adr_udp = None
        
        self.nom = "Unknown"
        self.x = 0
        self.y = 0
        self.map = 0
        self.id_porte = 0
        self.vie = 6
        self.inv = item.Inventaire()
        self.inv.add(item.Item(1,1))
        self.color = []
        self.color.append("0,128,0")
        self.color.append("0,93,0")
        self.color.append("0,0,0")
        self.color.append("255,221,212")
        self.color.append("145,72,0")
        self.sens = True
        self.fired = False
        self.hitting = False

        # Gravité
        self.v_y = 0
        self.v_x = 0
        self.isingrav = True

    def get_char(self):
        buffer = self.nom+";"+str(self.map)+";"+str(self.id_porte)+";"+str(self.vie)+";"+str(int(self.fired))+";"+self.inv.save()+";"+str(self.inv.item_sel)
        for i in self.color:
            buffer += ";"+i
        return buffer
        


server = Server()
server.start()
server.close()      
        
