import pygame
pygame.init()
from camera import *
from Physique import Physique
import math
import os
    
speed = 6

class Player(Physique):
        def __init__(self, x, y, radius=20,):
            super().__init__(x, y, radius*2, radius*2)
            self.radius = radius
            self.rect = pygame.Rect(x, y , radius * 2, radius * 2)
            self.pv = 100
            self.pvmax = 100
            self.invincible_temps =  - 1000
            self.duree_invincibilite = 2000
            self.position = pygame.math.Vector2(x,y)
            self.direction = pygame.math.Vector2(1,0) # initialisé vers la droite
            chemin = os.path.join(os.path.dirname(__file__), "assets/sprite_sheet_raven12.png")
            spritesheet = pygame.image.load(chemin).convert_alpha()
            self.frame_index = 0
            self.derniere_frame = 0
            self.direction_choisie = 0
            self.frames = []
            frame_width =964 // 8
            frame_height = 596//4

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


                

        def recevoir_degat(self, degat, liste_equipe):
            for elem in liste_equipe:
                if elem.pv > 0 :
                     elem.pv -= degat
                     break
            if all(elem.pv <=0 for elem in liste_equipe):
                self.pv = 0
        

        def mouvement(self,touches):
            self.velocity = pygame.math.Vector2(0, 0)
            if self.pv > 0:
                if touches[pygame.K_z] or touches[pygame.K_UP]:
                    if (touches[pygame.K_d] or touches[pygame.K_RIGHT]) ^ (touches[pygame.K_q] or touches[pygame.K_LEFT]): # ^ = ou exclusif (xor)
                        self.velocity.y = - speed / math.sqrt(2)
                    else:
                        self.velocity.y = - speed
                if touches[pygame.K_s] or touches[pygame.K_DOWN]:
                    if (touches[pygame.K_d] or touches[pygame.K_RIGHT]) ^ (touches[pygame.K_q] or touches[pygame.K_LEFT]):
                        self.velocity.y = speed / math.sqrt(2)
                    else:
                        self.velocity.y = speed
                if touches[pygame.K_q] or touches[pygame.K_LEFT]:
                    if (touches[pygame.K_z] or touches[pygame.K_UP]) ^ (touches[pygame.K_s] or touches[pygame.K_DOWN]):
                        self.velocity.x = -speed / math.sqrt(2)
                    else:
                        self.velocity.x = -speed
                if touches[pygame.K_d] or touches[pygame.K_RIGHT]:
                    if (touches[pygame.K_z] or touches[pygame.K_UP]) ^ (touches[pygame.K_s] or touches[pygame.K_DOWN]):
                        self.velocity.x= speed / math.sqrt(2)
                    else:
                        self.velocity.x = speed
            if self.velocity.length() > 0:
                    self.direction = self.velocity.normalize()
            return self.velocity.x, self.velocity.y

        def draw(self, screen, follow):
            if self.pv > 0:
                if self.pv > 0:
                    dx = self.direction.x
                    dy = self.direction.y
                    seuil = 0.4

                    if dx > seuil and dy > seuil:
                        colonne = 1  # bien placé
                    elif dx < -seuil and dy > seuil:
                        colonne = 7    # bien placé
                    elif dx < -seuil and dy < -seuil:
                        colonne = 3  # bien placé
                    elif dx > seuil and dy < -seuil:
                        colonne = 5  # bien placé
                    elif dy > seuil:
                        colonne = 0 # bien placé
                    elif dy < -seuil:
                        colonne = 4 # bien placé
                    elif dx < -seuil:
                        colonne = 2 # bien placé
                    elif dx > seuil:
                        colonne = 6 # bien placé
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
