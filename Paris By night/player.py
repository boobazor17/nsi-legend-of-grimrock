import pygame
pygame.init()



class Player:
        def __init__(self, x, y, radius=20):
            self.radius = radius
            self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
            self.pv = 100
            self.pvmax = 100
            self.invincible_temps =  - 1000
            self.duree_invincibilite = 2000
    
        def draw(self, screen, offset):
            draw_x = self.rect.centerx - offset.x
            draw_y = self.rect.centery - offset.y
            pygame.draw.circle(screen, (255, 0, 0), (int(draw_x), int(draw_y)), self.radius)