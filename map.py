#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

from bloc import *

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
                prop = [int(i) for i in prop]
                pmap.append(prop)
         
        for i in pmap:
            pbloc = i
            if pbloc[0] == 0:
                bloc = Porte(pbloc[1], 0)
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
            elif pbloc[0] == 1:
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
                bloc = BlocDanger(pbloc[1], pbloc[2])
                bloc.move_el(pbloc[3], pbloc[4])
                map.append(bloc)
            elif pbloc[0] == 6:
                bloc = Porte(pbloc[1], 1)
                bloc.move_el(pbloc[2], pbloc[3])
                map.append(bloc)
    except IOError:
        print(path + " : Map introuvable !")

    finally:
        return map

def save_map(nom, map):
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
                tampon = tampon + "0," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"
            if (i.etat == 1):
                tampon = tampon + "6," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"
        elif isinstance(i, Bloc):
            tampon = tampon + "1," + str(i.picture) +","+str(i.x)+","+str(i.y)+"\n"
    file.write(tampon)
    file.close()
