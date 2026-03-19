import pygame
import math 
pygame.init()
# x_max , x_min, y_max, y_min
x=300 
y=200
speed=10


#création de la classe contenant les caractéristiques des personnages
class personnage:
    def __init__(self, nom, pv, pvmax, attaque):
        self.nom = nom
        self.pv = pv
        self.pvmax = pvmax
        self.attaque = attaque

Fantome = personnage("Fantome", 100, 100, 20)
Rat = personnage("Rat", 50, 50, 10)

#création de la fenetre du jeu
pygame.display.set_caption("Fenêtre d'accueil")
screen = pygame.display.set_mode((720,720 ))

running = True 
clock = pygame.time.Clock()
while running == True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    screen.fill((201,158,89))
    
# déplacement du personnage uniforme dans chaque directions

    touches = pygame.key.get_pressed()
    if touches[pygame.K_z] or touches[pygame.K_UP]:
        if (touches[pygame.K_d] or touches[pygame.K_RIGHT]) ^ (touches[pygame.K_q] or touches[pygame.K_LEFT]): # ^ = ou exclusif ( xor)
            y -= speed/math.sqrt(2)
        else:
            y -= speed
    if touches[pygame.K_s] or touches[pygame.K_DOWN]:
        if (touches[pygame.K_d] or touches[pygame.K_RIGHT]) ^ (touches[pygame.K_q] or touches[pygame.K_LEFT]): 
            y += speed/math.sqrt(2)
        else:
            y += speed

    if touches[pygame.K_q] or touches[pygame.K_LEFT]:
        if (touches[pygame.K_z] or touches[pygame.K_UP]) ^ (touches[pygame.K_s] or touches[pygame.K_DOWN]):
            x -= speed/math.sqrt(2)
        else:
            x -= speed

    if touches[pygame.K_d] or touches[pygame.K_RIGHT]:
        if (touches[pygame.K_z] or touches[pygame.K_UP]) ^ (touches[pygame.K_s] or touches[pygame.K_DOWN]):
            x += speed/math.sqrt(2)
        else : 
            x += speed




    pygame.draw.circle(screen,(255, 0, 0),(x,y),20) 
    pygame.display.update()


def camera_(f):
    pass
