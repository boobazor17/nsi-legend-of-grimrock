import pygame
pygame.init()

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
while running == True:
    for event in pygame.event.get():
        screen.fill((201,158,89))


pygame.display.update()

if event.type == pygame.QUIT:
            running = False
            pygame.quit()
