import os
import pygame
 
def charger_images():
    base_dir = os.path.dirname(__file__)
    tower_path = os.path.join(base_dir, "assets/tower.png")
    tower = pygame.image.load(tower_path).convert_alpha()
    return {
        "tower": tower
    }
 

