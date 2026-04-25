import pygame
import math
from camera import *
pygame.init()
from Physique import Physique  
from Physique import projectile



speed = 10
class monstre(Physique):
        def __init__(self,x,y,nom,pv,pvmax,attaque,distance,distance_attaque):
            super().__init__(x,y,40,40)
            print(type(self.position))
            self.position = pygame.math.Vector2(x,y)
            self.nom = nom
            self.pv = pv
            self.pvmax = pvmax
            self.attaque = attaque
            self.distance = distance 
            self.distance_attaque = distance_attaque
            self.attaque_dernier_temps = - 1000
            self.attaque_cooldown = 400
            self.waypoints = [self.position.copy(), self.position+(200,0), self.position+(200,200), self.position+(0,200)]  # un carré par défaut
            self.waypoint_actuel = 0
            self.proj = projectile(x, y, 5, 8, 0, 0, 10,0) # initialisation du projectile (position(x,y)  vitesse , rayon, vitesse_x, vitesse_y, degat)
            self.rect = pygame.Rect(x, y, 40, 40)
    
        def draw(self, screen, follow):
            if self.pv > 0:
                pygame.draw.circle(screen, (99, 69, 45), follow.appliquer(self.position), 20)

            if self.proj.proj_actif and self.pv > 0:
                pygame.draw.circle(screen, (255, 165, 0), follow.appliquer(self.proj.position_proj), self.proj.proj_rayon)
                
    
        def attaque_m(self,player,list_object,liste_equipe):
            if self.pv > 0:
                dx = self.position.x - player.rect.centerx
                dy = self.position.y - player.rect.centery
                distance_reelle = math.sqrt(int(dx**2 + dy**2)) # avec le théoreme de Pythagore on calcule la distance entre le monstre et le joueur
                temps =  pygame.time.get_ticks()
                if self.distance_attaque >= distance_reelle and temps - self.attaque_dernier_temps >= self.attaque_cooldown :
                    self.attaque_dernier_temps = temps
                    if temps - player.invincible_temps >= player.duree_invincibilite and player.pv > 0:  
                        self.proj.lancer(self.position,player)
                    else :
                        for object in list_object: # check tous les objets de la liste pour voir s'il y a une collision avec le projectile
                            if object.rect.collidepoint(self.proj.position_proj):    
                                self.proj.proj_actif = False
                if self.proj.proj_actif and temps - self.attaque_dernier_temps <= 1500:
                    self.proj.position_proj += (self.proj.proj_vitesse_x, self.proj.proj_vitesse_y)
                    self.proj.collisions(player,liste_equipe)            
                else:
                    self.proj.proj_actif = False # on detruit le projectile , on met le else après le deuxième bloc if car si la condition est False donc tout le bloc est ignoré, y compris le proj_actif = False. Le projectile reste donc actif indéfiniment. :(
                    
            
                    
    
        def deplacement(self,player,l):
            self.velocity.x = 0
            self.velocity.y = 0
            if self.pv > 0:
                dx = self.position.x - player.rect.centerx
                dy = self.position.y - player.rect.centery
                distance_reelle = math.sqrt(int(dx**2 + dy**2))
                if self.distance >= distance_reelle and player.pv > 0:
                    if distance_reelle == 0:
                        distance_reelle = 1  # pour éviter la division par zéro
                    if distance_reelle > 70:
                            # Déplacement normalisé : dx/distance_reelle donne la direction (entre -1 et 1) et on multiplie par la vitesse pour garder une vitesse constante quelle que soit la direction
                            self.velocity.x -= (dx / distance_reelle) * 2*speed/3  # normalisé
                       
                            self.velocity.y -= (dy / distance_reelle) * 2*speed/3  # normalisé

                else:  # ronde — on récupère le waypoint actuel
                    cible_x, cible_y = self.waypoints[self.waypoint_actuel]
                    distance_x = cible_x - self.position.x 
                    distance_y = cible_y - self.position.y 
                    distance_total = math.sqrt(distance_x**2 + distance_y**2)
                    if distance_total < 10 and distance_total > - 10 :
                        self.waypoint_actuel = (self.waypoint_actuel + 1) % len(self.waypoints)
                    else:
                        self.velocity.x += (distance_x / distance_total) * 2*speed/5  # normalisé 
                        self.velocity.y += (distance_y / distance_total) * 2*speed/5
            self.position.x += self.velocity.x
            self.rect.center = self.position
            self.collisions(l)  # faire en sorte que le système de collisions marche
            self.position.y += self.velocity.y
            self.rect.center = self.position
            self.collisions(l)  # faire en sorte que le système de collisions marche


        def dash(self,player,liste_equipe,degat):
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
                        player.recevoir_degat(degat, liste_equipe)



        def liste(self,list_ennemi):            # pour supprimer les ennemis morts de la liste des ennemis
                    list_ennemi[:] = [monstreee for monstreee in list_ennemi if monstreee.pv >0] # notation slice pour modifier la liste originale , pop l'index créait des bug car on manipule un index qui n'existe plus 






