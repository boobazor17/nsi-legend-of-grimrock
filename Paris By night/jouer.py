import pygame
import math
from camera import *
from monstre import *
from player import *
from Physique import *
import equipe
import os
from map import *




def lancer(screen, font):
    pygame.init()
    width = 1080
    height = 720
    speed = 10

    
    map_manager = Map_Manager()
    map_manager.load_map("assets/caca.tmx")
    list_object = map_manager.list_object
    vases = map_manager.objets_interactifs

    player = Player(map_manager.spawnpoint_joueur.x, map_manager.spawnpoint_joueur.y)
    cam = Camera(player)
    follow = Follow(cam, player)
    border = Border(cam, player)
    auto = Auto(cam, player)
    cam.setmethod(follow)

    list_ennemi = []
    for e in map_manager.ennemis_to_spawn:
        list_ennemi.append(monstre(
            e["x"], e["y"], e["nom"],
            e["pv"], e["pvmax"],
            e["attaque"],
            e["distance"],
            e["distance_attaque"]
        ))

    vase1 = Vase(200, 500)
    mur = Mur(200, 600,500,200)
    
    
    
    # personage
    fantome_perso1 = equipe.equipe(0,0,"fantome",100,100,20,100,10,"assets/personnage log/fantome.png")             
    rat_perso2 =  equipe.equipe(0,0,"rat", 50, 50,20,20,10,"assets/personnage log/rat.png")       
    pigeon_perso3 = equipe.equipe(0,0,"nom",100,100,20,20,10,"assets/personnage log/pigeon.png")         
    perso4 = equipe.equipe(0,0,"nom", 100, 100,20,20,10,"assets/personnage log/pigeon.png")
    
    liste_ts = [fantome_perso1,rat_perso2,pigeon_perso3,perso4 ]
    liste_equipe = liste_ts[:4] #définit une équipe de base que l'on pourra modifier par la suite
   
     #attaque
    attaque_cac = equipe.attaque("cac", 20, 200, 0, 0, 1000)
    attaque_distance = equipe.attaque("distance", 10, 300, 0, 0, 1000) 
    attaque_distance1 = equipe.attaque("distance", 10, 300, 0, 0, 1000) # on créer 2 instances séparés pour pas qu'elle partage la même mémoire.
    attaque_mage = equipe.attaque("mage",30,200,10,0,5000)
   
    fantome_perso1.ajouter_attaque(attaque_mage)
    rat_perso2.ajouter_attaque(attaque_distance)
    pigeon_perso3.ajouter_attaque(attaque_cac)
    perso4.ajouter_attaque(attaque_distance1)      



    chemin = os.path.join(os.path.dirname(__file__), "assets/invent.png")
    image_invent = pygame.image.load(chemin).convert_alpha()
    image_invent = pygame.transform.scale(image_invent, (600, 300))
    
    ennemi1 = monstre(0,0,"ennemi1" , 100, 100, 10, 250, 130)
    
    
        
    clock   = pygame.time.Clock()
    running = True # variable pour la boucle de jeu

    inventory = False
    paused = False
    t1 = 0
    t2 = 0
    mon_inventaire = inventaire()



    while running: # boucle du jeu boucle infinie while true 
        clock.tick(60) # permet d'actualiser 60 fois le jeu par seconde (60 fps)
    
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
                    for elem in liste_equipe:
                         elem.pv = elem.pvmax
                    player.invincible_temps = pygame.time.get_ticks()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                t2 = pygame.time.get_ticks() 
                if  t2 - 500 > 0:
                    inventory = not inventory
                    t2 = pygame.time.get_ticks()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if inventory:
                    mon_inventaire.utiliser(event.pos,liste_equipe)
                if not inventory and not paused:
                    equipe.regarde_clique(event.pos,liste_equipe,list_ennemi,player,list_object) #event.pos = pos_souris



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
        if player.velocity.length() > 0:
            player.direction = player.velocity.normalize()

        # effet assombri lorsque le joueur est dans son inventaire a retravailler
        if inventory and player.pv and not paused> 0: 
            overlay = pygame.Surface((width, height))
            overlay.set_alpha(150)  # 0 = invisible, 255 = opaque
            overlay.fill((171, 128, 59))  
            screen.blit(overlay, (0, 0))

        if not paused and not inventory:
            player.position.x += player.velocity.x
            player.rect.center = player.position
            player.collisions_x(list_object)
            player.position.y += player.velocity.y
            player.rect.center = player.position
            player.collisions_y(list_object)
            map_manager.draw(screen, follow)
            for vase in vases:
                vase.interaction(player,screen, font, follow, mon_inventaire)
                cam.scroll()
        else:
            for object in list_object:
                pygame.draw.rect(screen, (255,0,0), (object.rect.x - int(cam.offset.x), object.rect.y - int(cam.offset.y), object.rect.width, object.rect.height), 2) #  dessine les hitbox des objets en rouge
                screen.blit(object.image, follow.appliquer(object.position))

        map_manager.draw(screen, follow)
        for vase in vases:
                screen.blit(vase.image, follow.appliquer(vase.position))
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

            bouton_quitter = pygame.Rect(440,350,200,70)
            pygame.draw.rect(screen,(201, 158, 89),bouton_quitter)
            texte = font.render("quitter", True, ('white'))
            screen.blit(texte,(490,370))
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_quitter.collidepoint(event.pos):
                    return "menu"
            

        
        # Ton code de jeu ici, mais seulement si pas en pause
        if not paused:
            # bouger les sprites, mettre à jour le jeu...
            pass
        
        
               

        if not paused :
            for monstree in list_ennemi:
                if  monstree.pv > 0:
                    l = [m for m in list_ennemi if m != monstree]
                    monstree.deplacement(player, l,list_object)
                    monstree.attaque_m(player,list_object,liste_equipe)
                    monstree.dash(player,liste_equipe,8)
            for monstree in list_ennemi:
                monstree.draw(screen, follow)

        if not paused and player.pv > 0 and not inventory:
            equipe.afficher_equipe(liste_equipe,screen)
            equipe.afficher_pv (liste_equipe,screen)
        
        for elem in liste_equipe:
            temps = pygame.time.get_ticks()
            elem.regenerer_mana()
            if elem.attaque.nom == "distance" or elem.attaque.nom == "mage" and elem.attaque.proj :
                elem.attaque.update(liste_equipe, list_object, temps,screen,list_ennemi,follow)
                elem.attaque.draw_proj(screen, follow)
            elif elem.attaque.nom == "cac" and elem.attaque.cac.cac_actif:
                elem.attaque.update(liste_equipe, list_object, temps,screen,list_ennemi,follow)
            if temps - elem.attaque.attaque_dernier_temps < 150 :
                elem.attaque.draw_proj(screen, follow)  
        ennemi1.liste(list_ennemi)


        if inventory and player.pv > 0 and not paused:
            hpb_w = 600
            hpb_h = 300
            hpb_x = width/2 - hpb_w/2
            hpb_y = height/2 - hpb_h/2
            t2 = pygame.time.get_ticks() # réinitialisation du timer pour éviter les appuis rapides qui font bug le menu pause

            screen.blit(image_invent, (hpb_x, hpb_y )) # affichage de l'inventaire du joueur dans le menu inventaire
            mon_inventaire.draw(screen, liste_equipe)
            
        pygame.display.update()
    return "menu"
        
