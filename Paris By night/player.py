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
            self.direction = pygame.math.Vector2(1,0) # initialisé vers la droite
           
        
        def draw(self, screen, follow):
            if self.pv > 0:
                x = int(self.rect.centerx - follow.camera.offset.x)
                y = int(self.rect.centery - follow.camera.offset.y)
                pygame.draw.circle(screen, (190, 65, 65), (x, y), self.radius)
                

        def attaque(self):
            if self.pv > 0:
                if pygame.key.get_pressed()[pygame.K_z]:
                     pass



             # Personnages jouables — chacun a ses propres stats
            Fantome = Player("Fantome", 100, 100, 20)
            Rat     = Player("Rat",     50,  50,  10)

        def recevoir_degat(self, degat, liste_equipe):
            for elem in liste_equipe:
                if elem.pv > 0 :
                     elem.pv -= degat
                     break
            if all(elem.pv <=0 for elem in liste_equipe):
                self.pv = 0
        

        


        
