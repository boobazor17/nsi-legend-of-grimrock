import pygame
import math
from camera import *
pygame.init()
from Physique import Physique

speed = 10
class monstre(Physique):
        def __init__(self,x,y,nom,pv,pvmax,attaque,distance,distance_attaque):
            self.position = pygame.math.Vector2(x,y)
            self.nom = nom
            self.pv = pv
            self.pvmax = pvmax
            self.attaque = attaque
            self.distance = distance 
            self.distance_attaque = distance_attaque
            self.attaque_dernier_temps = - 1000
            self.attaque_cooldown = 400
            self.position_proj = pygame.math.Vector2(x,y)
            self.proj_actif = False
            self.proj_vitesse = 5
            self.proj_rayon = 8
            self.waypoints = [self.position.copy(), self.position+(200,0), self.position+(200,200), self.position+(0,200)]  # un carré par défaut
            self.waypoint_actuel = 0
    
        def draw(self, screen, follow):
            if self.pv > 0:
                pygame.draw.circle(screen, (99, 69, 45), follow.appliquer(self.position), 20)

            if self.proj_actif:
                pygame.draw.circle(screen, (255, 165, 0), follow.appliquer(self.position_proj), self.proj_rayon)
    
        def attaque_m(self,player):
            if self.pv > 0:
                dx = self.position.x - player.rect.centerx
                dy = self.position.y - player.rect.centery
                distance_reelle = math.sqrt(int(dx**2 + dy**2)) # avec le théoreme de Pythagore on calcule la distance entre le monstre et le joueur
                temps =  pygame.time.get_ticks()
                if self.distance_attaque >= distance_reelle and temps - self.attaque_dernier_temps >= self.attaque_cooldown :
                    self.attaque_dernier_temps = temps
                    if temps - player.invincible_temps >= player.duree_invincibilite and player.pv >= 0:  
                        self.proj_actif = True
                        self.position_proj = self.position.copy()
                        ddx = player.rect.centerx - self.position_proj.x
                        ddy = player.rect.centery - self.position_proj.y
                        dist = math.sqrt(ddx**2 + ddy**2)
                        self.proj_vitesse_x = (ddx / dist) * self.proj_vitesse
                        self.proj_vitesse_y = (ddy / dist) * self.proj_vitesse 
                if self.proj_actif and temps - self.attaque_dernier_temps <= 1500:
                    self.position_proj += (self.proj_vitesse_x, self.proj_vitesse_y)
                    if player.rect.collidepoint(self.position_proj):
                        player.pv -= self.attaque
                        self.proj_actif = False
                else:
                    self.proj_actif = False # on detruit le projectile , on met le else après le deuxième bloc if car si la condition est False donc tout le bloc est ignoré, y compris le proj_actif = False. Le projectile reste donc actif indéfiniment. :(
                    
            
                    
    
        def deplacement(self,player):
            if self.pv > 0:
                dx = self.position.x - player.rect.centerx
                dy = self.position.y - player.rect.centery
                distance_reelle = math.sqrt(int(dx**2 + dy**2))
                if self.distance >= distance_reelle and player.pv > 0:
                    if dx >= 70 or dx <= -70 :
                        if dx >= 50:
                            self.position.x -= 3*speed//5
                        else:
                            self.position.x += 3*speed//5
                    if dy >= 70 or dy <= -70:
                        if dy >= 70:
                            self.position.y -= 3*speed//5
                        else:
                            self.position.y += 3*speed//5
                else:  # ronde — on récupère le waypoint actuel
                    cible_x, cible_y = self.waypoints[self.waypoint_actuel]
                    distance_x = cible_x - self.position.x 
                    distance_y = cible_y - self.position.y 
                    distance_total = math.sqrt(distance_x**2 + distance_y**2)
                    if distance_total < 10 and distance_total > - 10 :
                        self.waypoint_actuel = (self.waypoint_actuel + 1) % len(self.waypoints)
                    else:
                        self.position.x += (distance_x / distance_total) * 2*speed/5  # normalisé 
                        self.position.y += (distance_y / distance_total) * 2*speed/5


        def dash(self,player):
            if self.pv > 0 :
                temps =  pygame.time.get_ticks() 
                
                dx = self.position.x - player.rect.centerx
                dy = self.position.y - player.rect.centery
                distance_reelle = math.sqrt(int(dx**2 + dy**2))
                if self.distance >= distance_reelle and player.pv > 0:
                    
                    if (dx >= 70 or dx <= -70) and (dy >= 70 or dy <= -70) and temps - self.attaque_dernier_temps >= self.attaque_cooldown + 2000:
                        self.attaque_dernier_temps = temps
                        self.position.x = player.rect.centerx + (10 if dx >= 0 else -10)
                        self.position.y = player.rect.centery + (10 if dy >= 0 else -10)
                        player.pv -= 3 * self.attaque


