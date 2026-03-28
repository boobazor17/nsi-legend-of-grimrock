import pygame
import math
pygame.init()

speed = 10
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
            # pour les déplacements automatiques du monstre
            self.waypoints = [(self.x, self.y), (self.x +200, self.y), (self.x +200, self.y+ 200), (self.x, self.y+200)]  # un carré par défaut
            self.waypoint_actuel = 0 
    
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
            else:  # ronde — on récupère le waypoint actuel
                cible_x, cible_y = self.waypoints[self.waypoint_actuel]
                distance_x= cible_x - self.x 
                distance_y = cible_y - self.y 
                distance_total = math.sqrt(distance_x**2 + distance_y**2)
                if distance_total < 10 and distance_total > - 10 :
                    self.waypoint_actuel = (self.waypoint_actuel + 1) % len(self.waypoints)
                else:
                    self.x += (distance_x / distance_total) * 2*speed//5  # normalisé !
                    self.y += (distance_y / distance_total) * 2*speed//5

"""# Classe Player — le cercle rouge est le personnage
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
    # il sera lié à l'équipe plus tard"""
