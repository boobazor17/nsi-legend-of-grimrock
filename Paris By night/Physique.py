import pygame 
import os  
import math
pygame.init()

class Physique:
    def __init__(self,x,y,width,height,):
        self.position = pygame.math.Vector2(x,y)
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = pygame.math.Vector2(0,0)

    def collisions (self,list_object):
        for object in list_object:
            if self.rect.colliderect(object.rect):
                if self.velocity.x > 0: # collision à droite
                    self.rect.right = object.rect.left
                if self.velocity.x < 0: # collision à gauche
                    self.rect.left = object.rect.right
                if self.velocity.y > 0: # collision en bas
                    self.rect.bottom = object.rect.top
                if self.velocity.y < 0: # collision en haut
                    self.rect.top = object.rect.bottom

            self.position = self.rect.center


class Object:
    def __init__(self,x,y,width,height,couleur,Image=None):
        self.rect = pygame.Rect(x, y, width,height)
        self.position = pygame.math.Vector2(x,y)  
        self.couleur = couleur
        if Image: # s'il y a une image
            chemin = os.path.join(os.path.dirname(__file__), Image) #os.path.dirname(__file__) récupère le dossier où se trouve physique.py, puis os.path.join colle le chemin de l'image dessus
            self.image = pygame.image.load(chemin).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        else: # tant que une image n'est pas importée
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            self.image.fill(couleur)
    
    
class Vase(Object):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, (255, 0, 0), "assets/vase.png")
        self.position = pygame.math.Vector2(x,y)
        self.distance = 1000
        self.ouvert = False
        

    def interaction (self,player):
        l =[]

        dx = self.position.x - player.rect.centerx
        dy = self.position.y - player.rect.centery
        distance_reelle = math.sqrt(int(dx**2 + dy**2))
        if self.distance >= distance_reelle and not self.ouvert:
            
            touches = pygame.key.get_pressed()
            if touches[pygame.K_e]:
                    self.ouvert = True
                    l.append("potion de soin")
                    print(l)
                        


    

        