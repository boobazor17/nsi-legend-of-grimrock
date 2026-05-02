import pygame
import math
from camera import *
from monstre import *
from player import *
from Physique import *
import equipe
import os
from map import *
import Inventaire
import Boutique


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

    CLASSES_ENNEMIS = {
    "ennemi1": ennemi1,
    "araignee": araignee,
    }

    liste_portes = map_manager.obj_porte
    plaques = map_manager.plaques

    list_ennemi = []
    for e in map_manager.ennemis_to_spawn:
        classe =  CLASSES_ENNEMIS.get(e["nom"]) #grace a un dictionnaire on récupère le nom du monstre
        if classe:
            list_ennemi.append(classe(e["x"], e["y"])) # les statistiques du monstres sont automatiquement mises depuis sa classe on a juste besoin placer le monstre sur la map pour avoir des coordonnées

    liste_items_au_sol =  [] # liste des items au sol 

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
    attaque_mage = equipe.attaque("mage",30,200,10,0,3000)
   
    fantome_perso1.ajouter_attaque(attaque_mage)
    rat_perso2.ajouter_attaque(attaque_distance)
    pigeon_perso3.ajouter_attaque(attaque_cac)
    perso4.ajouter_attaque(attaque_distance1)      



    chemin = os.path.join(os.path.dirname(__file__), "assets/invent.png")
    image_invent = pygame.image.load(chemin).convert_alpha()
    image_invent = pygame.transform.scale(image_invent, (600, 300))
    

    joueur_or = [100]  # liste pour pouvoir le modifier depuis gerer_clic
    coffres = [obj for obj in map_manager.objets_interactifs if isinstance(obj, Boutique.Coffre)]
    mon_coffre = coffres[0]  # si tu n'en as qu'un
        
    clock   = pygame.time.Clock()
    running = True # variable pour la boucle de jeu

    inventory = False
    paused = False
    t1 = 0
    t2 = 0
    mon_inventaire = Inventaire.inventaire()

    try:
        sound_death = pygame.mixer.Sound("assets/sounds/morxane.mp3")
        sound_death.set_volume(0.5)
    except:
        sound_death = None

    son_death_joue = False


    while running: # boucle du jeu boucle infinie while true 
        clock.tick(60) # permet d'actualiser 60 fois le jeu par seconde (60 fps)
        events = pygame.event.get()
        for event in events:
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
                    Inventaire.changer_menu(event.pos)
                    if Inventaire.menu_actif == "equipe":
                        Inventaire.changer_equipe_inv(event.pos, liste_equipe)
                    else:
                        mon_inventaire.utiliser(event.pos, liste_equipe)
                if not inventory and not paused:
                    equipe.regarde_clique(event.pos, liste_equipe, list_ennemi, player, list_object)
                if mon_coffre.ouvert:
                    mon_coffre.gerer_clic(event.pos, mon_inventaire, joueur_or)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                dx = mon_coffre.position.x - player.rect.centerx
                dy = mon_coffre.position.y - player.rect.centery
                distance = math.sqrt(dx**2 + dy**2)
                if distance <= mon_coffre.distance and not mon_coffre.ouvert:
                    mon_coffre.ouvert = True
                for porte in liste_portes:
                    ddx = porte.position.x - player.rect.centerx
                    ddy = porte.position.y - player.rect.centery
                    distancee = math.sqrt(ddx**2 + ddy**2)
                    if distancee <= porte.distance_interaction and not porte.ouvert:
                        if isinstance(porte, Porte_normale):
                            porte.ouvert = True
                        elif isinstance(porte, Porte_clé):                          # si la porte est une porte à clé
                            for i in range (len(mon_inventaire.items)):         # on parcourt l'inventaire du joueur pour regarder s'il a une clé
                                if mon_inventaire.items[i].nom == "clé":     
                                    porte.ouvert = True                     # on ouvre la porte
                                    mon_inventaire.items.pop(i)             # on supprime la clé de l'inventaire du joueur
                                    break                                   # on sort de la boucle for pour éviter que créer un bug qui supprime toutes les clés de l'inventaire si le joueur en a plusieurs
                if len(liste_items_au_sol) !=0:
                    for item_sol in liste_items_au_sol :
                        item_sol.interaction(player, mon_inventaire, liste_items_au_sol)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                if inventory:
                    mon_inventaire.drop(liste_items_au_sol, player)

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
            for vase in vases:
                vase.interaction(player, screen, font, follow, mon_inventaire, joueur_or, events)
                cam.scroll()
            mon_coffre.interaction(player, screen, font, follow, mon_inventaire, joueur_or, events)
        else:
            for object in list_object:
                pygame.draw.rect(screen, (255,0,0), (object.rect.x - int(cam.offset.x), object.rect.y - int(cam.offset.y), object.rect.width, object.rect.height), 2)
                screen.blit(object.image, follow.appliquer(object.position))

        map_manager.draw(screen, follow)
        for vase in vases:
            screen.blit(vase.image, follow.appliquer(vase.position))
        screen.blit(mon_coffre.image, follow.appliquer(mon_coffre.position))


        for porte in liste_portes:
            if not porte.ouvert:
                screen.blit(porte.image, follow.appliquer(porte.position))
            porte.interaction(player, screen, follow, list_object, mon_inventaire, liste_items_au_sol)
            if isinstance(porte, Porte_plaque):
                image_plaque = porte.dessiner_plaque(screen, follow)
                screen.blit(image_plaque, follow.appliquer(
                     pygame.math.Vector2(porte.rect_plaque.x, porte.rect_plaque.y)
                        ))   

        for item in liste_items_au_sol:
            screen.blit(item.image,follow.appliquer(item.position))
                

        # Dessin du joueur
        player.draw(screen,follow)
    

        if mon_coffre.ouvert and player.pv > 0 and not paused:
            mon_coffre.dessiner_boutique(screen, joueur_or[0])

       
    
        if player.pv <= 0:
            
            if not son_death_joue and sound_death:
                sound_death.play()
                son_death_joue = True
                        
            font_gameover = pygame.font.Font(None, 230)
            texte_go = font_gameover.render("GAME OVER", True, (180, 20, 20))
            
            texte_go_ombre = font_gameover.render("GAME OVER", True, (60, 0, 0))
            screen.blit(texte_go_ombre, (width//2 - texte_go.get_width()//2 + 4, 54))  
            screen.blit(texte_go, (width//2 - texte_go.get_width()//2, 50))
            
        
            bouton_rejouer = pygame.Rect(440,350,200,70)
            img_bouton = pygame.image.load("/Users/famille/Desktop/nsi-legend-of-grimrock/Paris By night/assets/button.png")
            img_bouton = pygame.transform.scale(img_bouton, (370, 130))
            screen.blit(img_bouton, (358, 300))
            font = pygame.font.Font(None,60)
            texte = font.render("REJOUER", True, (20, 40, 70))
            screen.blit(texte, (443, 352))
            
            bouton_quitter = pygame.Rect(358, 500, 370, 130)
            img_bouton = pygame.image.load("/Users/famille/Desktop/nsi-legend-of-grimrock/Paris By night/assets/button.png")
            img_bouton = pygame.transform.scale(img_bouton, (370, 130))
            screen.blit(img_bouton, (358, 500))
            font = pygame.font.Font(None,60)
            texte = font.render("QUITTER", True, (20, 40, 70))
            screen.blit(texte, (435, 552))
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_quitter.collidepoint(event.pos):
                    return "menu"
                if bouton_rejouer.collidepoint(event.pos):
                    player.pv = player.pvmax
                    son_gameover_joue = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_quitter.collidepoint(event.pos):
                    return "menu"


        # Dessin du menu pause
        if paused:
            hpb_w = 480
            hpb_h = 240
            hpb_x = width/2 - hpb_w/2
            hpb_y = height/2 - hpb_h/2
            t1 = pygame.time.get_ticks() # réinitialisation du timer pour éviter les appuis rapides qui font bug le menu pause
            
            

            bouton_quitter = pygame.Rect(440,350,200,70)
            img_bouton = pygame.image.load("/Users/famille/Desktop/nsi-legend-of-grimrock/Paris By night/assets/button.png")
            img_bouton = pygame.transform.scale(img_bouton, (370, 130))
            screen.blit(img_bouton, (358, 300))
            font = pygame.font.Font(None,60)
            texte = font.render("QUITTER", True, (20, 40, 70))
            screen.blit(texte, (443, 352))
            
            bouton_sauvegarder = pygame.Rect(358, 500, 370, 130)
            img_bouton = pygame.image.load("/Users/famille/Desktop/nsi-legend-of-grimrock/Paris By night/assets/button.png")
            img_bouton = pygame.transform.scale(img_bouton, (370, 130))
            screen.blit(img_bouton, (358, 500))
            font = pygame.font.Font(None,40)
            texte = font.render("SAUVEGARDER", True, (20, 40, 70))
            screen.blit(texte, (435, 562))
            
            bouton_reprendre = pygame.Rect(358, 100, 370, 130)
            img_bouton = pygame.image.load("/Users/famille/Desktop/nsi-legend-of-grimrock/Paris By night/assets/button.png")
            img_bouton = pygame.transform.scale(img_bouton, (370, 130))
            screen.blit(img_bouton, (358, 100))
            font = pygame.font.Font(None,48)
            texte = font.render("REPRENDRE", True, (20, 40, 70))
            screen.blit(texte, (438, 158))
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_quitter.collidepoint(event.pos):
                    return "menu"
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_sauvegarder.collidepoint(event.pos):
                    return "sauvegarde"
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_reprendre.collidepoint(event.pos):
                    paused = False
            

        
        # si le jeu n'est pas en pause ça continue 
        if not paused:
            pass
        
               

        if not paused :
            for monstree in list_ennemi:
                if  monstree.pv > 0:
                    l = [m for m in list_ennemi if m != monstree]
                    monstree.deplacement(player, l,list_object)
                    
                    monstree.attaque_m(player, liste_equipe, list_object, list_ennemi)
                    if hasattr(monstree, "dash"): # vérifie si l'objet monstre a bien une méthode monstre avant de l'appeler pratique car toutes les classes n'ont pas les mêmes méthodes
                        monstree.dash(player, liste_equipe, 8)
                    
            for monstree in list_ennemi:
                monstree.draw(screen, follow, player)

        if not paused and player.pv > 0 and not inventory:
            equipe.afficher_equipe(liste_equipe,screen)
            equipe.afficher_pv (liste_equipe,screen)
        
        for elem in liste_equipe:
            temps = pygame.time.get_ticks()
            if elem.pv > 0 : 
                elem.regenerer_mana()
            if (elem.attaque.nom == "distance" or elem.attaque.nom == "mage") and elem.attaque.proj : # priorité des opérations 
                elem.attaque.update(liste_equipe, list_object, temps,screen,list_ennemi,follow)
                elem.attaque.draw_proj(screen, follow)
            elif elem.attaque.nom == "cac" and elem.attaque.cac.cac_actif:
                elem.attaque.update(liste_equipe, list_object, temps,screen,list_ennemi,follow)
            if temps - elem.attaque.attaque_dernier_temps < 150 :
                elem.attaque.draw_proj(screen, follow)  
        liste(list_ennemi)


        if inventory and player.pv > 0 and not paused:
            Inventaire.les_pieds_de_louis(screen, font, liste_equipe, mon_inventaire, image_invent)
                
        pygame.display.update()  
    pygame.quit()
    return None
