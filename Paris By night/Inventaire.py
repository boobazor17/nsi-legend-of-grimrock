import os
import pygame
import math
from camera import *
import equipe 


pygame.init()

perso_stats_selectionne_suplement_les_cheveux_de_ian = None
case_selectionnee_inv = None
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
        self.chemin_info = os.path.join(os.path.dirname(__file__), "assets/info.png")
        self.image_info = pygame.image.load(self.chemin_info).convert_alpha()
        self.image_info = pygame.transform.scale(self.image_info, (600, 300))
    
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

    def drop(self,liste_items_au_sol, player):
        if self.item_utilise is None:
            pass
        else:
            item_drop = self.items.pop(self.index)

            item_drop.position = player.position.copy()
            item_drop.rect.center = item_drop.position
            item_drop.au_sol = True
            liste_items_au_sol.append(item_drop)
            self.item_utilise = None
            self.perso_choisi = None
            self.index = None
            self.x = None
            self.y = None                           
         


boutons_menu = {
    "inventaire": pygame.Rect(50, 200, 150, 50),
    "equipe": pygame.Rect(50, 270, 150, 50),
    "stats": pygame.Rect(50, 340, 150, 50),
    "info": pygame.Rect(50, 410, 150, 50)
}
menu_actif = "inventaire"


def changer_equipe_inv(pos_souris, liste_equipe):
    global case_selectionnee_inv

    hpb_w = 600
    hpb_h = 300
    hpb_x = (width - hpb_w) / 2 + 175
    hpb_y = (height - hpb_h) / 2 + 65

    for i in range(2):
        for j in range(2):
            index = i * 2 + j
            case_x = hpb_x + j * 100 + 10
            case_y = hpb_y + i * 100 + 10
            case_rect = pygame.Rect(case_x, case_y, 100, 100)

            if case_rect.collidepoint(pos_souris) and index < len(liste_equipe):
                if case_selectionnee_inv is None:
                    case_selectionnee_inv = index
                elif case_selectionnee_inv == index:
                    case_selectionnee_inv = None
                else:
                    liste_equipe[case_selectionnee_inv], liste_equipe[index] = liste_equipe[index], liste_equipe[case_selectionnee_inv]
                    case_selectionnee_inv = None
                return

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
                
                hpb_x = (width - hpb_w) / 2 +175  #la meme chose que ce que t'as fait dans équipe ian
                hpb_y = (height - hpb_h) / 2 +65   #mais au centre cette fois
                hpb_w = 1/5 * width  +175
                hpb_h = 1/5 * width  +65

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
                

                for i in range(2):
                    for j in range(2):
                        index = i * 2 + j
                        case_x = hpb_x + j * 100 + 30  
                        case_y = hpb_y + i * 100 + 80 
                        if index < len(liste_equipe):
                            pv = liste_equipe[index].pv
                            pvmax = liste_equipe[index].pvmax
                            pygame.draw.rect(screen, (0, 0, 0), ((case_x-5), case_y, 70, 10)) 
                            if pv > 0:
                                pygame.draw.rect(screen, (200, 0, 0), ((case_x-5), case_y, 70 * (pv/pvmax),10))  # bordure
                            if liste_equipe[index].mana > 0:
                                pygame.draw.rect(screen, (0, 0, 0), ((case_x-5), case_y + 12, 70, 6))  # fond noir
                                pygame.draw.rect(screen, (0, 0, 139), ((case_x-5), case_y + 12, 70 * (liste_equipe[index].mana / liste_equipe[index].manamax), 6))
                if case_selectionnee_inv is not None:
                    i = case_selectionnee_inv // 2
                    j = case_selectionnee_inv % 2
                    case_x = hpb_x + j * 100 + 10
                    case_y = hpb_y + i * 100 + 10
                    pygame.draw.rect(screen, (255, 215, 0), (case_x, case_y, 100, 100), 4)

                


            elif menu_actif == "stats":
                pygame.draw.rect(screen, (180, 140, 80), (hpb_x, hpb_y, 600, 300))

                titre = font.render("Statistiques", True, (0, 0, 0))
                screen.blit(titre, (hpb_x + 200, hpb_y + 20))

                
                case_size = 70
                start_x = hpb_x + 20
                start_y = hpb_y + 60
                intervale = 90

            
                for i in range(2):
                    for j in range(2):
                        index = i * 2 + j
                        case_x = start_x + j * intervale
                        case_y = start_y + i * intervale

                        pygame.draw.rect(screen, (100, 80, 60), (case_x, case_y, case_size, case_size))
                        pygame.draw.rect(screen, (60, 40, 20), (case_x, case_y, case_size, case_size), 2)

                        if index < len(liste_equipe):
                            perso = liste_equipe[index]

                            
                            screen.blit(perso.image, (case_x, case_y - 10))

                          
                            if perso_stats_selectionne_suplement_les_cheveux_de_ian == perso:
                                pygame.draw.rect(screen, (255, 215, 0), (case_x, case_y, case_size, case_size), 3)

             
                if perso_stats_selectionne_suplement_les_cheveux_de_ian is not None:
                    perso = perso_stats_selectionne_suplement_les_cheveux_de_ian

                    x_stats = hpb_x + 250
                    y_stats = hpb_y + 80

                    lignes = [
                        f"PV : {perso.pv}/{perso.pvmax}",
                        f"Mana : {perso.mana}/{perso.manamax}",
                    ]


                    # affichage texte
                    for i, ligne in enumerate(lignes):
                        txt = font.render(ligne, True, (0, 0, 0))
                        screen.blit(txt, (x_stats, y_stats + i * 30))

                else:
                    # message si rien sélectionné
                    txt = font.render("Clique sur un personnage", True, (50, 50, 50))
                    screen.blit(txt, (hpb_x + 230, hpb_y + 150))
            
            
            elif menu_actif == "info":
                screen.blit(mon_inventaire.image_info , (hpb_x, hpb_y))

def changer_menu(pos_souris):
    global menu_actif
    for nom_du_menu, rect in boutons_menu.items():
        if rect.collidepoint(pos_souris):
            menu_actif = nom_du_menu

def selectionner_perso_stats(pos_souris, liste_equipe):
    global perso_stats_selectionne_suplement_les_cheveux_de_ian

    hpb_w = 600
    hpb_h = 300
    hpb_x = width/2 - hpb_w/2
    hpb_y = height/2 - hpb_h/2

    for i in range(2):
        for j in range(2):
            index = i * 2 + j
            case_x = hpb_x + 20 + j * 100
            case_y = hpb_y + 60 + i * 100
            case_rect = pygame.Rect(case_x, case_y, 80, 80)

            if case_rect.collidepoint(pos_souris) and index < len(liste_equipe):
                perso_stats_selectionne_suplement_les_cheveux_de_ian = liste_equipe[index]
