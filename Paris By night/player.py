from tkinter import Image

import pygame
pygame.init()
from camera import *
from Physique import Physique
    

class Player(Physique):
        def __init__(self, x, y, radius=20,):
            super().__init__(x, y, radius*2, radius*2)
            self.radius = radius
            self.rect = pygame.Rect(x, y , radius * 2, radius * 2)
            self.pv = 100
            self.pvmax = 100
            self.invincible_temps =  - 1000
            self.duree_invincibilite = 2000
            self.position = pygame.math.Vector2(x,y)
           
        
        def draw(self, screen, follow):
            if self.pv > 0:
                x = int(self.rect.centerx - follow.camera.offset.x)
                y = int(self.rect.centery - follow.camera.offset.y)
                pygame.draw.circle(screen, (190, 65, 65), (x, y), self.radius)
                

        def attaque():
             


             # Personnages jouables — chacun a ses propres stats
            Fantome = Player("Fantome", 100, 100, 20)
            Rat     = Player("Rat",     50,  50,  10)

"""liste_personnages = ["Fantome", "Rat"]
l=[]
if len (l)==0:
    for i in range (len(liste_personnages)):
        l.append(Player(liste_personnages[i], 100, 100, 20))"""
        