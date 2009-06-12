import pygame
from helpers import *

class Tile(pygame.sprite.Sprite):
    image = None
    imagefile = ''
    colorkey = None
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        if type(self).image is None: #first load
            type(self).image, type(self).rect = load_image(type(self).imagefile, type(self).colorkey)
        self.image = type(self).image
        self.rect = pygame.Rect(0,0,type(self).rect.width, type(self).rect.height)
        self.rect.center = (x,y)

class Wall(Tile):
    imagefile = 'wall.png'

class Exit(Tile):
    imagefile = 'exit.png'

class Coin(Tile):
    imagefile = 'coin.png'
    colorkey = -1
