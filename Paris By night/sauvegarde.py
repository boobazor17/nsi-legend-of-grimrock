import pygame
pygame.init()


def afficher_sauvegarde(screen, font):
    screen.fill((0, 0, 0))
    
    texte = font.render("sauvegarder partie", True, (16711935))
    screen.blit(texte, (450, 300))
