import pygame
pygame.init()

def afficher_credits(screen, font):

    screen.fill((0, 0, 0))

    credits = [ "LEGEND OF GRIMROCK",
                "", 
                "Par les développeurs :", 
                "leoti, Ian, Roxane er Lola", 
                "", 
                "Avec le parainage de :",
                "Guillaume et lounis",
                "", 
                "Afin de satisfaire les exigences démoniaques de :",
                "Monsieur Rossier", 
                "", 
                "Merci d'avoir joué !" ]

    y = 120

    for i, ligne in enumerate(credits):

        # couleur du titre
        if i == 0:
            couleur = (167, 119, 255)
        else:
            couleur = (255, 255, 255)

        texte = font.render(ligne, True, couleur)

        # centrage horizontal
        x = screen.get_width() // 2 - texte.get_width() // 2

        screen.blit(texte, (x, y))

        y += 50
