import pygame
import os
import math
from Physique import Object, item
 
pygame.init()
 
width = 1080
height = 720
 

CATALOGUE = [
    {"nom": "Potion de soin",   "prix": 30,  "effet":  20, "image": "assets/potion_vie.png"},
    {"nom": "Potion de dégâts", "prix": 30,  "effet": -20, "image": "assets/potion_degat.png"},
    {"nom": "Grande potion",    "prix": 60,  "effet":  50, "image": "assets/potion_vie.png"},
]
 
 
class Coffre(Object):
    def __init__(self, x, y):
        super().__init__(x, y, 60, 60, (180, 120, 40), "assets/vase.png")
        self.image_originale = self.image
        self.position = pygame.math.Vector2(x, y)
        self.distance = 200          # distance max d'interaction
        self.ouvert = False         # interface boutique visible ou non
        self.font = pygame.font.Font(None, 28)
        self.font_titre = pygame.font.Font(None, 36)
        self.images_items = []
        self.rect_fermer = None
        self.rects_acheter = []
        for article in CATALOGUE:
            try:
                chemin = os.path.join(os.path.dirname(__file__), article["image"])
                img = pygame.image.load(chemin).convert_alpha()
                img = pygame.transform.scale(img, (50, 50))
            except Exception:
                img = pygame.Surface((50, 50))
                img.fill((200, 100, 100))

            self.images_items.append(img)
        

    def dessiner_indicateur(self, screen, follow):
        texte_x = int(self.position.x - follow.camera.offset.x)
        texte_y = int(self.position.y - follow.camera.offset.y) - 50
        pygame.draw.circle(screen, "gold", (texte_x + 10, texte_y + 10), 20)
        texte = self.font_titre.render("E", True, (255, 255, 255))
        screen.blit(texte, (texte_x, texte_y))
 
    
    def animer(self):
        u = pygame.time.get_ticks()
        w = 60 + math.sin(u / 200) * 3
        h = 60 + math.sin(u / 200) * 3
        self.image = pygame.transform.scale(self.image_originale, (int(w), int(h)))
 

    def dessiner_boutique(self, screen, or_joueur):
        # fond principal
        bx, by, bw, bh = width // 2 - 250, height // 2 - 200, 500, 400
        pygame.draw.rect(screen, (60, 45, 25), (bx, by, bw, bh), border_radius=12)
        pygame.draw.rect(screen, (200, 160, 80), (bx, by, bw, bh), 3, border_radius=12)
 
        # titre
        titre = self.font_titre.render("⚒  Boutique", True, (255, 215, 0))
        screen.blit(titre, (bx + bw // 2 - titre.get_width() // 2, by + 14))
 
        # or du joueur
        or_texte = self.font.render(f"Or : {or_joueur}", True, (255, 215, 0))
        screen.blit(or_texte, (bx + bw - or_texte.get_width() - 16, by + 16))
 
        # ligne séparatrice
        pygame.draw.line(screen, (200, 160, 80), (bx + 10, by + 55), (bx + bw - 10, by + 55), 2)
 
        # items
        self.rects_acheter = []
        for idx, article in enumerate(CATALOGUE):
            iy = by + 70 + idx * 90
            # cadre item
            pygame.draw.rect(screen, (90, 65, 35), (bx + 15, iy, bw - 30, 78), border_radius=8)
            pygame.draw.rect(screen, (160, 120, 60), (bx + 15, iy, bw - 30, 78), 2, border_radius=8)
 
            # image item
            img = self.images_items[idx]
            screen.blit(img, (bx + 25, iy + 14))
 
            # nom
            nom = self.font.render(article["nom"], True, (245, 235, 200))
            screen.blit(nom, (bx + 90, iy + 10))
 
            # effet
            effet_val = article["effet"]
            effet_couleur = (100, 220, 100) if effet_val > 0 else (220, 100, 100)
            effet_txt = self.font.render(
                f"{'+ ' if effet_val > 0 else ''}{effet_val} PV", True, effet_couleur
            )
            screen.blit(effet_txt, (bx + 90, iy + 38))
 
            # bouton acheter
            btn = pygame.Rect(bx + bw - 130, iy + 20, 110, 38)
            peut_acheter = or_joueur >= article["prix"]
            couleur_btn = (180, 140, 40) if peut_acheter else (90, 70, 30)
            pygame.draw.rect(screen, couleur_btn, btn, border_radius=6)
            prix_txt = self.font.render(f"{article['prix']} or", True, (255, 255, 255) if peut_acheter else (130, 130, 130))
            screen.blit(prix_txt, (btn.x + btn.w // 2 - prix_txt.get_width() // 2,
                                   btn.y + btn.h // 2 - prix_txt.get_height() // 2))
            self.rects_acheter.append((btn, idx, peut_acheter))
 
        # bouton fermer
        self.rect_fermer = pygame.Rect(bx + bw // 2 - 60, by + bh - 48, 120, 36)
        pygame.draw.rect(screen, (120, 50, 50), self.rect_fermer, border_radius=6)
        fermer_txt = self.font.render("Fermer", True, (255, 255, 255))
        screen.blit(fermer_txt, (self.rect_fermer.x + self.rect_fermer.w // 2 - fermer_txt.get_width() // 2,
                                  self.rect_fermer.y + self.rect_fermer.h // 2 - fermer_txt.get_height() // 2))
 
    
    def interaction(self, player, screen, font, follow, mon_inventaire, joueur_or,events):
        print(self.ouvert)
        dx = self.position.x - player.rect.centerx
        dy = self.position.y - player.rect.centery
        distance_reelle = math.sqrt(dx ** 2 + dy ** 2)
 
        if distance_reelle <= self.distance and not self.ouvert:
            self.dessiner_indicateur(screen, follow)
            self.animer()
        else:
            if not self.ouvert:
                self.image = self.image_originale

    
    def gerer_clic(self, pos_souris, mon_inventaire, joueur_or):
        if not self.ouvert:
            return

        if not hasattr(self, "rect_fermer"):
            return

        # fermer
        if self.rect_fermer.collidepoint(pos_souris):
            self.ouvert = False
            return
 
        # acheter
        for btn, idx, peut_acheter in self.rects_acheter:
            if btn.collidepoint(pos_souris) and peut_acheter:
                article = CATALOGUE[idx]
                nouvel_item = item(
                    article["nom"], 50, 50, article["effet"],
                    (255, 200, 50), article["image"]
                )
                mon_inventaire.ajouter(nouvel_item)
                joueur_or[0] -= article["prix"]
                break
