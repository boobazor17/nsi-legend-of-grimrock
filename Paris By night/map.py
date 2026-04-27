import pygame
import pytmx
from Physique import Vase
import os 
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

    def load_map(self, path):
        chemin = os.path.join(os.path.dirname(__file__), path)
        tmx_data = pytmx.load_pygame(chemin, pixelalpha=True)
        self.tiles, self.collision_tiles, self.ennemis_to_spawn, \
        self.spawnpoint_joueur, self.objets_interactifs = create_map(tmx_data)
        self.list_object = self.collision_tiles + self.objets_interactifs # on garde les objets Tile entiers 
        for tile in self.tiles:
            tile.image = pygame.transform.scale(tile.image, (TILE_SIZE * SCALE, TILE_SIZE * SCALE))
            tile.rect = tile.image.get_rect(topleft=(tile.rect.x * SCALE, tile.rect.y * SCALE))
            tile.position = pygame.math.Vector2(tile.rect.topleft)


    def draw(self, screen, follow):
        for tile in self.tiles:
            pos = (tile.position.x - follow.camera.offset.x,
                   tile.position.y - follow.camera.offset.y)
            screen.blit(tile.image, pos)
            

def create_map(tmx_data):
    tiles = []
    collision_tiles = []
    ennemis_to_spawn = []
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
            else:
                tiles.append(Tile(pos_x, pos_y, image))

    objets_interactifs = []  # nouveau
    #  Object layers 
    for obj in tmx_data.objects:
        obj_type = obj.properties.get("obj_type")
        x = int(obj.x)
        y = int(obj.y)
        
        if obj_type == "vase":
            objets_interactifs.append(Vase(x * SCALE, y * SCALE))  #  Vase existant de Physique.py
        
        elif obj_type == "spawnpoint_joueur":
            spawnpoint_joueur = pygame.math.Vector2(x * SCALE, y * SCALE)
            print(f"Spawnpoint trouvé : {x * SCALE}, {y * SCALE}")

        elif obj_type == "ennemi":
            nom = obj.properties.get("nom", "ennemi1")
            ennemis_to_spawn.append({
                "nom": nom,
                "x": x * SCALE,
                "y": y * SCALE
            })

    return tiles, collision_tiles, ennemis_to_spawn, spawnpoint_joueur, objets_interactifs