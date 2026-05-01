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

    def collisions_x (self,list_object):
        for object in list_object:
            if self.rect.colliderect(object.rect):
                if self.velocity.x > 0: # collision à droite
                    self.rect.right = object.rect.left 
                    self.velocity.x = 0
                elif self.velocity.x < 0: # collision à gauche
                    self.rect.left = object.rect.right 
                    self.velocity.x = 0
                self.position.x = self.rect.centerx      

    def collisions_y(self,list_object):
        for object in list_object:
            if self.rect.colliderect(object.rect):
                if self.velocity.y > 0: # collision en bas
                            self.rect.bottom = object.rect.top 
                            self.velocity.y = 0
                elif self.velocity.y < 0: # collision en haut
                            self.rect.top = object.rect.bottom 
                            self.velocity.y = 0
                self.position.y = self.rect.centery
    
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


    def interaction (self,player,screen, font, follow, mon_inventaire,joueur_or,events):
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
                    cle= item("clé", 50, 50, 0, (255, 255, 0), "assets/cle.png")
                    self.ouvert = True
                    
                    self.image = self.image_originale
                    
                    mon_inventaire.ajouter(potion_vie) # Appelle la méthode sur l'instance car sinon appelle inventaire.ajouter sur la classe elle-même au lieu d'une instance de la classe.
                    mon_inventaire.ajouter(potion_degat)
                    mon_inventaire.ajouter(cle)
                    print (mon_inventaire.items[0].nom) 
        else:           
            self.image = self.image_originale
                        

class item(Object): # tout ce qui est dans l'inventaire
    def __init__(self, nom, height, width, effet, couleur=(255,255,255), Image=None):
        super().__init__(0, 0, width, height, couleur, Image)  
        self.nom = nom
        self.effet = effet
                    

    # potion_de_soin = item("potion de soin", 50)
    


                    
class projectile:                
        def __init__(self,x,y,proj_vitesse,proj_rayon,proj_vitesse_x,proj_vitesse_y,proj_degat,zone,sound_lancer=None,sound_toucher=None):
            self.position_proj = pygame.math.Vector2(x,y)
            self.proj_actif = False
            self.proj_vitesse = proj_vitesse
            self.proj_rayon = proj_rayon
            self.proj_vitesse_x = proj_vitesse_x
            self.proj_vitesse_y = proj_vitesse_y 
            self.proj_degat = proj_degat
            self.zone = zone
            self.temps_lancement = -100
            self.rect = pygame.Rect (x-proj_rayon, y-proj_rayon, proj_rayon*2, proj_rayon*2 ) # - proj rayon car le self.rect est inialisé au top left 
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
           
            distance = math.sqrt(ddx**2 + ddy**2)
            if distance == 0:  # <-- ajout
                return
            self.proj_vitesse_x = (ddx / distance) * self.proj_vitesse
            self.proj_vitesse_y = (ddy / distance) * self.proj_vitesse
            self.position_proj += (self.proj_vitesse_x, self.proj_vitesse_y)
            self.rect.x = self.position_proj.x - self.proj_rayon
            self.rect.y = self.position_proj.y - self.proj_rayon
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
                        print (cible.pv)

        def collisions_zone(self,list_ennemi,screen,follow):
            l = []
            if len(list_ennemi) != 0:
                for monstre in list_ennemi:
                    dx = monstre.position.x - self.position_proj.x
                    dy = monstre.position.y - self.position_proj.y
                    distance_reelle = math.sqrt(int(dx**2 + dy**2))
                    print (distance_reelle)
                    if monstre.rect.collidepoint(self.position_proj):
                        self.proj_actif = False
                        pygame.draw.circle(screen, (190, 65, 65), (follow.appliquer(self.position_proj) ), self.zone)
                        if distance_reelle <= self.zone:
                            l.append(monstre)

            if self.proj_actif is False:
                if len(list_ennemi) != 0:
                    for monstre in list_ennemi:
                        dx = monstre.position.x - self.position_proj.x
                        dy = monstre.position.y - self.position_proj.y
                        distance_reelle = math.sqrt(int(dx**2 + dy**2))
                        pygame.draw.circle(screen, (190, 65, 65), (follow.appliquer(self.position_proj) ), self.zone)
                        if distance_reelle <= self.zone:
                            l.append(monstre)

                        
            for i in range (len(l)):
                l[i].pv -=self.proj_degat 
                print (l[i].pv)
        
            
class Cac:
    def __init__(self,x,y,cac_hauteur,cac_largeur,cac_degat,zone,sound_lancer=None,sound_toucher=None):
        self.position_cac = pygame.math.Vector2(x,y)
        self.cac_actif = False
        self.cac_hauteur = cac_hauteur
        self.cac_largeur = cac_largeur
        self.cac_degat = cac_degat
        self.zone = zone
        self.cac_rect = None
        self.t = None
        self
        

    def lancer(self, origine, cible):
        self.cac_actif = True
        self.position_cac = origine.copy()
        
        dx = cible.position.x - origine.x
        dy = cible.position.y - origine.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance == 0:
            distance = 1
        dx /= distance  # normalise entre -1 et 1
        dy /= distance

        rect_x = origine.x + dx * self.cac_largeur - self.cac_largeur / 2
        rect_y = origine.y + dy * self.cac_hauteur - self.cac_hauteur / 2

        self.cac_rect = pygame.Rect(rect_x, rect_y, self.cac_largeur, self.cac_hauteur)

    def collisions(self,cible,list_ennemi,liste_equipe):
            if type(cible).__name__ == "Player":
                if cible.rect.colliderect(self.cac_rect) and self.cac_actif == True:
                    cible.recevoir_degat(self.cac_degat, liste_equipe)
                    self.cac_actif = False        
            else : 
                for monstre in list_ennemi :
                    if monstre.rect.colliderect(self.cac_rect):
                        monstre.pv -=self.cac_degat     
                        self.cac_actif = False
                        print (monstre.pv)
                        self.t = pygame.time.get_ticks()




class Mur(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (100, 80, 60), "assets/murr.png")
        self.image_originale = self.image
        self.position = pygame.math.Vector2(x, y)       

class porte(Object):             
    def __init__(self, x, y, nom, width, height, distance_interaction):
        super().__init__(x, y, width, height, (150, 75, 0), Image=None)  # sans nom
        self.nom = nom  # on garde le nom séparément
        self.image_originale = self.image
        self.position = pygame.math.Vector2(x, y) 
        self.ouvert = False
        self.distance_interaction = distance_interaction
        self.rect = pygame.Rect(x, y, width, height)
        self.e = False

class Porte_normale(porte):
    def __init__(self, x, y):
        super().__init__(x, y,"porte", 50, 100, 150)
        self.image_originale = self.image

    def interaction(self, player, screen, follow, list_object, mon_inventaire):
        if player.pv > 0:
            if self.ouvert is False:
                pass
            elif self.ouvert is True : # si la porte est ouverte
                self.e = True  # la variable self.e passa a True
                list_object[:] = [ objet for objet in list_object if not hasattr (objet, "e") or objet.e == False ] # on regarde si les objects dans list_object on un attribut "e" ou s'il est a False, on les garde 

    

class Porte_plaque(porte):
    def __init__(self, x, y, x_plaque, y_plaque, width_plaque, height_plaque):
        super().__init__(x, y, "porte_plaque", 50, 100, 150)  
        self.image_originale = self.image
        self.rect_plaque = pygame.Rect(x_plaque, y_plaque, width_plaque, height_plaque)
        self.plaque_appuyé = False 

    def interaction (self, player, screen, follow, list_object, mon_inventaire):
        if player.pv > 0:
            if player.rect.colliderect(self.rect_plaque) or item.colliderect(self.rect_plaque):
                self.plaque_appuyé = True
            else:
                self.plaque_appuyé = False
        self.ouvert = self.plaque_appuyé

class Porte_clé(porte):
    def __init__(self, x, y):
        super().__init__(x, y, "porte_cle", 50, 100, 150)
        self.image_originale = self.image
    def interaction(self, player, screen, follow, list_object, mon_inventaire):
         if player.pv > 0:
            if self.ouvert is False:
                pass
            elif self.ouvert is True : # si la porte est ouverte
                self.e = True  # la variable self.e passa a True
                list_object[:] = [ objet for objet in list_object if not hasattr (objet, "e") or objet.e == False ] # on regarde si les objects dans list_object on un attribut "e" ou s'il est a False, on les garde
