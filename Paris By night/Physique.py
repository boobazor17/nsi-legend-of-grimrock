import pygame 
import os  
import math
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
        

    def ajouter(self, nouvel_item):
        self.items.append(nouvel_item)
        

    def draw(self, screen):

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
                
                    
    def utiliser(self, pos_souris, player):
        for i in range(4):
            for j in range(4):
                index = i * 4 + j #  permet de calculer l'index de l'item dans la liste à partir de sa position dans la grille (i, j)
                case_x = 590 + j * 45
                case_y = 280 + i * 45
                case_rect = pygame.Rect(case_x, case_y, 42, 42)
                if case_rect.collidepoint(pos_souris): # vérifie si la position de la souris est dans la case cliquée
                    if index < len(self.items): #vérifie s'il Quand Python sort du for j, case_x garde la dernière valeur calculée soit j=3. C'est pour ça que l'image apparaît toujours à droite.
                        item_utilise = self.items[index]
                        player.pv += item_utilise.effet
                        if player.pv > player.pvmax:
                            player.pv = player.pvmax
                        self.items.pop(index)  
                        return  
                    
                    
        
