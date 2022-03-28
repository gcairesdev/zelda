import pygame
from settings import *
from support import *
from random import choice
from tile import Tile
from player import Player
from weapon import Weapon


class Level:
    def __init__(self):
        self.displaySurface = pygame.display.get_surface()
        self.visibleSprites = YSortCameraGroup()
        self.obstaclesSprites = pygame.sprite.Group()

        # attack sprites
        self.currentAttack = None

        self.createMap()

    def createMap(self):
        layouts = {
            'bondary': importCsvLayout('./src/map/mapFloorBlocks.csv'),
            'grass': importCsvLayout('./src/map/mapGrass.csv'),
            'object': importCsvLayout('./src/map/mapObjects.csv'),
        }
        graphics = {
            'grass': importImagesFrom('./src/img/grass'),
            'objects': importImagesFrom('./src/img/objects'),
        }

        for style, layout in layouts.items():
            for rowIndex, row in enumerate(layout):
                for colIndex, col in enumerate(row):
                    if col != '0' and col != '':
                        x = colIndex * TILE_SIZE
                        y = rowIndex * TILE_SIZE
                        if style == 'bondary':
                            Tile((x, y), [self.obstaclesSprites], 'invisible')
                        if style == 'grass':
                            randomGrassImg = choice(graphics['grass'])
                            Tile(
                                (x, y), [self.visibleSprites, self.obstaclesSprites], 'grass', randomGrassImg)
                        if style == 'object':
                            surface = graphics['objects'][int(col)]
                            Tile(
                                (x, y), [self.visibleSprites, self.obstaclesSprites], 'object', surface)

        self.player = Player((2000, 1430), [
                             self.visibleSprites], self.obstaclesSprites, self.createAttack, self.destroyAttack)

    def createAttack(self):
        self.currentAttack = Weapon(self.player, [self.visibleSprites])

    def destroyAttack(self):
        if self.currentAttack:
            self.currentAttack.kill()
        self.currentAttack = None

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
        self.floorSurface = pygame.image.load(
            './src/img/tilemap/ground.png').convert()
        self.floorRect = self.floorSurface.get_rect(topleft=(0, 0))

    def customDraw(self, player):
        self.offset.x = player.rect.centerx - self.halfWidth
        self.offset.y = player.rect.centery - self.halfHeight

        floorOffsetPosition = self.floorRect.topleft - self.offset
        self.displaySurface.blit(self.floorSurface, floorOffsetPosition)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offsetPosition = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, offsetPosition)
