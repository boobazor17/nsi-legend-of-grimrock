import pygame
pygame.init()
height= 720
width = 1080

def dessiner_vision(screen, follow, player, rayon=200):
    masque = pygame.Surface((width, height), pygame.SRCALPHA)
    masque.fill((0, 0, 0, 100))
    pos_joueur = follow.appliquer(player.position)
    pygame.draw.circle(masque, (0, 0, 0, 0), pos_joueur, 300)
    screen.blit(masque, (0, 0))