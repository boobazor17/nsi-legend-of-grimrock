import pygame 
import os  
import math
from camera import *
pygame.init()
font = pygame.font.Font(None,40)

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
    
    
class Vase(Object): # tout ce qui est physique
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, (255, 0, 0),"assets/vase.png")
        self.image_originale = self.image
        self.position = pygame.math.Vector2(x,y)
        self.distance = 200
        self.ouvert = False


    def interaction (self,player,screen, font, follow, mon_inventaire):
        dx = self.position.x - player.rect.centerx
        dy = self.position.y - player.rect.centery
        distance_reelle = math.sqrt(int(dx**2 + dy**2))
        texte_x =  int(self.position.x - follow.camera.offset.x) 
        texte_y =  int(self.position.y - follow.camera.offset.y) - 50
        texte = font.render("E", True, (255, 255, 255))
        if self.distance >= distance_reelle and not self.ouvert:
            pygame.draw.circle(screen,("gold"), (texte_x+10, texte_y+10), 20) # cercle doré autour du E pour indiquer que le joueur peut interagir avec le vase
            screen.blit(texte, (texte_x, texte_y))
            u = pygame.time.get_ticks()
            self.width = 50 +  math.sin(u/200) * 2.5
            self.height = 50 +  math.sin(u/200) * 2.5
            self.image = pygame.transform.scale(self.image_originale, (int(self.width), int(self.height)))
            touches = pygame.key.get_pressed()
            if touches[pygame.K_e]:
                    potion_vie = item("potion de soin", 50, 50, 20, (255, 0, 255), "assets/potion_vie.png")
                    potion_degat = item("potion de dégats", 50, 50, -20, (255, 0, 255), "assets/potion_degat.png")
                    self.ouvert = True
                    
                    self.image = self.image_originale
                    
                    mon_inventaire.ajouter(potion_vie) # Appelle la méthode sur l'instance car sinon appelle inventaire.ajouter sur la classe elle-même au lieu d'une instance de la classe.
                    mon_inventaire.ajouter(potion_degat)
                    print (mon_inventaire.items[0].nom) 
        else:           
            self.image = self.image_originale
                        

class item(Object): # tout ce qui est dans l'inventaire
    def __init__(self, nom, height, width, effet, couleur=(255,255,255), Image=None):
        super().__init__(0, 0, width, height, couleur, Image)  
        self.nom = nom
        self.effet = effet
                    

    # potion_de_soin = item("potion de soin", 50)
    

class inventaire:
    def __init__(self):
        self.items = []
        self.item_utilise = None
        self.perso_choisi = None
        self.index = None
        self.x=None
        self.y = None

    def ajouter(self, nouvel_item):
        self.items.append(nouvel_item)
        

    def draw(self, screen,liste_equipe):

        # affiche les 16 cases même vides
        for i in range(4):
            for j in range(4):
                index = i * 4 + j
                case_x = 590 + j * 45  # j pour les colonnes, i pour les lignes
                case_y = 280 + i * 45
                pygame.draw.rect(screen, (100, 80, 60), (case_x, case_y, 42, 42))
                pygame.draw.rect(screen, (60, 40, 20), (case_x, case_y, 42, 42), 2)  # bordure

            # mettre dans le même bloc à la suite car Quand Python sort du for j, case_x gardait la dernière valeur calculée soit j=3. C'est pour ça que l'image apparaîssait toujours à droite.
                if index < len(self.items):
                    image = self.items[index].image
                    screen.blit(image, (case_x, case_y))

        for i in range(len(liste_equipe)):
            case_xx = 270 
            case_jj = 240 + i*55
            image = liste_equipe[i].image
            screen.blit(image, (case_xx, case_jj))
            
        if self.index is not None:
            overlay = pygame.Surface((50, 50))
            overlay.set_alpha(100)  # 0 = invisible, 255 = opaque
            overlay.fill((50, 50, 50))  
            screen.blit(overlay, (self.x, self.y+10))
                    
    def utiliser(self, pos_souris,liste_equipe):
        if self.item_utilise is None:
                    for i in range(4):
                        for j in range(4):
                            index = i * 4 + j #  permet de calculer l'index de l'item dans la liste à partir de sa position dans la grille (i, j)
                            case_x = 590 + j * 45
                            case_y = 270 + i * 45
                            case_rect = pygame.Rect(case_x, case_y, 42, 42)
                            if case_rect.collidepoint(pos_souris): # vérifie si la position de la souris est dans la case cliquée
                                    if index < len(self.items): #vérifie s'il Quand Python sort du for j, case_x garde la dernière valeur calculée soit j=3. C'est pour ça que l'image apparaît toujours à droite.
                                        self.item_utilise = self.items[index]
                                        self.index = index
                                        self.x= case_x
                                        self.y = case_y

        else:
                    for elem in range(len(liste_equipe)):
                        case_xx = 270 
                        case_jj = 240 + elem*55
                        elem_rect= pygame.Rect(case_xx, case_jj, 100, 100)
                        if elem_rect.collidepoint(pos_souris):
                            self.perso_choisi = liste_equipe[elem]                 
        if self.perso_choisi and self.item_utilise:
            self.perso_choisi.pv += self.item_utilise.effet
            if self.perso_choisi.pv > self.perso_choisi.pvmax:
                self.perso_choisi.pv = self.perso_choisi.pvmax
            self.items.pop(self.index) 
            self.perso_choisi = None   
            self.item_utilise = None
            self.index = None
            self.c = None
            self.t = None
                    
class projectile:                
        def __init__(self,x,y,proj_vitesse,proj_rayon,proj_vitesse_x,proj_vitesse_y,proj_degat,sound_lancer=None,sound_toucher=None):
            self.position_proj = pygame.math.Vector2(x,y)
            self.proj_actif = False
            self.proj_vitesse = proj_vitesse
            self.proj_rayon = proj_rayon
            self.proj_vitesse_x = proj_vitesse_x
            self.proj_vitesse_y = proj_vitesse_y 
            self.proj_degat = proj_degat
            self.temps_lancement = -100
            try:
                self.sound_lancer = pygame.mixer.Sound("assets/sounds/rocksane.mp3")
                self.sound_lancer.set_volume(0.5)  # Volume entre 0.0 et 1.0
            except Exception as e:
                self.sound_lancer = None
             
        def lancer(self,origine,cible):
            self.proj_actif = True
            self.position_proj = origine.copy()
            if hasattr(cible, 'rect'):
                ddx = cible.rect.centerx - self.position_proj.x
                ddy = cible.rect.centery - self.position_proj.y
            else:
                ddx = cible.position.x - self.position_proj.x
                ddy = cible.position.y - self.position_proj.y
           
            dist = math.sqrt(ddx**2 + ddy**2)
            self.proj_vitesse_x = (ddx / dist) * self.proj_vitesse
            self.proj_vitesse_y = (ddy / dist) * self.proj_vitesse
            self.position_proj += (self.proj_vitesse_x, self.proj_vitesse_y)
            if self.sound_lancer is not None:
                self.sound_lancer.play()

        def collisions(self,cible,liste_equipe):    
            if self.proj_actif == True:
                if type(cible).__name__ == "Player":
                    if cible.rect.collidepoint(self.position_proj):
                        cible.recevoir_degat(self.proj_degat, liste_equipe)
                        self.proj_actif = False
                else:
                    if cible.rect.collidepoint(self.position_proj):
                        cible.pv -=self.proj_degat     
                        self.proj_actif = False

class mur(Object):
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height,(100, 80, 60),Image=None)
        self.image_originale = self.image
        self.position = pygame.math.Vector2(x,y)                    

               

