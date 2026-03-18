import pygame
pygame.init()

# generer la fenetre du jeu 
pygame.display.set_caption("caca")
screen = pygame.display.set_mode((1080,720 ))

font = pygame.font.Font(None,40)
font_titre = pygame.font.Font(None,80)


running = True
while running == True:
    for event in pygame.event.get():
        screen.fill((201,158,89))

        # bouton
        bouton = pygame.Rect(440,200,200,50)
        pygame.draw.rect(screen,(139,94,44),bouton)
    
        bouton3 = pygame.Rect(440,300,200,50)
        pygame.draw.rect(screen,(139,94,44),bouton3)
    
        bouton2 = pygame.Rect(440,400,200,50)
        pygame.draw.rect(screen,(139,94,44),bouton2)
    
        texte1 = font.render("Jouer", True, (245,240,220))
        texte2 = font.render("Sauvegarde", True, (245,240,220))
        texte3 = font.render("Credits", True, (245,240,220))
        texte4 = font_titre.render("Paris By Night", True, (245,240,220))

        screen.blit(texte1,(503,210))
        screen.blit(texte2,(460,310))
        screen.blit(texte3,(492,410))
        screen.blit(texte4,(355,10))

    

        # mettre à jour l'écran
        pygame.display.update()

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
f





