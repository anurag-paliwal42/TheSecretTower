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
import threading

import jeu
import map
import perso
import const
import item
from bloc import *

class Server:
    def __init__(self):

        # Proprietes
        self.host = '0.0.0.0'
        self.port = 2346
        self.msg_welcome = "*************************\n"+\
            "Welcome to this Server !\n"+\
            "Version "+const.version+"\n"+\
            "www.secrettower.net\n"+\
            "*************************\n"+\
            "Type \"/help\" for help\n"
        self.world = "phil"
        self.mobs = True
        
        
        const.display = False
        self.runned = False
        self.clients = []
        self.clients_saved = []
        self.maps = []
        self.event = []

        self.out("***Server TheSecretTower***"+\
                     "\n\tVersion: "+const.version+\
                     "\n\tWorld: "+self.world+\
                     "\n\tWelcome msg:\n"+self.msg_welcome)

        while not self.load_game(self.world):
            self.new_game(self.world)            

        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        self.tcp.bind((self.host,self.port))
        self.tcp.listen(3)

        self.udp.bind((self.host,self.port))

        self.runned = True
        thread_input=threading.Thread(target=self.input)
        thread_udp=threading.Thread(target=self.check_connection)
        thread_udp.start()
        self.out("Ready !\a")
        thread_input.start()
        self.main()
        thread_udp.join()

    def input(self):
        while self.runned:
            cmd = raw_input("> ").lower().strip()
            if len(cmd) > 0:
                cmd = cmd.split()
                if cmd[0] == "help" or cmd[0] == "?":
                    self.out("Commands help :"\
                                 "\nhelp or ?: Shows a list of server commands"\
                                 "\nkick player: Disconnects player from the server"\
                                 #"\nban player:  Bans player from the server"\
                                 #"\npardon player:  Pardons a banned player"\
                                 #"\nban-ip ip:  Bans IP address from the server"\
                                 #"\npardon-ip ip:  Pardons a banned IP address"\
                                 "\nlist or ls: list all connected players"\
                                 "\nsave: Save map and players"\
                                 "\nsay message: Broadcasts message"+\
                                 "\nstop: Save and stop the server")
                elif cmd[0] == "kick":
                    del cmd[0]
                    cmd = " ".join(cmd)
                    if self.get_client_nom(cmd) != None:
                        self.break_connection(self.get_client_nom(cmd).connection, "kick")
                    else:
                        self.out(cmd + " isn't connected")
                elif cmd[0] == "list" or cmd[0] == "ls":
                    if len(self.clients) > 0:
                        for i in self.clients:
                            self.out("-"+str(i.adr)+i.nom)
                    else:
                        self.out("The server is empty :'-(")
                elif cmd[0] == "say":
                    del cmd[0]
                    cmd = " ".join(cmd).capitalize()
                    self.event.append("say;[Server] "+cmd)
                elif cmd[0] == "save":
                    self.save_game(self.world)
                elif cmd[0] == "stop":
                    self.shutdown()

                else:
                    cmd = " ".join(cmd)
                    self.out("Unknown command \""+cmd+"\". Type \"help\" for help")

    def out(self, buffer):
        buffer = buffer.split("\n")
        t = localtime()
        for i in buffer:
            print "["+str(t.tm_hour)+":"+str(t.tm_min)+":"+str(t.tm_sec)+"] "+ i

    def main(self):
        while self.runned:
            self.read()

    def check_connection(self):
        while self.runned:
            asked, wlist, xlist = select.select([self.tcp,self.udp], [], [], 0.05)
            for i in asked:
                if i == self.tcp:
                    connection, adresse = self.tcp.accept() 
                    client = Client(connection, adresse)
                    self.clients.append(client)
                    self.out(str(client.adr)+" is asking a connection...")
                elif i == self.udp:
                    self.process_udp(i)

    def process_udp(self, sock):
        buffer,adr = sock.recvfrom(8000)
        buffer = buffer.split(";")
        
        buffer_ret = ""
        if buffer[0] == "set_adr_udp" and self.get_client_nom(buffer[1]) != None:
            self.get_client_nom(buffer[1]).adr_udp = adr
        elif buffer[0] == "set_pos":
            if self.get_client_adr(adr) != None:
                self.get_client_adr(adr).x = int(buffer[1])
                self.get_client_adr(adr).y = int(buffer[2])
                self.get_client_adr(adr).v_x = int(buffer[3])
                self.get_client_adr(adr).v_y = int(buffer[4])
                self.get_client_adr(adr).sens = int(buffer[5])
                self.get_client_adr(adr).hitting = int(buffer[6])
                self.get_client_adr(adr).fired = int(buffer[7])
                self.get_client_adr(adr).issprinting = int(buffer[8])
                self.get_client_adr(adr).bras[0] = int(buffer[9])
                self.get_client_adr(adr).bras[1] = int(buffer[10])
        elif buffer[0] == "get_pos":
            for i in self.clients:
                if i != self.get_client_adr(adr):
                    buffer_ret += i.nom+";"+str(i.map)+";"+str(i.x)+";"+str(i.y)+";"+str(i.v_x)+";"+str(i.v_y)+";"+str(int(i.sens))+";"+str(int(i.isingrav))+";"+str(int(i.hitting))+";"+str(int(i.fired))+";"+str(int(i.issprinting))+";"+str(i.bras[0])+";"+str(i.bras[1])+"\n"
        
        sock.sendto(buffer_ret,adr)        


    def break_connection(self, client, tag = ""):
        self.event.append("disconnect;"+self.get_client(client).nom)
        if tag == "kick":
            self.event.append("say;"+self.get_client(client).nom+" has been kicked")
            self.out(str(self.get_client(client).adr)+self.get_client(client).nom+" has been kicked")
        else:
            self.event.append("say;"+self.get_client(client).nom+" disconnected")
            self.out(str(self.get_client(client).adr)+self.get_client(client).nom+" disconnected")
        self.clients_saved.append(self.get_client(client))
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
        return Client()

    def get_client_adr(self, adr):
        for i in self.clients:
           if i.adr_udp == adr:
               return i
        return Client()

    def get_client_nom(self, nom):
        for i in self.clients:
           if i.nom == nom:
               return i
        return Client()

    def get_map(self, id):
        for i in self.maps:
           if i.id == id:
               return i
        return map.Map()

    def read(self):
        clients_to_read = []
        try:
            clients_to_read, wlist, xlist = select.select(self.get_clients(), [], [], 0.05)
        except select.error:
            pass
        else:
            for client in clients_to_read:
                try:
                    pbuffer = client.recv(1024)
                    
                    buffer_ret = " "
                    if pbuffer == "exit":
                        self.runned = False
                    buffer = pbuffer.split(";")
                    if buffer[0] == "co_perso":
                        founded = False
                        for i in self.clients:
                            if i.nom == buffer[1]:
                                founded = True
                                break
                        if not founded:
                            founded = False
                            for i in self.clients_saved:
                                if i.nom == buffer[1]:
                                    self.get_client(client).inv.empty()
                                    self.get_client(client).inv.load(i.inv.save())
                                    self.clients_saved.remove(i)
                                    break
                            self.get_client(client).nom = buffer[1]
                            self.get_client(client).color = []
                            self.get_client(client).color.append(buffer[2])
                            self.get_client(client).color.append(buffer[3])
                            self.get_client(client).color.append(buffer[4])
                            self.get_client(client).color.append(buffer[5])
                            self.get_client(client).color.append(buffer[6])
                            self.event.append("connect;"+self.get_client(client).nom)
                            self.event.append("say;"+self.get_client(client).nom+" connected")
                            buffer_ret = "Connected"
                            self.out(str(self.get_client(client).adr)+self.get_client(client).nom+" connected !\a")
                        else:
                            buffer_ret = "Pseudo already used"
                    elif buffer[0] == "get_welcome":
                        buffer_ret="say;"+self.msg_welcome
                    elif buffer[0] == "get_persos":
                        buffer_ret = ""
                        for i in self.clients:
                            if i != self.get_client(client):
                                buffer_ret += i.get_char()+"\n"
                        buffer_ret+= " "
                    elif buffer[0] == "get_perso":
                        if buffer[1] != self.get_client(client).nom and self.get_client_nom(buffer[1]) != None:
                            buffer_ret = self.get_client_nom(buffer[1]).get_char()
                    elif buffer[0] == "get_mobs":
                        buffer_ret=str(int(self.mobs))


                    # Inventory
                    elif buffer[0] == "set_inv":
                        self.get_client(client).inv.empty()
                        self.get_client(client).inv.load(buffer[1])
                    elif buffer[0] == "get_inv":
                        buffer_ret=self.get_client(client).inv.save()

                    # Map
                    elif buffer[0] == "get_map":
                        buffer_ret=map.map2char(self.get_map(int(buffer[1])).map)
                    elif buffer[0] == "set_map":
                        id_map = int(buffer[1])
                        self.get_client(client).map = id_map
                        found = False
                        for i in self.maps:
                            if i.id == id_map:
                                found = True
                        if not found:
                            map.save_map("save_srv/"+self.world+"/map"+str(id_map), self.gen_map(id_map))
                            self.maps.append(map.Map(map.open_map("save_srv/"+self.world+"/map"+str(id_map)),id_map))
                            
                    elif buffer[0] == "set_map_perso":
                        self.get_client(client).map = int(buffer[1])
                        self.get_client(client).id_porte = int(buffer[2])


                    elif buffer[0] == "set_vie":
                        self.get_client(client).vie = int(buffer[1])
                    elif buffer[0] == "nbr_player":
                        buffer_ret = str(len(self.clients))
                    elif buffer[0] == "get_last_event":
                        buffer_ret=str(len(self.event))
                    elif buffer[0] == "get_last_event_map":
                        buffer_ret=str(len(self.get_map(int(buffer[1])).event))
                    elif buffer[0] == "get_event_map":
                        buffer_ret=self.get_map(self.get_client(client).map).send_event(int(buffer[1]), self.get_client(client).nom)
                    elif buffer[0] == "get_event":
                        buffer_ret=self.send_event(int(buffer[1]))
                    elif buffer[0] == "jump":
                        self.get_client(client).isingrav = True
                    elif buffer[0] == "stop_jump":
                        self.get_client(client).isingrav = False
                    elif buffer[0] == "destroy_block":
                        self.get_map(self.get_client(client).map).event.append(self.get_client(client).nom+";"+pbuffer)
                        x = int(buffer[1])
                        y = int(buffer[2])
                        for i in self.get_map(self.get_client(client).map).map:
                            if i.x == x and i.y == y:
                                if isinstance(i, Coal):
                                    self.get_client(client).inv.add(item.Item(34, 4))
                                else:
                                    self.get_client(client).inv.add(i)
                                self.get_map(self.get_client(client).map).map.remove(i)
                                
                    # hit block
                    elif buffer[0] == "hit_block":
                        self.get_map(self.get_client(client).map).event.append(self.get_client(client).nom+";"+pbuffer)
                        x = int(buffer[1])
                        y = int(buffer[2])
                        damage = float(buffer[3])
                        for i in self.get_map(self.get_client(client).map).map:
                            if i.x == x and i.y == y:
                                if i.hit(damage):
                                    if isinstance(i, Coal):
                                        self.get_client(client).inv.add(item.Item(34, 4))
                                    else:
                                        self.get_client(client).inv.add(i)
                                    self.get_map(self.get_client(client).map).map.remove(i)

                    # Set Block
                    elif buffer[0] == "set_block":
                        self.get_map(self.get_client(client).map).event.append(self.get_client(client).nom+";"+pbuffer)
                        x = int(buffer[1])
                        y = int(buffer[2])
                        for i in self.get_map(self.get_client(client).map).map:
                            if i.x == x and i.y == y:
                                self.get_map(self.get_client(client).map).map.remove(i)
                        self.get_map(self.get_client(client).map).map.append(map.char2bloc(buffer[3]))

                    # Add block
                    elif buffer[0] == "add_block":
                        self.get_map(self.get_client(client).map).event.append(self.get_client(client).nom+";"+pbuffer)
                        bloc = map.char2bloc(buffer[1])
                        self.get_client(client).inv.changer_select(self.get_client(client).inv.search(item.Item_Bloc(bloc)))
                        self.get_client(client).inv.delete()
                        self.get_map(self.get_client(client).map).map.append(bloc)
                    elif buffer[0] == "lock_chest":
                        self.get_map(self.get_client(client).map).event.append(self.get_client(client).nom+";"+pbuffer)
                    elif buffer[0] == "say":
                        self.out(self.get_client(client).nom+"> "+buffer[1])
                        buffer_unspaced = buffer[1].split()
                        if buffer_unspaced[0] == "/me" and len(buffer_unspaced)>1:
                            del buffer_unspaced[0]
                            buffer[1] = " ".join(buffer_unspaced)
                            self.event.append("say;"+self.get_client(client).nom+" "+buffer[1])
                        elif buffer_unspaced[0] == "/help":
                            buffer_ret = "say;"+\
                                "Commands help : "+\
                                "\n/help : Shows a list of server commands"+\
                                "\n/welcome :  Shows welcome message"+\
                                "\n/list or /ls : list all connected players"+\
                                "\n/me action : Sends a message as an action"
                        elif buffer_unspaced[0] == "/list" or buffer_unspaced[0] == "/ls":
                            buffer_ret = "say;"+str(len(self.clients))+" player(s) connected :"
                            for i in self.clients:
                                buffer_ret += "\n-"+i.nom
                        elif buffer_unspaced[0] == "/welcome":
                            buffer_ret="say;"+self.msg_welcome
                        elif buffer_unspaced[0] == "/sign":
                            map_temp = self.get_map(self.get_client(client).map).map[:]
                            map_temp.reverse()
                            for i in map_temp:
                                if isinstance(i, Sign):
                                    del buffer_unspaced[0]
                                    buffer[1] = " ".join(buffer_unspaced)
                                    i.txt = buffer[1]
                                    self.get_map(self.get_client(client).map).event.append("server;set_block;"+str(i.x)+";"+str(i.y)+";"+map.bloc2char(i))
                                    break
                            map_temp = None
                        else:
                            self.event.append("say;"+self.get_client(client).nom+"> "+buffer[1])
                     
                    client.send(buffer_ret)
                except socket.error:
                    self.break_connection(client)

                    
    def shutdown(self):
        self.out("Stopping server...")
        self.save_game(self.world)
        self.runned = False 

    def close(self):
        for client in self.clients:
            client.connection.close()
        self.tcp.close()
        self.udp.close()

    def load_game(self, nom):
        if os.path.isdir("data/save_srv/"+nom):
            self.out("Loading characters...")
            file = open("data/save_srv/"+nom+"/char" , 'r')
            buffer = file.read().split("\n")
            for i in buffer:
                i=i.split(";")
                if len(i)>1:
                    new_client = Client()
                    new_client.nom = i[0]
                    new_client.inv.empty()
                    new_client.inv.load(i[1])
                    self.clients_saved.append(new_client)
                    self.out(new_client.nom+" loaded ")

            self.out("Loading "+nom+"...")
            i = 0
            while map.open_map("save_srv/"+nom+"/map"+str(i)) != []:
                self.maps.append(map.Map(map.open_map("save_srv/"+nom+"/map"+str(i)),i))
                i = i+1
            i = -1
            while map.open_map("save_srv/"+nom+"/map"+str(i)) != []:
                self.maps.append(map.Map(map.open_map("save_srv/"+nom+"/map"+str(i)),i))
                i = i-1
            return True
        else:
            return False



    def save_game(self, nom):
        # Map
        self.out("Saving "+nom+"...")
        for i in self.maps:
           map.save_map("save_srv/"+nom+"/map"+str(i.id), i.map) 
        # Perso
        for i in self.clients:
            self.clients_saved.append(i)
            
        file = open("data/save_srv/"+nom+"/char", "w")
        buffer  = ""
        for i in self.clients_saved:
            buffer += i.nom+";"+i.inv.save()+"\n"
        file.write(buffer)
        file.close()

    def new_game(self, nom):
        self.out("Generating "+nom+"...")
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
        file = open("data/save_srv/"+nom+"/char", "w")
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
                        elif rand < 40:
                            bloc =Tin(20)
                        elif rand < 60:
                            bloc = Copper(15)
                        elif rand < 70 and level < -5:
                            bloc = Iron(16)
                        elif rand < 75 and level < -10:
                            bloc = Gold(18)
                        elif rand < 80 and level < -20:
                            bloc = Diamond(19)
                        elif rand < 90 and level < -10:
                            bloc = Titanium(17)
                        elif rand < 95 and level < -20:
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

    def send_event(self, id):
        buffer = str(len(self.event))+"\n"
        for i in range(id, len(self.event)):
            buffer += self.event[i]+"\n"
        return buffer
        

        

class Client():
    def __init__(self, connection = None, adr = None):
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
        self.issprinting = False
        self.bras = [0,0]

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
        
