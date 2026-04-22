import pygame
import os
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
                self.attaque = attaque
                if Image: # s'il y a une image
                    chemin = os.path.join(os.path.dirname(__file__), Image) #os.path.dirname(__file__) récupère le dossier où se trouve physique.py, puis os.path.join colle le chemin de l'image dessus
                    self.image = pygame.image.load(chemin).convert_alpha()
                    self.image = pygame.transform.scale(self.image, (100, 100))
    
    
    def ajouter_attaque(self, attaque):
        self.attaque.utiliser(attaque)

    

class attaque:
    def __init__(self,nom,degat,portée,rayon,ralentissement,temps_recharge, ): 
        self.nom = nom
        self.degat = degat
        self.portée= portée
        self.rayon= rayon
        self.ralentissement= ralentissement
        self.temps_recharge= temps_recharge
    
    
    def utiliser(self, attaquant):
        '''ici on vérifierait la distance entre l'attaquant et la cible, et si elle est 
        inférieure ou égale à la portée de l'attaque, on infligerait les dégâts à la cible 
        plus les effets eventuels (ralentissement, etc.)'''
        pass












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
