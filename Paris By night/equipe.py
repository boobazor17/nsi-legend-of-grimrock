import pygame
import os
import math
from Physique import projectile
from Physique import Cac
pygame.init()
width = 1080
height = 720

class equipe :
    def __init__(self,x,y,nom,pv,pvmax,degat_attaque,distance_attaque,attaque,Image=None):
                self.position = pygame.math.Vector2(x,y)
                self.nom = nom
                self.pv = pv
                self.pvmax = pvmax
                self.degat_attaque = degat_attaque
                self.distance_attaque = distance_attaque
                self.attaque = None 
                if Image: # s'il y a une image
                    chemin = os.path.join(os.path.dirname(__file__), Image) #os.path.dirname(__file__) récupère le dossier où se trouve physique.py, puis os.path.join colle le chemin de l'image dessus
                    self.image = pygame.image.load(chemin).convert_alpha()
                    self.image = pygame.transform.scale(self.image, (100, 100))
    
    
    def ajouter_attaque(self, attaque):
        self.attaque = attaque

    

class attaque:
    def __init__(self,nom,degat,portée,rayon,ralentissement,temps_recharge): 
        self.nom = nom
        self.degat = degat
        self.portée= portée
        self.rayon= rayon
        self.ralentissement= ralentissement
        self.temps_recharge= temps_recharge
        self.attaque_dernier_temps = -1000
        self.proj = projectile(0, 0, 2, 8, 0, 0, 10,200) # (x,y) = (0,0)
        self.monstre = None                           
        self.case_rect = None     
        self.cac = Cac(0, 0, 50, 50, 10, 100)
    
    def utiliser(self, attaquant,list_ennemi,player,list_object,liste_equipe,case_rect):
        l =[]
        if len(list_ennemi) != 0:
            for monstre in list_ennemi:
                dx = monstre.position.x - player.rect.centerx
                dy = monstre.position.y - player.rect.centery
                distance_reelle = math.sqrt(int(dx**2 + dy**2))
                l.append((distance_reelle, monstre))
            l.sort()  #trie par distance
            monstre = l[0][1] # on récupère le monstre
            self.monstre =  monstre
            temps =  pygame.time.get_ticks() 
            if self.nom == "cac":
                print("attaque cac")
                if l[0][0] <= self.portée and temps - self.attaque_dernier_temps >= self.temps_recharge :
                    self.attaque_dernier_temps = temps
                    if attaquant.pv >= 0:
                        self.cac.lancer(pygame.math.Vector2(player.position))
                        self.case_rect = case_rect

            elif self.nom == "distance":
                if l[0][0] <= self.portée and temps - self.attaque_dernier_temps >= self.temps_recharge :
                        self.attaque_dernier_temps = temps
                        if attaquant.pv >= 0: 
                            self.proj.lancer(pygame.math.Vector2(player.position),monstre)
                            self.case_rect = case_rect
            elif self.nom == "mage" :
                if l[0][0] <= self.portée and temps - self.attaque_dernier_temps >= self.temps_recharge :
                        self.attaque_dernier_temps = temps
                        if attaquant.pv >= 0: 
                            self.proj.lancer(pygame.math.Vector2(player.position), monstre)
                            self.case_rect = case_rect



    def update(self, liste_equipe,list_object,temps,screen,list_ennemi,follow):
            if self.nom == "distance" or self.nom == "mage":
                if self.proj.proj_actif:
                    if self.monstre is not None :
                        if temps - self.attaque_dernier_temps <= 1500:
                                self.proj.position_proj += (self.proj.proj_vitesse_x, self.proj.proj_vitesse_y)
                                self.proj.collisions(self.monstre,liste_equipe)
                                if self.nom == "mage":
                                   self.proj.collisions_zone(list_ennemi,screen,follow)
                                overlay = pygame.Surface((100, 100))
                                overlay.set_alpha(100)  # 0 = invisible, 255 = opaque
                                overlay.fill((50, 50, 50))  
                                screen.blit(overlay, (self.case_rect.x, self.case_rect.y))          
                        else:
                                self.proj.proj_actif = False 
                                self.proj.collisions_zone(list_ennemi,screen,follow)
                    for object in list_object: # check tous les objets de la liste pour voir s'il y a une collision avec le projectile
                        if object.rect.collidepoint(self.proj.position_proj):    
                                    self.proj.proj_actif = False       
                if temps - self.attaque_dernier_temps <= 1500: 
                    overlay = pygame.Surface((100, 100))
                    overlay.set_alpha(100)  # 0 = invisible, 255 = opaque
                    overlay.fill((50, 50, 50))  
                    screen.blit(overlay, (self.case_rect.x, self.case_rect.y))   
            elif self.nom == "cac":
                if self.cac.cac_actif:
                    print(self.cac.cac_actif)
                    if self.monstre is not None:
                        if temps - self.attaque_dernier_temps <= 500:
                            self.cac.collisions(self.monstre,list_ennemi,liste_equipe)
                            overlay = pygame.Surface((100, 100))
                            overlay.set_alpha(100)  # 0 = invisible, 255 = opaque
                            overlay.fill((50, 50, 50))  
                            screen.blit(overlay, (self.case_rect.x, self.case_rect.y))          
                        else : 
                            self.cac.cac_actif = False


                           

    def draw_proj(self,screen,follow):
        if  self.proj.proj_actif:
            pygame.draw.circle(screen, (255, 0, 0), follow.appliquer(self.proj.position_proj), self.proj.proj_rayon)
        if self.cac.cac_actif :
            x, y = follow.appliquer(self.cac.position_cac) #on récupère les coordonnées écran de la position du cac en appliquant l'offset de caméra
            pygame.draw.rect(screen, (255, 0, 0), (x, y, self.cac.cac_largeur, self.cac.cac_hauteur)) #on dessine le rectangle de l'attaque corps à corps en rouge pour le visualiser
   
            #on fait ça en 2 lignes pour éviter un problème de tuple.
   
   
   
    """ def personnage():
     for i in range(4):  # pour des équipes de 4
        print("Choisis un personnage :")
        
        for index, perso in enumerate():
            print(index, "-", perso["nom"])     #choisir le perso avec son nom et un chiffre l'index
        
        choix = int(input("Numéro du personnage : ")) #rentrer le numéro donc l'index
        
        equipe.append([choix])

    print("Ton équipe est composée de :")
    for perso in equipe:
        print(perso["nom"], "-", perso["pv"], "PV") #affiche les infos du perso

    if [choix] not in equipe:  #pour éviter que un personnage soit choisi plusieurs fois par erreur
        equipe.append([choix])
    else:
        print("Déjà choisi !") """                

def regarde_clique(pos_souris,liste_equipe,list_ennemi,player,list_object):
        hpb_w = 1/5 * width
        hpb_h = 1/5* width
        hpb_x = width - hpb_w -20 
        hpb_y = height - hpb_h -20
        for i in range(2):
                for j in range(2):
                    index = i*2 + j
                    case_x = hpb_x + j * 100 + 10  # j pour les colonnes, i pour les lignes
                    case_y = hpb_y + i * 100 + 10
                    case_rect = pygame.Rect(case_x, case_y, 100, 100)
                    if case_rect.collidepoint(pos_souris):
                        attaquant = liste_equipe[index]
                        if attaquant.pv > 0:
                            attaquant.attaque.utiliser(attaquant,list_ennemi,player,list_object,liste_equipe,case_rect)



    
def changer_equipe(self,taille_equipe,liste_ts,liste_equipe):
            pass

def afficher_equipe(liste_equipe,screen):
            hpb_w = 1/5 * width
            hpb_h = 1/5* width
            hpb_x = width - hpb_w -20 
            hpb_y = height - hpb_h -20
            barre_perso = pygame.Rect(hpb_x, hpb_y, hpb_w, hpb_h)
            pygame.draw.rect(screen, (59, 55, 55), barre_perso )
            for i in range(2):
                for j in range(2):
                    index = i * 2 + j
                    case_x = hpb_x + j * 100 + 10  # j pour les colonnes, i pour les lignes
                    case_y = hpb_y + i * 100 + 10
                    pygame.draw.rect(screen, (100, 80, 60), (case_x, case_y, 100,100))
                    pygame.draw.rect(screen, (60, 40, 20), (case_x, case_y, 100,100), 2)  # bordure
                    if index < len(liste_equipe):
                        image = liste_equipe[index].image
                        screen.blit(image, (case_x, case_y-20))


def afficher_pv (liste_equipe,screen):
    for i in range(2):
        for j in range(2):
            hpb_x = 4/5 *width 
            hpb_y = 2/5* width + 40
            index = i * 2 + j
            case_x = hpb_x + j * 100 + 10  # j pour les colonnes, i pour les lignes
            case_y = hpb_y + i * 100 + 100 
            if index < len(liste_equipe):
                pv = liste_equipe[index].pv
                pvmax = liste_equipe[index].pvmax
                pygame.draw.rect(screen, (0, 0, 0), ((case_x-5), case_y, 70, 10)) 
                if pv > 0:
                    pygame.draw.rect(screen, (200, 0, 0), ((case_x-5), case_y, 70 * (pv/pvmax),10))  # bordure
