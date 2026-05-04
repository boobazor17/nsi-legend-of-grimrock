import pygame

pygame.init()

perso1 = pygame.image.load("escargot.png")

fenetre = pygame.display.set_mode((800, 600))


perso4_x, perso4_y = 100, 100

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

fenetre.fill((0, 0, 0))
fenetre.blit(perso1, (perso4_x, perso4_y))
pygame.display.update()

pygame.quit()