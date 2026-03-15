import pygame

pygame.init()

perso2 = pygame.image.load("rat.png")

fenetre = pygame.display.set_mode((800, 600))


perso2_x, perso2_y = 100, 100

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


fenetre.fill((0, 0, 0))
fenetre.blit(perso2, (perso2_x, perso2_y))
pygame.display.update()

pygame.quit()