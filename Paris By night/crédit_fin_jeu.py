import pygame
import random
import os

pygame.init()

# ajout de la musique
pygame.mixer.music.load(
    os.path.join("assets", "fin.mp3")
)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Taille de la fenêtre
LARGEUR, HAUTEUR = 1000, 700

ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Fin du jeu - Paris By Night")

horloge = pygame.time.Clock()

# Couleurs du générique
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)

# Police du texte
police = pygame.font.SysFont("arial", 40)

# Liste du générique de fin
texte = [
    "Paris By Night",
    "",
    "Un jeu de :",
    "",
    "Ian BEAUGRAND",
    "Léoti CHARLES-LANDIER",
    "Lola MOULIUS-MAZI",
    "Roxane MOINE-ANCIAN",
    "",
    "Merci d'avoir joué !"
]

# Position du texte au début
position_texte_y = HAUTEUR

# Chargement des images
image1 = pygame.image.load("assets/photo.png")
image2 = pygame.image.load("assets/photoo.png")
image3 = pygame.image.load("assets/photooo.png")

# Dimensions des images
image1 = pygame.transform.scale(image1, (200, 150))
image2 = pygame.transform.scale(image2, (200, 150))
image3 = pygame.transform.scale(image3, (300, 200))

# Création des particules
particules = []

class Particule:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        # direction aléatoire des particules
        self.vitesse_x = random.uniform(-5, 5)
        self.vitesse_y = random.uniform(-5, 5)

        # durée de vie des particules
        self.vie = random.randint(40, 80)

        # taille des particules
        self.taille = random.randint(4, 8)

        # couleur des particules
        self.couleur = (
            random.randint(150, 255),
            random.randint(100, 255),
            random.randint(0, 100)
        )

    def mise_a_jour(self):

        self.x += self.vitesse_x
        self.y += self.vitesse_y

        # effet de gravité
        self.vitesse_y += 0.05

        # diminution de la durée de vie
        self.vie -= 1

    def afficher(self):

        pygame.draw.circle(
            ecran,
            self.couleur,
            (int(self.x), int(self.y)),
            self.taille
        )

compteur_images = 0

running = True

while running :

    # fond noir
    ecran.fill(NOIR)

    # fermeture de la fenêtre
    for evenement in pygame.event.get():

        if evenement.type == pygame.QUIT:
            running = False

    # place l'image à gauche
    if compteur_images > 120:
        ecran.blit(image3, (20, 20))

    # feu d'artifice
    if compteur_images == 121:

        for _ in range(150):
            particules.append(
                Particule(170, 120)
            )

    # fait défiler le texte
    for numero_ligne, ligne in enumerate(texte):

        texte_affiche = police.render(
            ligne,
            True,
            BLANC
        )

        ecran.blit(
            texte_affiche,
            (
                LARGEUR // 2 - texte_affiche.get_width() // 2,
                position_texte_y + numero_ligne * 50
            )
        )

    # vitesse du défilement
    position_texte_y -= 0.5

    # image 1 + feu d'artifice
    if compteur_images == 220:

        for _ in range(150):
            particules.append(
                Particule(LARGEUR - 140, 300)
            )

    if compteur_images > 260:
        ecran.blit(image1, (LARGEUR - 240, 220))

    # place l'image en bas
    if compteur_images > 320:

        ecran.blit(image2, (20, HAUTEUR - 190))

        # feu d'artifice
        if compteur_images == 321:

            for _ in range(120):
                particules.append(
                    Particule(120, HAUTEUR - 120)
                )

    # affichage des particules
    for particule in particules[:]:

        particule.mise_a_jour()
        particule.afficher()

        # supprime les particules mortes
        if particule.vie <= 0:
            particules.remove(particule)

    # mise à jour de l'écran
    pygame.display.flip()

    # limite à 60 FPS
    horloge.tick(60)

    compteur_images += 1

# fermeture de pygame
pygame.quit()
