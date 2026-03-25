import pygame
import math
from camera import *

def lancer():
 
 pygame.init()
 font = pygame.font.Font(None,40)
 width = 1080
 height = 720
 speed = 10
 
 screen = pygame.display.set_mode((width, height))
 pygame.display.set_caption("Fenêtre d'accueil")
  
 invicible  = 0 #permet d'être invincible après la réapparition
 
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
         self.pv = 100
         self.pvmax = 100
         self.invincible_temps =  - 1000
         self.duree_invincibilite = 2000
 
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
         self.attaque_dernier_temps = - 1000
         self.attaque_cooldown = 400
         self.proj_x = self.x
         self.proj_y = self.y
         self.proj_actif = False
         self.proj_vitesse = 5
         self.proj_rayon = 8
 
     def draw(self, screen, offset):
         draw_x = self.x - offset.x
         draw_y = self.y - offset.y
         pygame.draw.circle(screen, (99, 69, 45), (int(draw_x), int(draw_y)), 20)
 
         if self.proj_actif:
             proj_draw_x = int(self.proj_x - offset.x)
             proj_draw_y = int(self.proj_y - offset.y)
             pygame.draw.circle(screen, (255, 165, 0), (proj_draw_x, proj_draw_y), self.proj_rayon)
 
     def attaque_m(self,player):
        dx = self.x - player.rect.centerx
        dy = self.y - player.rect.centery
        distance_reelle = math.sqrt(int(dx**2 + dy**2)) # avec le théoreme de Pythagore on calcule la distance entre le monstre et le joueur
        temps =  pygame.time.get_ticks()
        if self.distance_attaque >= distance_reelle and temps - self.attaque_dernier_temps >= self.attaque_cooldown :
            self.attaque_dernier_temps = temps
            self.proj_x = self.x
            self.proj_y = self.y
            if temps - player.invincible_temps >= player.duree_invincibilite and player.pv >= 0:  
                 self.proj_actif = True
                 
        if self.proj_actif and temps - self.attaque_dernier_temps <= 1500:
            ddx = player.rect.centerx - self.proj_x
            ddy = player.rect.centery - self.proj_y
            dist = math.sqrt(ddx**2 + ddy**2)
            self.proj_x += (ddx / dist) * self.proj_vitesse
            self.proj_y += (ddy / dist) * self.proj_vitesse 

            if player.rect.collidepoint(self.proj_x,self.proj_y):
                player.pv -= self.attaque
                self.proj_actif = False    
        else:
            self.proj_actif = False # on detruit le projectile , on met le else après le deuxième bloc if car si la condition est False donc tout le bloc est ignoré, y compris le proj_actif = False. Le projectile reste donc actif indéfiniment. :(
                
           
                 
 
     def deplacement(self,player):
         dx = self.x - player.rect.centerx
         dy = self.y - player.rect.centery
         distance_reelle = math.sqrt(int(dx**2 + dy**2))
         if self.distance >= distance_reelle :
             if dx >= 70 or dx <= -70 :
                 if dx >= 50:
                     self.x -= 3*speed//5
                 else:
                     self.x += 3*speed//5
             if dy >= 70 or dy <= -70:
                 if dy >= 70:
                     self.y -= 3*speed//5
                 else:
                     self.y += 3*speed//5
         else:
             pass # le monstre fait sa ronde
 
 Fantome = Personnage("Fantome", 100, 100, 20)
 Rat     = Personnage("Rat",     50,  50,  10)
 
 Julien = monstre("Julien" , 50, 60, 10, 220, 100)
 
 clock   = pygame.time.Clock()
 running = True
  
 while running:
     clock.tick(60)
  
     for event in pygame.event.get():
         if event.type == pygame.QUIT:
             running = False
  
     screen.fill((201, 158, 89))
 
     # déplacement du personnage uniforme dans chaque directions
     touches = pygame.key.get_pressed()
     if player.pv > 0:
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
 
     # création de la barre de vie , rectangle noir puis rectangle rouge représentant la vie
     hpb_w = 200
     hpb_h = 12
     hpb_x = width/2 - hpb_w/2
     hpb_y = height/2 + 4*height//9  # 1/18px au dessus du bas de l'écran 
     barre_hp = pygame.Rect(hpb_x, hpb_y, hpb_w, hpb_h)
     pygame.draw.rect(screen, (0, 0, 0), barre_hp )
     hpb_w = 200 - 200 + player.pv*2
     if hpb_w > 200 :
         hpb_w = 200
     hpb_h = 12
     hpb_x = width/2 - hpb_w/2
     hpb_y = height/2 + 4*height//9  # 1/18px au dessus du bas de l'écran 
     barre_hp2 = pygame.Rect(hpb_x, hpb_y, hpb_w, hpb_h)
     pygame.draw.rect(screen, (255, 0, 0), barre_hp2 )
     cam.scroll()
 
     # Dessin du joueur
     if player.pv > 0:
         player.draw(screen, cam.offset)
 
     if player.pv <= 0:
             # dimensions du bouton
         bouton_w = 200
         bouton_h = 60
 
         # centré horizontalement, en dessous du joueur
         bouton_x = width/2 - bouton_w/2
         bouton_y = height/2 + 50  # 50px en dessous du centre (là où est le joueur)
 
         bouton_rejouer = pygame.Rect(bouton_x, bouton_y, bouton_w, bouton_h)
         pygame.draw.rect(screen, (139, 94, 44), bouton_rejouer)
 
         texte = font.render("Rejouer", True, (245, 240, 220))
         texte_x = bouton_x + bouton_w/2 - texte.get_width()/2   # centré dans le bouton
         texte_y = bouton_y + bouton_h/2 - texte.get_height()/2  # centré dans le bouton
         screen.blit(texte, (texte_x, texte_y))
         if event.type == pygame.MOUSEBUTTONDOWN:
             if bouton_rejouer.collidepoint(event.pos):
                 player.pv = player.pvmax 
                 temps =  pygame.time.get_ticks()
                 player.invincible_temps = temps
                 
     Julien.attaque_m(player)
     Julien.deplacement(player)
     Julien.draw(screen, cam.offset)
     # Exemple d'objet fixe dans le monde (cercle bleu)
     pygame.draw.circle(screen, (0, 0, 255), (100 - int(cam.offset.x), 50 - int(cam.offset.y)), 20)
  
     pygame.display.update()
     
 pygame.quit()
