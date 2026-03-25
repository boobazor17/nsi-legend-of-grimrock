import pygame
pygame.init()
import credits
import sauvegarde
import jouer

# generer la fenetre du jeu 
pygame.display.set_caption("caca")
screen = pygame.display.set_mode((1080,720 ))

font = pygame.font.Font(None,40)
font_titre = pygame.font.Font(None,80)

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

    screen.fill((201,158,89))
    if etat == "menu":
                    # bouton
                    bouton_jouer = pygame.Rect(440,200,200,50)
                    pygame.draw.rect(screen,(139,94,44),bouton_jouer)
                
                    bouton_sauvegarde = pygame.Rect(440,300,200,50)
                    pygame.draw.rect(screen,(139,94,44),bouton_sauvegarde)
                
                    bouton_credits = pygame.Rect(440,400,200,50)
                    pygame.draw.rect(screen,(139,94,44),bouton_credits)
                
                    screen.blit(font.render("Jouer",      True, (245, 240, 220)), (503, 210))
                    screen.blit(font.render("Sauvegarde", True, (245, 240, 220)), (460, 310))
                    screen.blit(font.render("Credits",    True, (245, 240, 220)), (492, 410))
                    screen.blit(font_titre.render("Paris By Night", True, (245, 240, 220)), (355, 10))
                                        
    elif etat == "credits":
        credits.afficher_credits(screen, font)
                        
    elif etat == "sauvegarde":
        sauvegarde.afficher_sauvegarde(screen, font)

    elif etat == "jouer":
        jouer.lancer()


            

    # mettre à jour l'écran
    pygame.display.update()

    if event.type == pygame.QUIT:
        running = False
        pygame.quit()
