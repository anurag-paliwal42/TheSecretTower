#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

from bloc import *

MAP0 = [[1, 1, 200, 550], [1, 1, 250, 500], [1,1,350, 400], [1,1, 450, 300], [1,1,200,150], [1,1,0,450],[2,1,60,200,0,350], [1,1,350,200], [2,1,450,200,100,0],
[3, 1, 0, 450, 500],
[3, 1, 5, 500, 500],
[4,1, 1, 600,550]]

MAPS = [MAP0]

def open_map(id_map):
    pmap = MAPS[id_map] 
    map = []
#   with open('data/map/map1', 'r') as file:
 #       elements = []
  #      tampon = file.read()
   #     
    #    elements = tampon.split("\n")
        
     #   for element in elements:
      #      prop = element.split(" ")
       #     for i in prop:
        #       if i != " ":
         #           print i
          #          i = int(i)
          #  print prop"""
         
    for i in pmap:
        pbloc = i
        if pbloc[0] == 1:
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
    return map

"""   

    bloc = Bloc(1)
    bloc.move_el(200,550)

    map.append(bloc)

    bloc2 = Bloc(1)
    bloc2.move_el(250,500)
    map.append(bloc2)

    bloc3 = Bloc(1)
    bloc3.move_el(350,400)
    map.append(bloc3)

    bloc4 = Bloc(1)
    bloc4.move_el(450,300)
    map.append(bloc4)

    bloc5 = Bloc(1)
    bloc5.move_el(350,200)
    map.append(bloc5)

    bloc5 = Bloc(1)
    bloc5.move_el(200,150)
    map.append(bloc5)

    bloc7 = Bloc(1)
    bloc7.move_el(0,450)
    map.append(bloc7)

    bloc6 = BlocMouvant(1, 60, 200, 0, 350)
    map.append(bloc6)

    bloc8 = BlocMouvant(1, 450, 200, 100, 0)
    map.append(bloc8)

    bloc9 = BlocDisp(1)
    bloc9.move_el(450,500)
    map.append(bloc9)
    
    bloc10 = BlocDisp(1, 5)
    bloc10.move_el(500,500)
    map.append(bloc10)

    bloc11 = BlocDanger(1, 1)
    bloc11.move_el(600,550)
    map.append(bloc11)"""







