import pygame
pygame.init()
import credits
import sauvegarde
import jouer
import assetss

# generer la fenetre du jeu 
pygame.display.set_caption("caca")
screen = pygame.display.set_mode((1080,720 ))

font = pygame.font.Font(None,40)
font_titre = pygame.font.Font(None,220)

images = assetss.charger_images()  
tower_img = images["tower"] 

etat = "menu"
running = True
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

    screen.fill(("Midnightblue"))
    if etat == "menu":
                    # bouton
                    bouton_jouer = pygame.Rect(100,150,260,130)
                    pygame.draw.rect(screen,("gold"),bouton_jouer)
                    pygame.draw.rect(screen, ("goldenrod"), bouton_jouer, 14)
                
                    bouton_sauvegarde = pygame.Rect(100,325,260,130)
                    pygame.draw.rect(screen,("gold"),bouton_sauvegarde)
                    pygame.draw.rect(screen, ("goldenrod"), bouton_sauvegarde, 14)
                
                    bouton_credits = pygame.Rect(100,500,260,130)
                    pygame.draw.rect(screen,("gold"),bouton_credits)
                    pygame.draw.rect(screen, ("goldenrod"), bouton_credits, 14)
                
                    texte1 = font.render("JOUER", True, ('MidnightBlue'))
                    texte2 = font.render("SAUVEGARDE", True, ('MidnightBlue'))
                    texte3 = font.render("CREDITS", True, ('MidnightBlue'))
                    texte4a = font_titre.render("PARIS", True, ("lightsteelblue"))
                    texte4b = font_titre.render("BY", True, ("lightsteelblue"))
                    texte4c = font_titre.render("NIGHT", True, ("lightsteelblue"))
                    
                    screen.blit(tower_img, (380, 10))
                    
                    screen.blit(texte1,(185,200))
                    screen.blit(texte2,(136,380))
                    screen.blit(texte3,(173,555))
                    screen.blit(texte4a, (400, 150))
                    screen.blit(texte4b, (530, 320))
                    screen.blit(texte4c, (400, 500))
                                        
    elif etat == "credits":
        credits.afficher_credits(screen, font)
        
        
                        
    elif etat == "sauvegarde":                             
        resultat = sauvegarde.afficher_sauvegarde(screen, font)
        if resultat == "menu":
            etat = "menu"    

    elif etat == "jouer":
        resultat = jouer.lancer(screen, font)
        if resultat == "menu":
            etat = "menu"
        elif resultat == "sauvegarde":  
            etat = "sauvegarde"
        
       
    if etat == "credits" or etat == "sauvegarde":
        if event.type == pygame.QUIT:
                etat = "menu"
            
    # mettre à jour l'écran
    pygame.display.update()

    if event.type == pygame.QUIT:
        running = False
        pygame.quit()
