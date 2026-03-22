import pygame
import math
from camera import *
 
pygame.init()

width = 1080
height = 720
speed = 10
 
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fenêtre d'accueil")
 


# Classe Player — le cercle rouge est le personnage
class Personnage:
    def __init__(self, nom, pv, pvmax, attaque):
        self.nom = nom
        self.pv = pv
        self.pvmax = pvmax
        self.attaque = attaque

# Personnages jouables — chacun a ses propres stats
Fantome = Personnage("Fantome", 100, 100, 20)
Rat     = Personnage("Rat",     50,  50,  10)

# Player représente le sprite qui se déplace,
# il sera lié à l'équipe plus tard
class Player:
    def __init__(self, x, y, radius=20):
        self.radius = radius
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)

    def draw(self, screen, offset):
        draw_x = self.rect.centerx - offset.x
        draw_y = self.rect.centery - offset.y
        pygame.draw.circle(screen, (255, 0, 0), (int(draw_x), int(draw_y)), self.radius)


# Initialisation joueur + caméra
player = Player(300, 200)
cam    = Camera(player)
follow = Follow(cam, player)
border = Border(cam, player)
auto   = Auto(cam, player)
cam.setmethod(follow)  # mode caméra actif (follow / border / auto)


class monstre:
    def __init__(self,nom,pv,pvmax,attaque,distance,distance_attaque):
        self.nom = nom
        self.pv = pv
        self.pvmax = pvmax
        self.attaque = attaque
        self.distance = distance 
        self.distance_attaque = distance_attaque
        self.x = 0 #position de départ
        self.y = 0 #position de départ

    def attaque_m(self,player):
        # on calcule la vraie distance entre le monstre et le joueur
        dx = self.x - player.rect.centerx
        dy = self.y - player.rect.centery
        player.pv = Fantome.pv 
        distance_reelle = math.sqrt(int(dx**2 +dy**2)) # avec le théoreme de Pythagore on calcule la distance entre le monstre et le joueur
        if self.distance_attaque >= distance_reelle:
            player.pv -= self.attaque    

    def deplacement(self,player):
        dx = self.x - player.rect.centerx
        dy = self.y - player.rect.centery
        player.pv = Fantome.pv 
        distance_reelle = math.sqrt(int(dx**2 +dy**2))
        if self.distance >= distance_reelle:
            pass # le monstre se dirige vers le joueur
        else:
            pass # le monstre fait sa ronde

Fantome = Personnage("Fantome", 100, 100, 20)
Rat     = Personnage("Rat",     50,  50,  10)

Julien = monstre("Julien",50 ,60 ,12 ,50 ,25)

clock   = pygame.time.Clock()
running = True
 
while running:
    clock.tick(60)
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
    screen.fill((201, 158, 89))

    Julien.attaque_m(player)
 
    # déplacement du personnage uniforme dans chaque directions
    touches = pygame.key.get_pressed()
    if touches[pygame.K_z] or touches[pygame.K_UP]:
        if (touches[pygame.K_d] or touches[pygame.K_RIGHT]) ^ (touches[pygame.K_q] or touches[pygame.K_LEFT]): # ^ = ou exclusif (xor)
            player.rect.y -= speed / math.sqrt(2)
        else:
            player.rect.y -= speed
    if touches[pygame.K_s] or touches[pygame.K_DOWN]:
        if (touches[pygame.K_d] or touches[pygame.K_RIGHT]) ^ (touches[pygame.K_q] or touches[pygame.K_LEFT]):
            player.rect.y += speed / math.sqrt(2)
        else:
            player.rect.y += speed
    if touches[pygame.K_q] or touches[pygame.K_LEFT]:
        if (touches[pygame.K_z] or touches[pygame.K_UP]) ^ (touches[pygame.K_s] or touches[pygame.K_DOWN]):
            player.rect.x -= speed / math.sqrt(2)
        else:
            player.rect.x -= speed
    if touches[pygame.K_d] or touches[pygame.K_RIGHT]:
        if (touches[pygame.K_z] or touches[pygame.K_UP]) ^ (touches[pygame.K_s] or touches[pygame.K_DOWN]):
            player.rect.x += speed / math.sqrt(2)
        else:
            player.rect.x += speed
 
    cam.scroll()
 
    # Dessin du joueur
    player.draw(screen, cam.offset)
 
    # Exemple d'objet fixe dans le monde (cercle bleu)
    pygame.draw.circle(screen, (0, 0, 255), (100 - int(cam.offset.x), 50 - int(cam.offset.y)), 20)
 
    pygame.display.update()
 
pygame.quit()
