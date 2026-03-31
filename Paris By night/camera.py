import pygame
vec = pygame.math.Vector2
from abc import ABC, abstractmethod
 
width = 1080
height = 720
 
class Camera:
    def __init__(self, player):
        self.player = player
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)
        self.CONST = vec(-width/2 + player.rect.w/2, -height/2 + player.rect.h/2)
 
    def setmethod(self, method):
        self.method = method
 
    def scroll(self):
        self.method.scroll()
 
 
class CamScroll(ABC):
    def __init__(self, camera, player):
        self.camera = camera
        self.player = player
 
    @abstractmethod
    def scroll(self):
        pass
 
 
class Follow(CamScroll):
    def __init__(self, camera, player):
        super().__init__(camera, player)
 
    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x) / 20
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y) / 20
        self.camera.offset.x = int(self.camera.offset_float.x)
        self.camera.offset.y = int(self.camera.offset_float.y)
    
    def appliquer(self, position):
        return (int(position.x - self.camera.offset.x), 
                int(position.y - self.camera.offset.y))
    
class Border(CamScroll):
    def __init__(self, camera, player):
        super().__init__(camera, player)
 
    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x) / 20
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y) / 20
        self.camera.offset.x = int(self.camera.offset_float.x)
        self.camera.offset.y = int(self.camera.offset_float.y)
        # Bornes de la carte (3000 = largeur de ta map, à adapter)
        self.camera.offset.x = max(0, self.camera.offset.x)
        self.camera.offset.x = min(self.camera.offset.x, 3000 - width)
 
 
class Auto(CamScroll):
    def __init__(self, camera, player):
        super().__init__(camera, player)
 
    def scroll(self):
        self.camera.offset.x += 1
