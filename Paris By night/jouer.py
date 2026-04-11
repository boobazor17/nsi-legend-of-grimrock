import pygame
import math
from camera import *
from monstre import *
from player import *
from Physique import *
import os




def lancer():
    pygame.init()
    font = pygame.font.Font(None,40)
    width = 1080
    height = 720
    speed = 10
    
    

    vase1 = Vase(200, 500)
    list_object =[
    vase1 ]
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Fenêtre d'accueil")
    
    # Initialisation joueur + caméra
    player = Player(300, 200)
    cam    = Camera(player)
    follow = Follow(cam, player)
    border = Border(cam, player)
    auto   = Auto(cam, player)
    cam.setmethod(follow)  # mode caméra actif (follow / border / auto)

    chemin = os.path.join(os.path.dirname(__file__), "assets/invent.png")
    image_invent = pygame.image.load(chemin).convert_alpha()
    image_invent = pygame.transform.scale(image_invent, (600, 300))
    
    ennemi1 = monstre(0,0,"ennemi1" , 50, 60, 10, 250, 130)
    list_ennemi = [ennemi1]
    clock   = pygame.time.Clock()
    running = True

    inventory = False
    paused = False
    t1 = 0
    t2 = 0
    mon_inventaire = inventaire()
    while running:
        clock.tick(60)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                t1 = pygame.time.get_ticks() 
                if  t1 - 500 > 0:
                    paused = not paused
                    t1 = pygame.time.get_ticks()
            elif event.type == pygame.MOUSEBUTTONDOWN and player.pv <= 0:
                if bouton_rejouer.collidepoint(event.pos):
                    player.pv = player.pvmax
                    player.invincible_temps = pygame.time.get_ticks()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                t2 = pygame.time.get_ticks() 
                if  t2 - 500 > 0:
                    inventory = not inventory
                    t2 = pygame.time.get_ticks()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if inventory:
                    mon_inventaire.utiliser(event.pos, player)



        screen.fill((201, 158, 89))
        player.velocity = pygame.math.Vector2(0, 0)
        # déplacement du personnage uniforme dans chaque directions
        touches = pygame.key.get_pressed()
        if player.pv > 0:
            if touches[pygame.K_z] or touches[pygame.K_UP]:
                if (touches[pygame.K_d] or touches[pygame.K_RIGHT]) ^ (touches[pygame.K_q] or touches[pygame.K_LEFT]): # ^ = ou exclusif (xor)
                    player.velocity.y = - speed / math.sqrt(2)
                else:
                    player.velocity.y = - speed
            if touches[pygame.K_s] or touches[pygame.K_DOWN]:
                if (touches[pygame.K_d] or touches[pygame.K_RIGHT]) ^ (touches[pygame.K_q] or touches[pygame.K_LEFT]):
                    player.velocity.y = speed / math.sqrt(2)
                else:
                    player.velocity.y = speed
            if touches[pygame.K_q] or touches[pygame.K_LEFT]:
                if (touches[pygame.K_z] or touches[pygame.K_UP]) ^ (touches[pygame.K_s] or touches[pygame.K_DOWN]):
                    player.velocity.x = -speed / math.sqrt(2)
                else:
                    player.velocity.x = -speed
            if touches[pygame.K_d] or touches[pygame.K_RIGHT]:
                if (touches[pygame.K_z] or touches[pygame.K_UP]) ^ (touches[pygame.K_s] or touches[pygame.K_DOWN]):
                    player.velocity.x= speed / math.sqrt(2)
                else:
                    player.velocity.x = speed
 
        if not paused and not inventory:
            player.position += player.velocity
            player.rect.center = player.position
            for object in list_object: # check tous les objets de la liste pour voir s'il y a une collision avec le joueur
                # pygame.draw.rect(screen, (255,0,0), (object.rect.x - int(cam.offset.x), object.rect.y - int(cam.offset.y), object.rect.width, object.rect.height), 2) #  dessine les hitbox des objets en rouge 
                screen.blit(object.image, follow.appliquer(object.position))
            player.collisions(list_object) 
            vase1.interaction(player,screen, font, follow, mon_inventaire)
            cam.scroll()
        else:
            for object in list_object:
                pygame.draw.rect(screen, (255,0,0), (object.rect.x - int(cam.offset.x), object.rect.y - int(cam.offset.y), object.rect.width, object.rect.height), 2) #  dessine les hitbox des objets en rouge
                screen.blit(object.image, follow.appliquer(object.position))

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
        
        player.draw(screen,follow)
    
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

        
        

        # Dessin du menu pause
        if paused:
            hpb_w = 480
            hpb_h = 240
            hpb_x = width/2 - hpb_w/2
            hpb_y = height/2 - hpb_h/2
            t1 = pygame.time.get_ticks() # réinitialisation du timer pour éviter les appuis rapides qui font bug le menu pause
            
            texte = font.render("Menu Pause", True, (245, 240, 220))
            texte_x = hpb_x+ hpb_w/2 - texte.get_width()/2   # centré dans le bouton
            texte_y = hpb_y + hpb_h/2 - texte.get_height()/2 -100  # centré dans le bouton
            menu_pause = pygame.Rect(hpb_x, hpb_y, hpb_w, hpb_h)
            pygame.draw.rect(screen, (128, 94, 40), menu_pause)
            screen.blit(texte, (texte_x, texte_y))

        # Ton code de jeu ici, mais seulement si pas en pause
        if not paused:
            # bouger les sprites, mettre à jour le jeu...
            pass
        
        
                   

        if not paused and ennemi1.pv > 0:
            ennemi1.attaque_m(player)
            ennemi1.deplacement(player)
            ennemi1.dash(player)
        ennemi1.draw(screen, follow)
        

        if inventory and player.pv > 0 and not paused:
            hpb_w = 600
            hpb_h = 300
            hpb_x = width/2 - hpb_w/2
            hpb_y = height/2 - hpb_h/2
            t2 = pygame.time.get_ticks() # réinitialisation du timer pour éviter les appuis rapides qui font bug le menu pause

            screen.blit(image_invent, (hpb_x, hpb_y )) # affichage de l'inventaire du joueur dans le menu inventaire
            mon_inventaire.draw(screen)
        
        pygame.display.update()
    pygame.quit()
        

