import pygame
import math
from camera import *
from monstre import *
from player import *

def lancer():
 
    pygame.init()
    font = pygame.font.Font(None,40)
    width = 1080
    height = 720
    speed = 10
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Fenêtre d'accueil")
    
    # Initialisation joueur + caméra
    player = Player(300, 200)
    cam    = Camera(player)
    follow = Follow(cam, player)
    border = Border(cam, player)
    auto   = Auto(cam, player)
    cam.setmethod(follow)  # mode caméra actif (follow / border / auto)
    
    
    ennemi1 = monstre("ennemi1" , 50, 60, 10, 220, 100)
    
    clock   = pygame.time.Clock()
    running = True
    
    while running:
        clock.tick(60)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        screen.fill((201, 158, 89))
    
        # déplacement du personnage uniforme dans chaque directions
        touches = pygame.key.get_pressed()
        if player.pv > 0:
            if touches[pygame.K_z] or touches[pygame.K_UP]:
                if (touches[pygame.K_d] or touches[pygame.K_RIGHT]) ^ (touches[pygame.K_q] or touches[pygame.K_LEFT]): # ^ = ou exclusif (xor)
                    player.rect.y -= speed / math.sqrt(2)
                else:
                    player.rect.y -= speed
            if touches[pygame.K_s] or touches[pygame.K_DOWN]:
                if (touches[pygame.K_d] or touches[pygame.K_RIGHT]) ^ (touches[pygame.K_q] or touches[pygame.K_LEFT]):
                    player.rect.y += speed / math.sqrt(2)
                else:
                    player.rect.y += speed
            if touches[pygame.K_q] or touches[pygame.K_LEFT]:
                if (touches[pygame.K_z] or touches[pygame.K_UP]) ^ (touches[pygame.K_s] or touches[pygame.K_DOWN]):
                    player.rect.x -= speed / math.sqrt(2)
                else:
                    player.rect.x -= speed
            if touches[pygame.K_d] or touches[pygame.K_RIGHT]:
                if (touches[pygame.K_z] or touches[pygame.K_UP]) ^ (touches[pygame.K_s] or touches[pygame.K_DOWN]):
                    player.rect.x += speed / math.sqrt(2)
                else:
                    player.rect.x += speed
    
        # création de la barre de vie , rectangle noir puis rectangle rouge représentant la vie
        hpb_w = 200
        hpb_h = 12
        hpb_x = width/2 - hpb_w/2
        hpb_y = height/2 + 4*height//9  # 1/18px au dessus du bas de l'écran 
        barre_hp = pygame.Rect(hpb_x, hpb_y, hpb_w, hpb_h)
        pygame.draw.rect(screen, (0, 0, 0), barre_hp )
        hpb_w = 200 - 200 + player.pv*2
        if hpb_w > 200 :
            hpb_w = 200
        hpb_h = 12
        hpb_x = width/2 - hpb_w/2
        hpb_y = height/2 + 4*height//9  # 1/18px au dessus du bas de l'écran 
        barre_hp2 = pygame.Rect(hpb_x, hpb_y, hpb_w, hpb_h)
        pygame.draw.rect(screen, (255, 0, 0), barre_hp2 )
        cam.scroll()
    
        # Dessin du joueur
        if player.pv > 0:
            player.draw(screen, cam.offset)
    
        if player.pv <= 0:
                # dimensions du bouton
            bouton_w = 200
            bouton_h = 60
    
            # centré horizontalement, en dessous du joueur
            bouton_x = width/2 - bouton_w/2
            bouton_y = height/2 + 50  # 50px en dessous du centre (là où est le joueur)
    
            bouton_rejouer = pygame.Rect(bouton_x, bouton_y, bouton_w, bouton_h)
            pygame.draw.rect(screen, (139, 94, 44), bouton_rejouer)
    
            texte = font.render("Rejouer", True, (245, 240, 220))
            texte_x = bouton_x + bouton_w/2 - texte.get_width()/2   # centré dans le bouton
            texte_y = bouton_y + bouton_h/2 - texte.get_height()/2  # centré dans le bouton
            screen.blit(texte, (texte_x, texte_y))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_rejouer.collidepoint(event.pos):
                    player.pv = player.pvmax 
                    temps =  pygame.time.get_ticks()
                    player.invincible_temps = temps
                    
        ennemi1.attaque_m(player)
        ennemi1.deplacement(player)
        ennemi1.draw(screen, cam.offset)
        # Exemple d'objet fixe dans le monde (cercle bleu)
        pygame.draw.circle(screen, (0, 0, 255), (100 - int(cam.offset.x), 50 - int(cam.offset.y)), 20)
    
        pygame.display.update()
        
    pygame.quit()
