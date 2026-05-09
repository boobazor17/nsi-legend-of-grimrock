import pygame
import random
import os

pygame.init()

pygame.init()

# ajout de a musique (techno/house spécialement pour vous)

pygame.mixer.music.load(
    os.path.join(os.path.dirname(__file__), "fin.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

    # Taille de la fenêtre
WIDTH, HEIGHT = 1000, 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fin du jeu - Paris By Night")

clock = pygame.time.Clock()

# Couleurs du générique 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Police du texte 
font = pygame.font.SysFont("arial", 40)

 # liste du générique de fin

text = [
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
text_y = HEIGHT

# mise en forme des image et affichage 

image1 = pygame.image.load("photo.png")
image2 = pygame.image.load("photoo.png")
image3 = pygame.image.load("photooo.png")

# dimension des images
image1 = pygame.transform.scale(image1, (200, 150))
image2 = pygame.transform.scale(image2, (200, 150))
image3 = pygame.transform.scale(image3, (300, 200))


    # création des particules
particles = []

class Particle:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        # direction aléatoire pour les particules
        self.dx = random.uniform(-5, 5)
        self.dy = random.uniform(-5, 5)

        # durée de vie des particules
        self.life = random.randint(40, 80)

        # taille des particules
        self.size = random.randint(4, 8)

        # couleur des particules
        self.color = (
            random.randint(150,255),
            random.randint(100,255),
            random.randint(0,100)
        )

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.05
        self.life -= 1
    def draw(self):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.size
        )

frame_count = 0
running = True

while running:

    # le fond noir
    screen.fill(BLACK)

    # ferme la fenêtre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
 # place l'image à gauche 
    if frame_count > 120:
        screen.blit(image3, (20, 20))

    # feu d'artifice
    if frame_count == 121:
        for _ in range(150):
            particles.append(
                Particle(170, 120))
            
    # fait défiler le texte 
    for i, line in enumerate(text):

        render_text = font.render(line, True, WHITE)

        screen.blit(
            render_text,
            (
                WIDTH // 2 - render_text.get_width() // 2,
                text_y + i * 50
            )
        )

    # ppour la vitesse du défilement
    text_y -= 0.5

# image 1 + feu d'artifice 
    if frame_count == 220:
        for _ in range(150):
            particles.append(Particle(WIDTH - 140, 300))

    if frame_count > 260:
        screen.blit(image1, (WIDTH - 240, 220))

    # place l'image en bas

    if frame_count > 320:
        screen.blit(image2, (20, HEIGHT - 190))

        # feu d'artifice
        if frame_count == 321:

            for _ in range(120):
                particles.append(Particle(120, HEIGHT - 120))

    # Affiche les particules
    for p in particles[:]:

        p.update()
        p.draw()

        # supprime les particules 
        if p.life <= 0:
            particles.remove(p)

    # Met à jour de écran
    pygame.display.flip()

    clock.tick(60)

    frame_count += 1

# pour quitter pygame
pygame.quit()
