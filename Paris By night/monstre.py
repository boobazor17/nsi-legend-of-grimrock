import pygame
import math
from camera import *
pygame.init()
from Physique import Physique  
from Physique import projectile
from Physique import Cac

                
class monstre(Physique):
    def __init__(self, x, y, nom, pv, pvmax, attaque, distance, distance_attaque):
        super().__init__(x,y,40,40)
        self.position = pygame.math.Vector2(x,y)
        self.nom = nom
        self.pv = pv
        self.pvmax = pvmax
        self.attaque = attaque
        self.distance = distance 
        self.distance_attaque = distance_attaque
        self.attaque_dernier_temps = - 1000
         
        
class monstre_rodeur(monstre):
    def __init__(self, x, y, nom, pv, pvmax, attaque, distance, distance_attaque,speed):
        super().__init__(x, y, nom, pv, pvmax, attaque, distance, distance_attaque)
        self.waypoints = [self.position.copy(), self.position+(200,0), self.position+(200,200), self.position+(0,200)]  # patrouille ici
        self.waypoint_actuel = 0
        self.attaque_cooldown = 400
        self.speed =speed

    def deplacement(self,player,l,list_object):
            self.velocity.x = 0
            self.velocity.y = 0
            if self.pv > 0:
                dx = self.position.x - player.rect.centerx
                dy = self.position.y - player.rect.centery
                distance_reelle = math.sqrt(int(dx**2 + dy**2))
                if self.distance >= distance_reelle and player.pv > 0:
                    if distance_reelle == 0:
                        distance_reelle = 1  # pour éviter la division par zéro et le crash du jeu hein
                    if distance_reelle > 70:
                            # Déplacement normalisé : dx/distance_reelle donne la direction (entre -1 et 1) et on multiplie par la vitesse pour garder une vitesse constante quelle que soit la direction
                            self.velocity.x -= (dx / distance_reelle) * 2*self.speed/3  # normalisé
                       
                            self.velocity.y -= (dy / distance_reelle) * 2*self.speed/3  # normalisé

                else:  # ronde — on récupère le waypoint actuel
                    cible_x, cible_y = self.waypoints[self.waypoint_actuel]
                    distance_x = cible_x - self.position.x 
                    distance_y = cible_y - self.position.y 
                    distance_total = math.sqrt(distance_x**2 + distance_y**2)
                    if distance_total < 10 and distance_total > - 10 :
                        self.waypoint_actuel = (self.waypoint_actuel + 1) % len(self.waypoints)
                    else:
                        self.velocity.x += (distance_x / distance_total) * 2*self.speed/5  # normalisé 
                        self.velocity.y += (distance_y / distance_total) * 2*self.speed/5
            self.position.x += self.velocity.x
            self.rect.center = self.position
            self.collisions_x(l)  # faire en sorte que le système de collisions marche
            self.collisions_x(list_object)
            self.position.y += self.velocity.y
            self.rect.center = self.position
            self.collisions_y(l)  # faire en sorte que le système de collisions marche
            self.collisions_y(list_object)


class araignee(monstre_rodeur):
    def __init__(self, x, y):
        super().__init__(x, y, "araignee", 80, 80, 15, 200, 100, 8)
        self.cac = Cac(0, 0, 35, 35, 10, 100)
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 10
        self.a = None # variable

    def attaque_m(self,player,liste_equipe,list_object,list_ennemi):
        if self.pv > 0:
            dx = self.position.x - player.rect.centerx
            dy = self.position.y - player.rect.centery
            distance_reelle = math.sqrt(int(dx**2 + dy**2)) # avec le théoreme de Pythagore on calcule la distance entre le monstre et le joueur
            temps =  pygame.time.get_ticks()
            if distance_reelle <self.distance and temps - self.attaque_dernier_temps >= self.attaque_cooldown :
                        self.attaque_dernier_temps = temps
                        if temps - player.invincible_temps >= player.duree_invincibilite and player.pv > 0:  
                            self.cac.lancer(self.position,player)
            if self.cac.cac_actif and temps - self.attaque_dernier_temps <= 500:
                self.cac.collisions(player,list_ennemi,liste_equipe)            
            else:
                self.cac.cac_actif = False
                        

    def draw(self, screen, follow, player):
                if self.pv > 0:
                    pygame.draw.circle(screen, (0, 0, 255), follow.appliquer(self.position), 20)
                    if self.cac.cac_actif :
                        self.a = pygame.time.get_ticks()
                    if self.a is not None and player.pv > 0:
                        if self.a - self.attaque_dernier_temps< 150: 
                            pygame.draw.rect(screen, (255, 0, 0), (self.cac.cac_rect.x - follow.camera.offset.x, self.cac.cac_rect.y - follow.camera.offset.y, self.cac.cac_largeur,self.cac.cac_hauteur))

class ennemi1(monstre_rodeur):
    def __init__(self, x, y):
        super().__init__(x, y, "ennemi1", 100, 100, 10, 250, 130, 10)
        self.proj = projectile(x, y, 5, 8, 0, 0, 10,0) # initialisation du projectile (position(x,y)  vitesse , rayon, vitesse_x, vitesse_y, degat)
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 10
        self.dash_actif = False
        self.dash_debut = 0
        self.dash_duree = 350  # 3 secondes
        self.acceleration_dash = 40

    def draw(self, screen, follow, player):
                if self.pv > 0:
                    pygame.draw.circle(screen, (99, 69, 45), follow.appliquer(self.position), 20)

                if self.proj.proj_actif and self.pv > 0:
                    pygame.draw.circle(screen, (255, 165, 0), follow.appliquer(self.proj.position_proj), self.proj.proj_rayon)

    
    def attaque_m(self,player,liste_equipe,list_object,list_ennemi):
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
                    
            
                    
    
        

    def dash(self,player,liste_equipe,degat):
                if self.pv <= 0 :   #plus optimal que de faire un if à chaque fois dans les fonctions de déplacement et d'attaque, on sort directement de la fonction si le monstre est mort
                    return
                temps =  pygame.time.get_ticks() 
                
                dx = self.position.x - player.rect.centerx
                dy = self.position.y - player.rect.centery
                distance_reelle = math.sqrt(int(dx**2 + dy**2))
                if  player.pv > 0 and distance_reelle < 200 and temps - self.attaque_dernier_temps >= self.attaque_cooldown + 2000:

                    self.attaque_dernier_temps = temps
                    player.recevoir_degat(degat, liste_equipe)

                    self.dash_actif = True
                    print("dash activé")
                    self.dash_debut = temps
                    self.speed += self.acceleration_dash

                    # Fin du dash après 3 secondes
                if self.dash_actif:
                    if temps - self.dash_debut >= self.dash_duree:
                        self.speed -= self.acceleration_dash
                        self.dash_actif = False
                        print("dash désactivé")



def liste(list_ennemi):            # pour supprimer les ennemis morts de la liste des ennemis
                    list_ennemi[:] = [monstreee for monstreee in list_ennemi if monstreee.pv >0] # notation slice pour modifier la liste originale , pop l'index créait des bug car on manipule un index qui n'existe plus 
