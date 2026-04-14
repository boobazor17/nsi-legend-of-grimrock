import pygame

pygame.init()

perso1 = pygame.image.load("fantome.png")

fenetre = pygame.display.set_mode((800, 600))


perso1_x, perso1_y = 100, 100

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

fenetre.fill((0, 0, 0))
fenetre.blit(perso1, (perso1_x, perso1_y))
pygame.display.update()

pygame.quit()