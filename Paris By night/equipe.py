import pygame
pygame.init()

class equipe :
    def __init__(self,x,y,nom,pv,pvmax,attaque,distance_attaque):
                self.position = pygame.math.Vector2(x,y)
                self.nom = nom
                self.pv = pv
                self.pvmax = pvmax
                self.attaque = attaque
                self.distance_attaque = distance_attaque
                


    taille_equipe = 4

    """ def personnage():
     for i in range(4):  # pour des équipes de 4
        print("Choisis un personnage :")
        
        for index, perso in enumerate():
            print(index, "-", perso["nom"])     #choisir le perso avec son nom et un chiffre l'index
        
        choix = int(input("Numéro du personnage : ")) #rentrer le numéro donc l'index
        
        equipe.append([choix])

    print("Ton équipe est composée de :")
    for perso in equipe:
        print(perso["nom"], "-", perso["pv"], "PV") #affiche les infos du perso

    if [choix] not in equipe:  #pour éviter que un personnage soit choisi plusieurs fois par erreur
        equipe.append([choix])
    else:
        print("Déjà choisi !") """
    
    def changer_equipe(taille_equipe,liste_ts,liste_equipe):
            pass


fantome_perso1 = equipe(0,0,"fantome",100,100,20,100)
                
rat_perso2 =  equipe(0,0,"rat", 100, 20,20,20)
                
pigeon_perso3 = equipe(0,0,"nom",100,20,20,20)
            
perso4 = equipe(0,0,"nom", 100, 20,20,20)

liste_ts = [fantome_perso1,rat_perso2,pigeon_perso3,perso4 ]


                