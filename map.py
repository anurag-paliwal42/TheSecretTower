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
from bloc import *
from item import *

# Chargement carte
def open_map(path):
    pmap = [] 
    map = []
    try:
        file = open("data/"+ path, 'r')
        elements = []
        tampon = file.read()
        
        elements = tampon.split("\n")
        
        for element in elements:
            if element != "":
                prop = element.split(",")
                if int(prop[0]) == 11 or  int(prop[0])==22:
                    for i in range(4):
                        prop[i] = int(prop[i])
                else:
                    prop = [int(i) for i in prop]
                pmap.append(prop)
                
        for i in pmap:
            pbloc = i
            if pbloc[0] == 0:
                bloc = Porte(pbloc[1], 0, pbloc[4])
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            elif pbloc[0] == 1:
                if pbloc[1] == 1:
                    bloc = Stone(pbloc[1])
                elif pbloc[1] == 6:
                    bloc = Wood(pbloc[1])
                else:
                    bloc = Bloc(pbloc[1])
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            elif pbloc[0] == 2:
                bloc = BlocMouvant(pbloc[1], pbloc[2], pbloc[3], pbloc[4], pbloc[5])
                map.append(bloc)
            elif pbloc[0] == 3:
                bloc = BlocDisp(pbloc[1], pbloc[2])
                bloc.move_el(pbloc[3], pbloc[4])
                map.append(bloc)
            elif pbloc[0] == 4:
                if pbloc[1] == 2:
                    bloc = Lava()
                    bloc.move_el(pbloc[3], pbloc[4])
                    map.append(bloc)    
                else:
                    bloc = BlocDanger(pbloc[1], pbloc[2])
                    bloc.move_el(pbloc[3], pbloc[4])
                    map.append(bloc)
            elif pbloc[0] == 6:
                bloc = Porte(pbloc[1], 1, pbloc[4])
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            elif pbloc[0] == 7:
                bloc = Porte(pbloc[1], 2, pbloc[4], pbloc[5])
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            # Terre
            elif pbloc[0] == 8:
                bloc = Terre(pbloc[1])
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            # Echelle
            elif pbloc[0] == 9:
                bloc = Echelle(pbloc[1])
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            # Atelier
            elif pbloc[0] == 10:
                bloc = Atelier(pbloc[1])
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            # Coffre
            elif pbloc[0] == 11:
                bloc = Coffre(pbloc[1])
                bloc.move_el(pbloc[2], pbloc[3])
                bloc.inv.load(pbloc[4])                 
                map.append(bloc)
            # Forge
            elif pbloc[0] == 12:
                bloc = Forge(pbloc[1])
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            # Torch
            elif pbloc[0] == 13:
                bloc = Torch(pbloc[1])
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            # Coal
            elif pbloc[0] == 14:
                bloc = Coal(pbloc[1])
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            # Copper
            elif pbloc[0] == 15:
                bloc = Copper(pbloc[1])
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            # Iron
            elif pbloc[0] == 16:
                bloc = Iron(pbloc[1])
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            # Titanium
            elif pbloc[0] == 17:
                bloc = Titanium(pbloc[1])
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            # Gold
            elif pbloc[0] == 18:
                bloc = Gold(pbloc[1])
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            # Diamond
            elif pbloc[0] == 19:
                bloc = Diamond(pbloc[1])
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            # Tin
            elif pbloc[0] == 20:
                bloc = Tin(pbloc[1])
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            # Uranium
            elif pbloc[0] == 21:
                bloc = Uranium(pbloc[1])
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            # Sign
            elif pbloc[0] == 22:
                bloc = Sign(pbloc[1], pbloc[4].replace("/n", "\n").replace("/c",","))
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            # Furnace
            elif pbloc[0] == 23:
                bloc = Furnace(pbloc[1])
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)

    except IOError:
        print(path + " : Map introuvable !")

    finally:
        return map

    

def save_map(nom, map):
    if not os.path.isdir("data/map/custom/"):
        os.mkdir("data/map/custom/")
    file = open("data/"+nom, "w")
    tampon = ""
    for i in map:
        if isinstance(i, BlocMouvant):
            tampon = tampon + "2," + str(i.picture) +","+str(i.debut_x)+","+str(i.debut_y)+","+str(i.dep_x)+","+ str(i.dep_y)+"\n"
        elif isinstance(i, BlocDisp):
            tampon = tampon + "3, " + str(i.picture) +","+str(i.begin)+","+str(i.x)+","+str(i.y)+"\n"
        elif isinstance(i, BlocDanger):
            tampon = tampon + "4," + str(i.picture) +","+str(i.atk)+","+str(i.x)+","+str(i.y)+"\n"
        elif isinstance(i, Porte):
            if (i.etat == 0):
                tampon = tampon + "0," + str(i.picture) +","+str(i.x)+","+str(i.y)+","+str(i.id)+"\n"
            if (i.etat == 1):
                tampon = tampon + "6," + str(i.picture) +","+str(i.x)+","+str(i.y)+","+str(i.id)+"\n"
            if (i.etat == 2):
                tampon = tampon + "7," + str(i.picture) +","+str(i.x)+","+str(i.y)+","+str(i.id)+","+str(i.target)+"\n"
        elif isinstance(i, Terre):
            tampon = tampon + "8," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"
        elif isinstance(i, Echelle):
            tampon = tampon + "9," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"
        elif isinstance(i, Atelier):
            tampon = tampon + "10," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"
        elif isinstance(i, Coffre):
            tampon = tampon + "11," + str(i.picture) +","+str(i.x)+","+str(i.y)+","+i.inv.save()+"\n"
            #tampon = tampon + "11," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"
        elif isinstance(i, Forge):
            tampon = tampon + "12," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"
        elif isinstance(i, Torch):
            tampon = tampon + "13," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"
        elif isinstance(i, Coal):
            tampon = tampon + "14," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"
        elif isinstance(i, Copper):
            tampon = tampon + "15," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"
        elif isinstance(i, Iron):
            tampon = tampon + "16," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"
        elif isinstance(i, Titanium):
            tampon = tampon + "17," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"
        elif isinstance(i, Gold):
            tampon = tampon + "18," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"
        elif isinstance(i, Diamond):
            tampon = tampon + "19," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"
        elif isinstance(i, Tin):
            tampon = tampon + "20," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"
        elif isinstance(i, Uranium):
            tampon = tampon + "21," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"
        elif isinstance(i, Sign):
            tampon = tampon + "22," + str(i.picture) +","+str(i.x)+","+str(i.y)+","+i.txt.replace("\n", "/n").replace(",", "/c")+"\n"
        elif isinstance(i, Furnace):
            tampon = tampon + "23," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"
        elif isinstance(i, Bloc):
            tampon = tampon + "1," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"

    file.write(tampon)
    file.close()
