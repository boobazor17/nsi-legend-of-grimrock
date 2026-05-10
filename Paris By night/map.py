import pygame
import pytmx
from Boutique import Coffre
from Physique import Vase, Porte_normale, Porte_plaque, Porte_clé, item, item_consommable, item_objet, item_equipement
import os 
from Boutique import Coffre
pygame.init()

TILE_SIZE = 16
SCALE = 3  # multiplie la taille des tuiles par 3
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.position = pygame.math.Vector2(x, y)

class CollisionTile(Tile):
    """Tuile solide qui bloque le joueur"""
    pass

class Map_Manager:
    def __init__(self):
        self.tiles = []
        self.collision_tiles = []
        self.list_object = []  # compatible avec le système de collisions
        self.ennemis_to_spawn = []
        self.spawnpoint_joueur = pygame.math.Vector2(0, 0)
        self.transitions = []
        self.vide_tiles = []


    def load_map(self, path):
        chemin = os.path.join(os.path.dirname(__file__), path)
        tmx_data = pytmx.load_pygame(chemin, pixelalpha=True)
        self.tiles, self.collision_tiles, self.ennemis_to_spawn, \
        self.spawnpoint_joueur, self.objets_interactifs, self.obj_porte, self.plaques, self.transitions, self.vide_tiles= create_map(tmx_data)
        self.list_object = self.collision_tiles + self.objets_interactifs + self.obj_porte # on garde les objets Tile entiers 
        for tile in self.tiles:
            tile.image = pygame.transform.scale(tile.image, (TILE_SIZE * SCALE, TILE_SIZE * SCALE))
            tile.rect = tile.image.get_rect(topleft=(tile.rect.x * SCALE, tile.rect.y * SCALE))
            tile.position = pygame.math.Vector2(tile.rect.topleft)


    def draw(self, screen, follow):
        for tile in self.tiles:
            pos = (tile.position.x - follow.camera.offset.x,
                   tile.position.y - follow.camera.offset.y)
            screen.blit(tile.image, pos)

CLASSES_PORTES = {
    "porte": Porte_normale,
    "porte_cle": Porte_clé,
}         
def creer_item_depuis_nom(nom):
    if nom == "potion_vie":
        return item_consommable("potion de soin", 50, 50, 20, (255, 0, 255), "assets/potion_vie.png")
    elif nom == "potion_degat":
        return item_consommable("potion de dégats", 50, 50, -20, (255, 0, 255), "assets/potion_degat.png")
    elif nom == "cle":
        return item_objet("clé", 50, 50, 0, (255, 255, 0), "assets/cle.png")
    elif nom == "cailloux":
        return item_objet("caillou", 50, 50, 0, (100, 100, 100), "assets/cailloux.png")
    elif nom == "epee":
        return item_equipement("épée", 50, 50, (150, 150, 150), "assets/épée.png", "arme", bonus_attaque=10)
    elif nom == "rune_degat":
        return item_equipement("rune de dégats", 50, 50, (255, 0, 0), "assets/rune_degat.png", "rune", bonus_attaque=5)
    elif nom == "rune_vie":
        return item_equipement("rune de vie", 50, 50, (0, 255, 0), "assets/rune_vie.png", "rune", bonus_pv=20)
    elif nom == "rune_mana":
        return item_equipement("rune de mana", 50, 50, (0, 0, 255), "assets/rune_mana.png", "rune", bonus_mana=20)
    return None

def create_map(tmx_data):
    tiles = []
    collision_tiles = []
    ennemis_to_spawn = []
    vide_tiles = []
    spawnpoint_joueur = pygame.math.Vector2(0, 0)

    # Tile layers 
    for layer in tmx_data.visible_layers:
        if not hasattr(layer, 'data'):
            continue
        for x, y, gid in layer:
            if gid == 0:
                continue
            props = tmx_data.get_tile_properties_by_gid(gid)
            image = tmx_data.get_tile_image_by_gid(gid)
            if image is None:
                continue

            pos_x = x * TILE_SIZE
            pos_y = y * TILE_SIZE
            tile_type = props.get("type") if props else None

            if tile_type == "mur":
                t = CollisionTile(pos_x, pos_y, image)
                tiles.append(t)
                collision_tiles.append(t)
            if tile_type == "vide":
                    t = Tile(pos_x, pos_y, image)
                    tiles.append(t)
                    vide_tiles.append(t)
            else:
                tiles.append(Tile(pos_x, pos_y, image))

    objets_interactifs = []  # nouveau
    transitions = []
    objet_porte =["porte","porte_cle"] # liste des types de portes 
    obj_porte =[]
    plaques ={} 
    portes_plaques_en_attente = [] # on créé une liste pour stocker les portes plaques en attente de leur plaque associée car sinon on risque de ne pas trouver la plaque associée si elle est définie après la porte 
    #  Object layers 
    types_ennemis =["ennemi1","araignee","necromancien", "sanglichon","bat"]
    for obj in tmx_data.objects:
        obj_type = obj.properties.get("obj_type")
        x = int(obj.x)
        y = int(obj.y)
        
        if obj_type == "vase":
            contenu_texte = obj.properties.get("contenu", "")
            contenu = []

            for nom_item in contenu_texte.split(","):
                nom_item = nom_item.strip()
                nouvel_item = creer_item_depuis_nom(nom_item)
                if nouvel_item is not None:
                    contenu.append(nouvel_item)
            objets_interactifs.append(Vase(x * SCALE, y * SCALE, contenu))  #  Vase existant de Physique.py
        
        elif obj_type == "spawnpoint_joueur":
            spawnpoint_joueur = pygame.math.Vector2(x * SCALE, y * SCALE)
            print(f"Spawnpoint trouvé : {x * SCALE}, {y * SCALE}")

        elif obj_type in types_ennemis:
            ennemis_to_spawn.append({
        "nom": obj_type,  # le nom c'est simplement obj_type
        "x": x * SCALE,
        "y": y * SCALE,
        })
        elif obj_type == "coffre":
            objets_interactifs.append(Coffre(x * SCALE, y * SCALE))  # Coffre à implémenter dans Boutique.py

        elif obj_type in objet_porte:
            classe = CLASSES_PORTES.get(obj_type)
            if classe:
                obj_porte.append(classe(x * SCALE, y * SCALE))

        elif obj_type == "plaque":
            nom = obj.properties.get("nom")
            plaques[nom] = (x * SCALE, y * SCALE)
            print("plaque trouvée :", nom)

        elif obj_type == "porte_plaque":
            nom = obj.properties.get("nom")
            portes_plaques_en_attente.append((nom, x * SCALE, y * SCALE))
        
        elif obj_type == "changement_map":
            transitions.append({
                "rect": pygame.Rect(x * SCALE, y * SCALE, int(obj.width) * SCALE, int(obj.height) * SCALE),
                "map": obj.properties.get("map")
            })



    for nom, x_porte, y_porte in portes_plaques_en_attente:
            if nom in plaques:
                x_plaque, y_plaque = plaques[nom]
                obj_porte.append(Porte_plaque(x_porte, y_porte, x_plaque, y_plaque))

        
            

    return tiles, collision_tiles, ennemis_to_spawn, spawnpoint_joueur, objets_interactifs, obj_porte, plaques, transitions, vide_tiles

