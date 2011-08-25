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

import socket

import const
import map
from perso import *

def connect():
    stop = False
    tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
 
    try:
        tcp.connect((const.host,const.port))
        for i in const.input:
            send(tcp,i);
            const.input = []
        const.input = []
    except socket.error:
        const.output = const.host+":"+str(const.port)+" : Connection Refused"
    else:
        if const.input_udp != "":
            send_udp(udp,const.input_udp)
            const.input_udp = ""
        send(tcp, "get_persos")
        send(tcp,"get_last_event_map;0")
        send(tcp,"get_last_event")
        while const.runned:
            for i in const.input:
                send(tcp,i);
                const.input.remove(i)
            if const.input_udp != "":
                send_udp(udp,const.input_udp)
                const.input_udp = ""

            send_udp(udp, "get_pos", tcp)
            const.id_last_event = send(tcp,"get_event;"+str(const.id_last_event));
            const.id_last_event_map = send(tcp,"get_event_map;"+str(const.id_last_event_map));
            for event in const.events:
                buffer = event.split(";")
                const.events.remove(event)
                if len(buffer) > 1:
                    print buffer
                    if buffer[0] == "connect":
                        send(tcp, "get_perso;"+buffer[1])
                    if buffer[0] == "disconnect":
                        for i in const.persos:
                            if i.nom == buffer[1]:
                                const.persos.remove(i)
                    if buffer[0] == "say":
                        const.msg.append(buffer[1])


def send_udp(sock, cmd, tcp=None):
    sock.sendto(cmd, (const.host, const.port))
    buffer = sock.recv(2048)

    if cmd == "get_pos":
        for i in buffer.split("\n"):
            if i != " " and i != "":
                found = False
                nom = i.split(";")[0]
                for perso in const.persos:
                    if perso.nom == nom: 
                        char_perso = i.split(";")
                        perso.map = int(char_perso[1])
                        perso.x = int(char_perso[2])
                        perso.y = int(char_perso[3])
                        perso.v_x = int(char_perso[4])
                        perso.v_y = int(char_perso[5])
                        perso.sens = bool(int(char_perso[6]))
                        perso.isingrav = bool(int(char_perso[7]))
                        perso.hitting = bool(int(char_perso[8]))
                        perso.fired = bool(int(char_perso[9]))
                        perso.issprinting = bool(int(char_perso[10]))
                        perso.bras[0] = int(char_perso[11])
                        perso.bras[1] = int(char_perso[12])

            
def send(sock, cmd):
    sock.send(cmd)
    buffer = sock.recv(4096)

    if cmd == "get_persos" or cmd.split(";")[0]== "get_perso":
        for i in buffer.split("\n"):
            if i != " " and i != "":
                found = False
                nom = i.split(";")[0]
                for perso in const.persos:
                    if perso.nom == nom:
                        found = True
                if not found:
                    new_perso = Perso()
                    new_perso.ctrl = False
                    new_perso.inv.ctrl = False
                    char_perso = i.split(";")
                    new_perso.nom = char_perso[0]
                    new_perso.map = int(char_perso[1])
                    new_perso.id_porte = int(char_perso[2])
                    new_perso.vie = int(char_perso[3])
                    new_perso.fired = bool(int(char_perso[4]))
                    new_perso.inv.load(char_perso[5])
                    new_perso.inv.item_sel = int(char_perso[6])
                    for nbr in range(5):
                        new_perso.char2color(char_perso[nbr+7], nbr)
                    new_perso.update_color()
                    const.persos.append(new_perso)
    elif cmd.split(";")[0] == "co_perso":
        const.output=buffer

    elif cmd == "get_inv":
        const.output=buffer
    elif cmd == "get_mobs":
        const.mobs=bool(int(buffer))

    elif cmd.split(";")[0] == "get_map":
        const.map = map.char2map(buffer, True) 

    elif cmd == "get_welcome":
        const.events.append(buffer)

    elif cmd.split(";")[0] == "get_last_event":
        const.id_last_event=int(buffer)
    elif cmd.split(";")[0] == "get_last_event_map":
        const.id_last_event_map=int(buffer)
        print const.id_last_event_map

    elif cmd.split(";")[0] == "get_event_map":
        buffer = buffer.split("\n")
        id_last_event = buffer[0]
        buffer.remove(id_last_event)
        if buffer != [""]:
            const.events_map.extend(buffer)
        return id_last_event

    elif cmd.split(";")[0] == "say":
        if cmd.split(";")[1] in ["/help", "/list", "/ls", "/welcome"]:
            const.events.append(buffer)

    elif cmd.split(";")[0] == "get_event":
        buffer = buffer.split("\n")
        id_last_event = buffer[0]
        buffer.remove(id_last_event)
        if buffer != [""]:
            const.events.extend(buffer)
        return id_last_event
    return True


