import pygame
from settings import *
from support import *
from tile import Tile
from player import Player

class Level:
    def __init__(self):
        self.displaySurface = pygame.display.get_surface()
        self.visibleSprites = YSortCameraGroup()
        self.obstaclesSprites = pygame.sprite.Group()
        self.createMap()

    def createMap(self):
        layouts = {
            'bondary': importCsvLayout('./src/map/mapFloorBlocks.csv'),
        }

        for style, layout in layouts.items():
            for rowIndex, row in enumerate(layout):
                for colIndex, col in enumerate(row):
                    if col != '-1':
                        x = colIndex * TILE_SIZE
                        y = rowIndex * TILE_SIZE
                        if style == 'bondary':
                            Tile((x, y), [self.obstaclesSprites], 'invisible')

        self.player = Player((2000, 1430), [self.visibleSprites], self.obstaclesSprites)


    def run(self):
        self.visibleSprites.customDraw(self.player)
        self.visibleSprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.halfWidth = self.displaySurface.get_size()[0] // 2
        self.halfHeight = self.displaySurface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.floorSurface = pygame.image.load('./src/img/tilemap/ground.png').convert()
        self.floorRect = self.floorSurface.get_rect(topleft = (0, 0))

    def customDraw(self, player):
        self.offset.x = player.rect.centerx - self.halfWidth
        self.offset.y = player.rect.centery - self.halfHeight

        floorOffsetPosition = self.floorRect.topleft - self.offset
        self.displaySurface.blit(self.floorSurface, floorOffsetPosition)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offsetPosition = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, offsetPosition)