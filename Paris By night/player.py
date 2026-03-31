import pygame
pygame.init()
from camera import *


class Player:
        def __init__(self, x, y, radius=20):
            self.radius = radius
            self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
            self.pv = 100
            self.pvmax = 100
            self.invincible_temps =  - 1000
            self.duree_invincibilite = 2000
            self.position = pygame.math.Vector2(x,y)
    
        def draw(self, screen, follow):
            pygame.draw.circle(screen, (255, 0, 0), follow.appliquer(self.position) , self.radius)

        def attaque():
             


             # Personnages jouables — chacun a ses propres stats
            Fantome = Player("Fantome", 100, 100, 20)
            Rat     = Player("Rat",     50,  50,  10)
