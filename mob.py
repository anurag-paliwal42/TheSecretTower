#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

from element import *
from bloc import *
import const

# Pygame
import pygame
from pygame.locals import *


class Mob(Element):
    
    def __init__(self, id):
        Element.__init__(self)
        self.id = id
        self.vie = 10
        self.atk = 1
        self.sens = True
        self.changement = 0
        self.rang_image = 0



        self.isingrav=False
        self.v_y = 0
        
        self.anim()
        self.rect.width = 20
        self.rect.height = 40
        self.rect = self.rect.move(15, 10)

    def update(self, map):
        if self.vie > 0:
            self.tomber(map)
            if self.sens:
                if self.move(1, 0, map) != True:
                    if random.randint(0,3) == 0 and not self.isingrav:
                        self.sens = False
                    else:
                        self.sauter(-10)
            elif not self.sens:
                if self.move(-1, 0, map) != True:
                    if random.randint(0,3) == 0 and not self.isingrav:
                        self.sens = True
                    else:
                        self.sauter(-10)
            self.anim()
            

    def subir_degats(self, degat):
        if (self.vie > 0):
            self.vie = self.vie - degat
            self.sauter(-5)
            return True
        if (self.vie <= 0):
            return False


    def anim(self):
        image = copy.copy(const.vide)
        rect = pygame.Rect(self.rang_image*50,0, 50,50)

        if time() - self.changement > 0.1 and not self.isingrav:
            self.changement = time()
            if self.rang_image < 2:
                self.rang_image += 1
            else:
                self.rang_image = 0
            rect = pygame.Rect(self.rang_image*50,0, 50,50)
        elif self.isingrav:
            rect = pygame.Rect(100, 0, 50,50)
        
        image.blit(const.sprite_mobs, (0,0), rect)
        if not self.sens:
            image = pygame.transform.flip(image, True, False)
        self.changer_image(image)


    def sauter(self, y, force = False):
        if self.isingrav == False or force:
            self.v_y = y
            self.isingrav = True

    def tomber(self, map):
        if self.y < 550 or self.v_y:
           if self.move(0, self.v_y, map):
               if self.v_y <> 0:
                   self.isingrav = True
               self.v_y = self.v_y + 1


           else:
               self.isingrav = False
               self.v_y = 0

        else: 
            self.isingrav = False

    def move(self, x, y, map):
        if self.collided_map(x, y, map) == False:
            if self.y+y < 550: 
                self.move_el(0,y)
            else:
                self.move_el(0, 550-self.y)
                
            if self.x + x > 0 and self.x +x < 750:
                self.move_el(x,0)
            else:
                return False
            return True
        
        return False

    def collided_map(self, dep_x, dep_y, map):
        future_rect = pygame.Rect(self.rect)
        future_rect = future_rect.move(dep_x, dep_y)
        collided = False
        # Vérification pour chaques éléments de la map
        for i in map:
            if future_rect.colliderect(i.rect):
 
                # Vérif bloc mouvant
                if isinstance(i, BlocMouvant):
                    # Vérif position
                    if (self.y-dep_y) <= i.y-50:
                        if i.aller:
                            if i.x < i.dep_x+i.debut_x:
                                self.move(1,0, map)
                        else:
                            if i.x > i.debut_x:
                                self.move(-1,0, map)
                            if i.y > i.debut_y:
                                self.move(0,-1, map)
                        collided=True
                elif isinstance(i, BlocDisp):
                    if (i.etat):
                        collided=True
                elif isinstance(i, BlocDanger):
                    if i.atk >= self.vie:
                        self.subir_degats(i.atk)
                    collided=True
                elif not isinstance(i, Porte) and not isinstance(i, Echelle) and not isinstance(i, Deco):
                    collided=True
            
        return collided

    def collided_perso(self, dep_x, dep_y, perso):
        future_rect = pygame.Rect(self.rect)
        future_rect = future_rect.move(dep_x, dep_y)

        if future_rect.colliderect(perso.rect) and self.vie > 0:
            perso.subir_degats(self.atk)
            return True

        return False
        
