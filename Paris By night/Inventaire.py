import pygame
import math
from camera import *


pygame.init()

width = 1080
height = 720

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



boutons_menu = {
    "inventaire": pygame.Rect(50, 200, 150, 50),
    "equipe": pygame.Rect(50, 270, 150, 50),
    "stats": pygame.Rect(50, 340, 150, 50)
}
menu_actif = "inventaire"

def les_pieds_de_louis(screen, font, liste_equipe,mon_inventaire,image_invent):
            hpb_w = 600
            hpb_h = 300
            hpb_x = width/2 - hpb_w/2
            hpb_y = height/2 - hpb_h/2
            t2 = pygame.time.get_ticks() # réinitialisation du timer pour éviter les appuis rapides qui font bug le menu pause

            for nom_des_menus, rect in boutons_menu.items():
                couleur = (200, 170, 100) if menu_actif == nom_des_menus else (150, 120, 70)
                pygame.draw.rect(screen, couleur, rect)

                texte = font.render(nom_des_menus.capitalize(), True, (0, 0, 0))
                screen.blit(texte, (rect.x + 10, rect.y + 10))

            if menu_actif == "inventaire":
                screen.blit(image_invent, (hpb_x, hpb_y))
                mon_inventaire.draw(screen, liste_equipe)

            elif menu_actif == "equipe":
                pygame.draw.rect(screen, (180, 140, 80), (hpb_x, hpb_y, 600, 300))
                texte = font.render("Menu Équipe", True, (0, 0, 0))
                screen.blit(texte, (hpb_x + 200, hpb_y + 20))

            elif menu_actif == "stats":
                pygame.draw.rect(screen, (180, 140, 80), (hpb_x, hpb_y, 600, 300))
                texte = font.render("Statistiques", True, (0, 0, 0))
                screen.blit(texte, (hpb_x + 200, hpb_y + 20))



def changer_menu(pos_souris):
    global menu_actif
    for nom_du_menu, rect in boutons_menu.items():
        if rect.collidepoint(pos_souris):
            menu_actif = nom_du_menu
