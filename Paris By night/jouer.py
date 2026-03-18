import pygame
pygame.init()

x=300 
y=200
speed=50


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
screen = pygame.display.set_mode((1080,720 ))

running = True 
clock = pygame.time.Clock()
while running == True:
    clock.tick(20)
    for event in pygame.event.get():
        screen.fill((201,158,89))
    


    touches = pygame.key.get_pressed()
    if touches[pygame.K_z] or touches[pygame.K_UP]:
        y -= speed
    if touches[pygame.K_s] or touches[pygame.K_DOWN]:
        y += speed
    if touches[pygame.K_q] or touches[pygame.K_LEFT]:
        x -= speed
    if touches[pygame.K_d] or touches[pygame.K_RIGHT]:
        x += speed
    pygame.display.update()
    pygame.draw.circle(screen,(255, 0, 0),(x,y),20) 
    pygame.display.update()

    if event.type == pygame.QUIT:
            running = False
            pygame.quit()
