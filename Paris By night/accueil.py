import pygame
pygame.init()
import credits
import sauvegarde
import jouer
import assetss

# generer la fenetre du jeu 
pygame.display.set_caption("caca")
screen = pygame.display.set_mode((1080,720 ))

# mettre le fond
fond = pygame.image.load("assets/fond.png")
fond = pygame.transform.scale(fond, (1080, 720))

# insérer les boutons
bouton_img = pygame.image.load("assets/bouton.png")
bouton_img = pygame.transform.scale(bouton_img, (260, 130))

font = pygame.font.Font(None,40)
font_titre = pygame.font.Font(None,220)
images = assetss.charger_images()  


etat = "menu"
running = True
save_a_charger = None 

while running == True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if etat == "menu":
                if bouton_credits.collidepoint(event.pos):
                    etat = "credits"
                elif bouton_sauvegarde.collidepoint(event.pos):
                    etat = "sauvegarde"
                elif bouton_jouer.collidepoint(event.pos):
                    etat = "jouer"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and etat == "credits":
                etat = "menu"

    screen.blit(fond, (0, 0))
    if etat == "menu":
                    # bouton
                    bouton_jouer = pygame.Rect(100,150,260,130)
                    screen.blit(bouton_img, bouton_jouer)
                
                    bouton_sauvegarde = pygame.Rect(100,325,260,130)
                    screen.blit(bouton_img, bouton_sauvegarde)
                
                    bouton_credits = pygame.Rect(100,500,260,130)
                    screen.blit(bouton_img, bouton_credits)
                
                    texte1 = font.render("NOUVELLE", True, ('Black'))
                    texte5 = font.render("PARTIE", True, ('Black'))
                    texte2 = font.render("SAUVEGARDE", True, ('Black'))
                    texte3 = font.render("CREDITS", True, ('Black'))
                    texte4a = font_titre.render("PARIS", True, ("White"))
                    texte4b = font_titre.render("BY", True, ("White"))
                    texte4c = font_titre.render("NIGHT", True, ("White"))
                    
                    
                    screen.blit(texte1,(160,175))
                    screen.blit(texte5, (177, 205))
                    screen.blit(texte2,(136,365))
                    screen.blit(texte3,(166,540))
                    screen.blit(texte4a, (400, 150))
                    screen.blit(texte4b, (530, 320))
                    screen.blit(texte4c, (400, 500))
                                        
    elif etat == "credits":
        credits.afficher_credits(screen, font)
                        
    elif etat == "sauvegarde":                             
        resultat = sauvegarde.afficher_sauvegarde(screen, font)
        if resultat == "menu":
            etat = "menu"    
        elif isinstance(resultat, tuple) and resultat[0] == "charger":
            _, slot, save_data = resultat
            save_a_charger = save_data
            etat = "jouer"

    elif etat == "jouer":
        resultat = jouer.lancer(screen, font, save_a_charger)
        save_a_charger = None
        if resultat == "menu":
            etat = "menu"
        elif resultat == "sauvegarde":  
            etat = "sauvegarde"
        
       
    if etat == "credits" or etat == "sauvegarde":
        if event.type == pygame.QUIT:
                etat = "menu"

    bouton_img = bouton_img.convert_alpha()
            
    # mettre à jour l'écran
    pygame.display.update()

    if event.type == pygame.QUIT:
        running = False
        pygame.quit()
