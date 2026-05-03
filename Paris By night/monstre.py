import pygame
import math
from camera import *
pygame.init()
from Physique import Physique
from Physique import projectile
from Physique import Cac
import os
from random import randint

                
class monstre(Physique):
    def __init__(self, x, y, nom, pv, pvmax, attaque, distance, distance_attaque, attaque_cooldown, speed):
        super().__init__(x,y,40,40)
        self.position = pygame.math.Vector2(x,y)
        self.direction = pygame.math.Vector2(0, 0)
        self.nom = nom
        self.pv = pv
        self.pvmax = pvmax
        self.attaque = attaque
        self.distance = distance 
        self.distance_attaque = distance_attaque
        self.attaque_dernier_temps = - 1000
        self.has_ronde = False
        self.attaque_cooldown = attaque_cooldown
        self.speed = speed

    def deplacement(self,player,l,list_object):
            self.velocity.x = 0
            self.velocity.y = 0
            self.direction = self.velocity
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

                if self.has_ronde :  # ronde — on récupère le waypoint actuel
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
            if self.velocity.length() > 0:
                self.direction = self.velocity.normalize()

        
class monstre_summoner(monstre):
    def __init__(self, x, y, nom, pv, pvmax, attaque, distance, distance_attaque, attaque_cooldown, speed, summon_max, summon_cooldown,ligne,colonne, classe, Image= None ):
        super().__init__(x, y, nom, pv, pvmax, attaque, distance, distance_attaque, attaque_cooldown, speed)
        self.speed =speed
        self.summon_cooldown = summon_cooldown  # 5 secondes
        self.summon_dernier_temps = -1000
        self.summon_number = []
        self.summon_max = summon_max
        self.ligne = ligne
        self.colonne = colonne
        self.classe = classe

    

    def summon(self, classe, list_ennemi):
        ennemi = classe(self.position.x + randint(-50,50),self.position.y + randint(-50,50))
        ennemi.rect.center = ennemi.position
        self.summon_number.append(ennemi)
        list_ennemi.append(ennemi)

    def draw(self, screen, follow, player):
        pass

         

    def attaque_m(self, player, liste_equipe, list_object, list_ennemi, classe):
        if self.pv > 0:
            dx = self.position.x - player.rect.centerx
            dy = self.position.y - player.rect.centery
            distance_reelle = math.sqrt(int(dx**2 + dy**2))
            temps =  pygame.time.get_ticks()
            if  distance_reelle <= self.distance_attaque and player.pv > 0:
                if len(self.summon_number) < self.summon_max and temps - self.summon_dernier_temps >= self.summon_cooldown:
                    self.summon_dernier_temps = temps
                    self.summon(classe, list_ennemi)

class bat_summoner(monstre_summoner):
    def __init__(self, x, y):
        super().__init__(x, y, "necromancien", 100, 100, 0, 300, 200, 500, 4, 4, 5000, 4, 4, bat, Image= None )

class bat(monstre):
    def __init__(self, x, y):
        super().__init__(x, y, "bat", 30, 30, 10, 100, 70, 500, 8 )
        self.summon_dernier_temps = -1000
        self.cac = Cac(0, 0, 20, 20, 10, 50) 
        self.direction_choisie = 0

    def attaque_m(self, player, liste_equipe, list_object, list_ennemi, classe):
        if self.pv > 0:
            dx = self.position.x - player.rect.centerx
            dy = self.position.y - player.rect.centery
            distance_reelle = math.sqrt(int(dx**2 + dy**2)) # avec le théoreme de Pythagore on calcule la distance entre le monstre et le joueur
            temps =  pygame.time.get_ticks()
            if distance_reelle <self.distance_attaque and temps - self.attaque_dernier_temps >= self.attaque_cooldown :
                        self.attaque_dernier_temps = temps
                        if temps - player.invincible_temps >= player.duree_invincibilite and player.pv > 0:  
                            self.cac.lancer(self.position,player)
                            self.animation_cac_active = True
                            self.animation_cac_debut = pygame.time.get_ticks()
                            self.direction_attaque = self.direction_choisie
            if self.cac.cac_actif and temps - self.attaque_dernier_temps <= 500:
                self.cac.collisions(player,list_ennemi,liste_equipe)            
            else:
                self.cac.cac_actif = False

    def draw(self, screen, follow, player):
        if self.pv > 0:
            pygame.draw.circle(screen, (128, 0, 128), follow.appliquer(self.position), 15)
     

class monstre_rodeur(monstre):
    def __init__(self, x, y, nom, pv, pvmax, attaque, distance, distance_attaque, attaque_cooldown, speed):
        super().__init__(x, y, nom, pv, pvmax, attaque, distance, distance_attaque, attaque_cooldown, speed)
        self.waypoints = [self.position.copy(), self.position+(200,0), self.position+(200,200), self.position+(0,200)]  # patrouille ici
        self.waypoint_actuel = 0
        self.speed =speed
        self.has_ronde = True
        self.attaque_cooldown = attaque_cooldown



class araignee(monstre_rodeur):
    def __init__(self, x, y):
        super().__init__(x, y, "araignee", 80, 80, 15, 200, 100, 700, 6)
        self.cac = Cac(0, 0, 35, 35, 10, 100)
        self.rect = pygame.Rect(x, y, 40, 40)
        self.a = None # variable
        chemin = os.path.join(os.path.dirname(__file__), "assets/araignee_spritesheet.png")
        spritesheet = pygame.image.load(chemin).convert_alpha()
        chemin = os.path.join(os.path.dirname(__file__), "assets/aa.png")
        attaque_sheet = pygame.image.load(chemin).convert_alpha()

        self.frames = []
        frame_width = 110
        frame_height = 70

        for ligne in range(4): # on a 4 lignes d'animation dans la spritesheet
            ligne_frames = []
            for colonne in range(8): # on a 8 colonnes d'animation dans la spritesheet
                frame = spritesheet.subsurface(
                    pygame.Rect(
                        colonne * frame_width,
                        ligne * frame_height,
                        frame_width,
                        frame_height
                    )
                )
                ligne_frames.append(frame)
            self.frames.append(ligne_frames)

        self.frame_index = 0
        self.derniere_frame = 0
        self.direction_choisie = 0

        # Si le fond noir n'est pas transparent :
        attaque_sheet.set_colorkey((0, 0, 0))

        self.frames_attaque = []

        colonnes_attaque = 5
        lignes_attaque = 8
        frame_w = attaque_sheet.get_width() // colonnes_attaque
        frame_h = attaque_sheet.get_height() // lignes_attaque

        for ligne in range(lignes_attaque):
            ligne_frames = []
            for colonne in range(colonnes_attaque):
                frame = attaque_sheet.subsurface(
                    pygame.Rect(
                        colonne * frame_w,
                        ligne * frame_h,
                        frame_w,
                        frame_h
                    )
                )
                ligne_frames.append(frame)
            self.frames_attaque.append(ligne_frames)
        self.animation_cac_active = False
        self.animation_cac_debut = 0
        self.direction_attaque = 0



    def attaque_m(self,player,liste_equipe,list_object,list_ennemi, classe):
        if self.pv > 0:
            dx = self.position.x - player.rect.centerx
            dy = self.position.y - player.rect.centery
            distance_reelle = math.sqrt(int(dx**2 + dy**2)) # avec le théoreme de Pythagore on calcule la distance entre le monstre et le joueur
            temps =  pygame.time.get_ticks()
            if distance_reelle <self.distance_attaque and temps - self.attaque_dernier_temps >= self.attaque_cooldown :
                        self.attaque_dernier_temps = temps
                        if temps - player.invincible_temps >= player.duree_invincibilite and player.pv > 0:  
                            self.cac.lancer(self.position,player)
                            self.animation_cac_active = True
                            self.animation_cac_debut = pygame.time.get_ticks()
                            self.direction_attaque = self.direction_choisie
            if self.cac.cac_actif and temps - self.attaque_dernier_temps <= 500:
                self.cac.collisions(player,list_ennemi,liste_equipe)            
            else:
                self.cac.cac_actif = False
                        

    def draw(self, screen, follow, player):
                if self.pv > 0:
                    dx = self.direction.x
                    dy = self.direction.y
                    seuil = 0.4

                    if dx > seuil and dy > seuil:
                        colonne = 4
                    elif dx < -seuil and dy > seuil:
                        colonne = 5
                    elif dx < -seuil and dy < -seuil:
                        colonne = 6
                    elif dx > seuil and dy < -seuil:
                        colonne = 7
                    elif dy > seuil:
                        colonne = 0
                    elif dy < -seuil:
                        colonne = 1
                    elif dx < -seuil:
                        colonne = 3
                    elif dx > seuil:
                        colonne = 2
                    else:
                        colonne = self.direction_choisie

                    # 1. choisir direction_choisie
                    self.direction_choisie = colonne

                    # 2. avancer l’animation
                    temps = pygame.time.get_ticks()
                    if self.velocity.length() > 0:
                        if temps - self.derniere_frame > 120:
                            self.frame_index = (self.frame_index + 1) % 4
                            self.derniere_frame = temps

                    # 3. choisir une seule image
                    image = self.frames[self.frame_index][self.direction_choisie]

                    # 4. afficher
                    pos = follow.appliquer(self.position)
                    x = pos[0] - image.get_width() // 2
                    y = pos[1] - image.get_height() // 2
                    screen.blit(image, (x, y))

                    if self.animation_cac_active and self.cac.cac_rect is not None and player.pv > 0:
                        temps_attaque = pygame.time.get_ticks() - self.animation_cac_debut
                        frame_attaque = temps_attaque // 60

                        if frame_attaque < 5:
                            correspondance_attaque = {
                                0: 2,  # bas
                                1: 6,  # haut
                                2: 0,
                                3: 4,
                                4: 7,
                                5: 5,
                                6: 3,
                                7: 1,
                            }


                            ligne_attaque = correspondance_attaque[self.direction_attaque]
                            image_attaque = self.frames_attaque[ligne_attaque][frame_attaque]

                            x = self.cac.cac_rect.centerx - follow.camera.offset.x - image_attaque.get_width() // 2
                            y = self.cac.cac_rect.centery - follow.camera.offset.y - image_attaque.get_height() // 2

                            screen.blit(image_attaque, (x, y))
                        else:
                            self.animation_cac_active = False


class ennemi1(monstre_rodeur):
    def __init__(self, x, y):
        super().__init__(x, y, "ennemi1", 100, 100, 10, 250, 130, 600, 10)
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

    
    def attaque_m(self, player, liste_equipe, list_object, list_ennemi, classe):
            if self.pv > 0:
                dx = self.position.x - player.rect.centerx
                dy = self.position.y - player.rect.centery
                distance_reelle = math.sqrt(int(dx**2 + dy**2)) # avec le théoreme de Pythagore on calcule la distance entre le monstre et le joueur
                temps =  pygame.time.get_ticks()
                if self.distance_attaque >= distance_reelle and temps - self.attaque_dernier_temps >= self.attaque_cooldown :
                    self.attaque_dernier_temps = temps
                    if temps - player.invincible_temps >= player.duree_invincibilite and player.pv > 0:  
                        self.proj.lancer(self.position,player)
                if self.proj.proj_actif and temps - self.attaque_dernier_temps <= 1500:
                    self.proj.position_proj += (self.proj.proj_vitesse_x, self.proj.proj_vitesse_y)
                    self.proj.rect.x = self.proj.position_proj.x - self.proj.proj_rayon
                    self.proj.rect.y = self.proj.position_proj.y - self.proj.proj_rayon
                    self.proj.collisions(player,liste_equipe) 
                    for object in list_object: # check tous les objets de la liste pour voir s'il y a une collision avec le projectile
                        if object.rect.colliderect(self.proj.rect):    
                                self.proj.proj_actif = False           
                else:
                    self.proj.proj_actif = False # on detruit le projectile , on met le else après le deuxième bloc if car si la condition est False donc tout le bloc est ignoré, y compris le proj_actif = False. Le projectile reste donc actif indéfiniment. :(
                    
            
                    
    
        

    def dash(self, player, liste_equipe, degat):
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
