import pygame
import random
import os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 1080, 720

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.uniform(-5, 5)
        self.dy = random.uniform(-5, 5)
        self.life = random.randint(40, 80)
        self.size = random.randint(4, 8)
        self.color = (
            random.randint(150, 255),
            random.randint(100, 255),
            random.randint(0, 100)
        )

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.05
        self.life -= 1

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.size
        )

def lancer_fin():
    pygame.init()

    pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), "assets/sounds/fin.mp3"))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fin du jeu - Paris By Night")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("arial", 40)

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

    text_y = float(HEIGHT)

    image1 = pygame.image.load(os.path.join(os.path.dirname(__file__), "assets/photo.png"))
    image2 = pygame.image.load(os.path.join(os.path.dirname(__file__), "assets/photoo.png"))
    image3 = pygame.image.load(os.path.join(os.path.dirname(__file__), "assets/photooo.png"))

    image1 = pygame.transform.scale(image1, (200, 150))
    image2 = pygame.transform.scale(image2, (200, 150))
    image3 = pygame.transform.scale(image3, (300, 200))

    particles = []
    frame_count = 0
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if frame_count > 120:
            screen.blit(image3, (20, 20))

        if frame_count == 121:
            for _ in range(150):
                particles.append(Particle(170, 120))

        for i, line in enumerate(text):
            render_text = font.render(line, True, WHITE)
            screen.blit(render_text, (
                WIDTH // 2 - render_text.get_width() // 2,
                int(text_y) + i * 50
            ))

        text_y -= 0.5

        if frame_count == 220:
            for _ in range(150):
                particles.append(Particle(WIDTH - 140, 300))

        if frame_count > 260:
            screen.blit(image1, (WIDTH - 240, 220))

        if frame_count > 320:
            screen.blit(image2, (20, HEIGHT - 190))
            if frame_count == 321:
                for _ in range(120):
                    particles.append(Particle(120, HEIGHT - 120))

        for p in particles[:]:
            p.update()
            p.draw(screen)
            if p.life <= 0:
                particles.remove(p)

        pygame.display.flip()
        clock.tick(60)
        frame_count += 1

    pygame.quit()
