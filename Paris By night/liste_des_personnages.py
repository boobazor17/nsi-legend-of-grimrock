#liste des personnages

fantome_perso1 = {
    "nom": "Fantôme du métro",
    "pv": 100,
    "attaque": 20
}
rat_perso2 = {
    "nom": "Rat des égoûts",
    "pv": 100,
    "attaque": 20
}
pigeon_perso3 = {
    "nom": "Pigeon parisien",
    "pv": 100,
    "attaque": 20
}
_perso4 = {
    "nom": " ??? ",
    "pv": 100,
    "attaque": 20
}

personnages_disponibles = [
    {"nom": "Fantôme du métro", "pv": 100, "attaque": 20},
    {"nom": "Rat des égoûts", "pv": 100, "attaque": 20},
    {"nom": "Pigeon parisien", "pv": 100, "attaque": 20},
    {"nom": " ??? ", "pv": 100, "attaque": 20}
]

equipe = []

for i in range(4):  # pour des équipes de 4
    print("Choisis un personnage :")
    
    for index, perso in enumerate(personnages_disponibles):
        print(index, "-", perso["nom"])     #choisir le perso avec son nom et un chiffre l'index
    
    choix = int(input("Numéro du personnage : ")) #rentrer le numéro donc l'index
    
    equipe.append(personnages_disponibles[choix])

print("Ton équipe est composée de :")
for perso in equipe:
    print(perso["nom"], "-", perso["pv"], "PV") #affiche les infos du perso

if personnages_disponibles[choix] not in equipe:  #pour éviter que un personnage soit choisi plusieurs fois par erreur
    equipe.append(personnages_disponibles[choix])
else:
    print("Déjà choisi !")



