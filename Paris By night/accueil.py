import pygame
pygame.init()
import credits
import sauvegarde
import jouer
import assetss
import menu_equipe

# Initialisation de la fenêtre principale du jeu
pygame.display.set_caption("caca")
screen = pygame.display.set_mode((1080, 720))

# Chargement et redimensionnement du fond d'écran du menu
fond = pygame.image.load("assets/fond.png")
fond = pygame.transform.scale(fond, (1080, 720))

# Chargement et redimensionnement de l'image des boutons du menu
bouton_img = pygame.image.load("assets/bouton.png")
bouton_img = pygame.transform.scale(bouton_img, (260, 130))

# Polices : une pour les textes normaux, une grande pour le titre
font = pygame.font.Font(None, 40)
font_titre = pygame.font.Font(None, 220)

# Chargement des images statiques via le module assetss
images = assetss.charger_images()

# Son d'introduction joué une seule fois au lancement de l'intro
son = pygame.mixer.Sound("assets/sounds/audio_intro.mp3")
son_lance = False  # flag pour éviter de relancer le son à chaque frame

# État initial du jeu — gère quelle "page" est affichée
etat = "menu"
running = True
save_a_charger = None   # données de sauvegarde à charger si le joueur reprend une partie
equipe_choisie = None   # équipe choisie dans le menu de sélection

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if etat == "menu":
                # Navigation vers les différents états selon le bouton cliqué
                if bouton_credits.collidepoint(event.pos):
                    etat = "credits"
                elif bouton_sauvegarde.collidepoint(event.pos):
                    etat = "sauvegarde"
                elif bouton_jouer.collidepoint(event.pos):
                    etat = "intro"

        elif event.type == pygame.KEYDOWN:
            # Echap ramène toujours au menu depuis les états credits et intro
            if event.key == pygame.K_ESCAPE and etat == "credits":
                etat = "menu"
            elif event.key == pygame.K_ESCAPE and etat == "intro":
                etat = "menu"
            # Espace depuis l'intro lance le choix d'équipe
            elif event.key == pygame.K_SPACE and etat == "intro":
                etat = "choix_equipe"

    # Fond affiché en permanence derrière tous les états
    screen.blit(fond, (0, 0))

    if etat == "menu":
        # Définition et affichage des trois boutons du menu principal
        bouton_jouer = pygame.Rect(100, 150, 260, 130)
        screen.blit(bouton_img, bouton_jouer)

        bouton_sauvegarde = pygame.Rect(100, 325, 260, 130)
        screen.blit(bouton_img, bouton_sauvegarde)

        bouton_credits = pygame.Rect(100, 500, 260, 130)
        screen.blit(bouton_img, bouton_credits)

        # Textes des boutons
        texte1 = font.render("NOUVELLE", True, "Black")
        texte5 = font.render("PARTIE", True, "Black")
        texte2 = font.render("SAUVEGARDE", True, "Black")
        texte3 = font.render("CREDITS", True, "Black")

        # Titre du jeu affiché en grand sur la droite
        texte4a = font_titre.render("PARIS", True, "White")
        texte4b = font_titre.render("BY", True, "White")
        texte4c = font_titre.render("NIGHT", True, "White")

        screen.blit(texte1, (160, 175))
        screen.blit(texte5, (177, 205))
        screen.blit(texte2, (136, 365))
        screen.blit(texte3, (166, 540))
        screen.blit(texte4a, (400, 150))
        screen.blit(texte4b, (530, 320))
        screen.blit(texte4c, (400, 500))

    elif etat == "credits":
        # Délègue l'affichage des crédits au module credits
        credits.afficher_credits(screen, font)

    elif etat == "sauvegarde":
        # Affiche le menu de sauvegarde et récupère le résultat
        # retourne "menu" si le joueur annule, ou ("charger", slot, save_data) s'il charge une partie
        resultat = sauvegarde.afficher_sauvegarde(screen, font)
        if resultat == "menu":
            etat = "menu"
        elif isinstance(resultat, tuple) and resultat[0] == "charger":
            _, slot, save_data = resultat
            save_a_charger = save_data  # on stocke les données pour les passer à jouer.lancer()
            etat = "jouer"

    elif etat == "choix_equipe":
        # Affiche le menu de sélection d'équipe
        # retourne la liste des clés des personnages choisis, ou None si le joueur annule
        equipe_choisie = menu_equipe.afficher_menu_equipe(screen)
        if equipe_choisie is None:
            etat = "menu"
        else:
            etat = "jouer"

    elif etat == "jouer":
        # Lance la boucle de jeu principale et attend son résultat
        # retourne "menu" si le joueur quitte, "sauvegarde" s'il veut gérer ses sauvegardes
        resultat = jouer.lancer(screen, font, save_a_charger, equipe_choisie)
        save_a_charger = None   # on remet à None après usage pour éviter de recharger la même save
        equipe_choisie = None
        if resultat == "menu":
            etat = "menu"
        elif resultat == "sauvegarde":
            etat = "sauvegarde"

    elif etat == "intro":
        # Écran d'introduction avec le texte de lore du jeu
        screen.fill((10, 8, 20))
        if not son_lance:
            # On joue le son d'intro une seule fois grâce au flag son_lance
            son.play()
            son_lance = True

        lignes = [
            "Paris, By Night.",
            "En dessous des rues paisibles de la capitale",
            "vous vous êtes égarés dans les catacombes.",
            "Des créatures y rodent, attirées par une magie oubliée.",
            "avec votre équipe descendez dans les profondeurs",
            "pour retrouver la source du mal.",
            "",
            "Appuyez sur ESPACE pour commencer."
        ]

        # Affichage ligne par ligne avec un espacement vertical de 45px
        y = 140
        for ligne in lignes:
            texte = font.render(ligne, True, (230, 220, 190))
            screen.blit(texte, (30, y))
            y += 45

    # Conversion du bouton en format alpha pour la transparence
    bouton_img = bouton_img.convert_alpha()

    pygame.display.update()

    if event.type == pygame.QUIT:
        running = False
        pygame.quit()
