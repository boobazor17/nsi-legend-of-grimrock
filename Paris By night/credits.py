import pygame
pygame.init()


def afficher_credits(screen, font):
    screen.fill((0, 0, 0))
    
    texte = font.render("ici ce sera les credits dcp", True, (16711935))
    screen.blit(texte, (450, 300))
