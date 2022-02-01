import pygame
from settings import *
from tile import Tile

class Level:
    def __init__(self):
        self.displaySurface = pygame.display.get_surface()
        self.visibleSprites = pygame.sprite.Group()
        self.obstaclesSprites = pygame.sprite.Group()
        self.createMap()

    def createMap(self):
        for rowIndex, row in enumerate(WORLD_MAP):
            for colIndex, col in enumerate(row):
                x = colIndex * TILE_SIZE
                y = rowIndex * TILE_SIZE
                if col == 'x':
                    Tile((x, y), [self.visibleSprites, self.obstaclesSprites])

    def run(self):
        self.visibleSprites.draw(self.displaySurface)