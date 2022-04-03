import pygame
from settings import *
from support import *
from random import choice, randint
from tile import Tile
from player import Player
from ui import UI
from weapon import Weapon
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade


class Level:
    def __init__(self):
        self.gamePaused = False
        self.displaySurface = pygame.display.get_surface()
        self.visibleSprites = YSortCameraGroup()
        self.obstaclesSprites = pygame.sprite.Group()

        # attack sprites
        self.currentAttack = None
        self.attackSprites = pygame.sprite.Group()
        self.attackableSprites = pygame.sprite.Group()

        self.createMap()

        # user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # particles
        self.animationPlayer = AnimationPlayer()
        self.magicPlayer = MagicPlayer(self.animationPlayer)

    def createMap(self):
        layouts = {
            'bondary': importCsvLayout(resourcePath('src/map/mapFloorBlocks.csv')),
            'grass': importCsvLayout(resourcePath('src/map/mapGrass.csv')),
            'object': importCsvLayout(resourcePath('src/map/mapObjects.csv')),
            'entities': importCsvLayout(resourcePath('src/map/mapEntities.csv')),
        }
        graphics = {
            'grass': importImagesFrom(resourcePath('src/img/grass')),
            'objects': importImagesFrom(resourcePath('src/img/objects')),
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
                                (x, y),
                                [self.visibleSprites, self.obstaclesSprites,
                                    self.attackableSprites],
                                'grass',
                                randomGrassImg
                            )
                        if style == 'object':
                            surface = graphics['objects'][int(col)]
                            Tile(
                                (x, y),
                                [self.visibleSprites, self.obstaclesSprites],
                                'object',
                                surface
                            )
                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x, y),
                                    [self.visibleSprites],
                                    self.obstaclesSprites,
                                    self.createAttack,
                                    self.destroyAttack,
                                    self.createMagic
                                )
                            else:
                                if col == '390':
                                    enemyName = 'bamboo'
                                elif col == '391':
                                    enemyName = 'spirit'
                                elif col == '392':
                                    enemyName = 'raccoon'
                                else:
                                    enemyName = 'squid'

                                Enemy(
                                    enemyName,
                                    (x, y),
                                    [self.visibleSprites, self.attackableSprites],
                                    self.obstaclesSprites,
                                    self.damagePlayer,
                                    self.triggerDeathParticles,
                                    self.addXP
                                )

    def createAttack(self):
        self.currentAttack = Weapon(
            self.player,
            [self.visibleSprites, self.attackSprites]
        )

    def createMagic(self, name, strength, cost):
        if name == 'heal':
            self.magicPlayer.heal(self.player, strength,
                                  cost, [self.visibleSprites])
        if name == 'flame':
            self.magicPlayer.flame(self.player, strength, cost, [
                                   self.visibleSprites, self.attackSprites])

    def destroyAttack(self):
        if self.currentAttack:
            self.currentAttack.kill()
        self.currentAttack = None

    def playerAttackLogic(self):
        if self.attackSprites:
            for attackSprite in self.attackSprites:
                collisionSprites = pygame.sprite.spritecollide(
                    attackSprite,
                    self.attackableSprites,
                    False
                )
                if collisionSprites:
                    for targetSprite in collisionSprites:
                        if targetSprite.spriteType == 'grass':
                            position = targetSprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for _ in range(randint(3, 6)):
                                self.animationPlayer.createGrassParticles(
                                    position - offset,
                                    [self.visibleSprites]
                                )
                            targetSprite.kill()
                        else:
                            targetSprite.getDamage(
                                self.player,
                                attackSprite.spriteType
                            )

    def damagePlayer(self, ammount, attackType):
        if self.player.vulnerable:
            self.player.health -= ammount
            self.player.vulnerable = False
            self.player.hurtTime = pygame.time.get_ticks()
            self.animationPlayer.createParticles(
                attackType, self.player.rect.center, [self.visibleSprites]
            )

    def triggerDeathParticles(self, name, position):
        self.animationPlayer.createParticles(
            name, position, self.visibleSprites)

    def addXP(self, ammount):
        self.player.exp += ammount

    def toggleMenu(self):
        self.gamePaused = not self.gamePaused

    def run(self):
        self.visibleSprites.customDraw(self.player)
        self.ui.display(self.player)

        if self.gamePaused:
            self.upgrade.display()
        elif self.player.dead:
            self.ui.gameOver()
        else:
            self.visibleSprites.update()
            self.visibleSprites.enemyUpdate(self.player)
            self.playerAttackLogic()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.halfWidth = self.displaySurface.get_size()[0] // 2
        self.halfHeight = self.displaySurface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        assetUrl = resourcePath('src/img/tilemap/ground.png')
        self.floorSurface = pygame.image.load(assetUrl).convert()
        self.floorRect = self.floorSurface.get_rect(topleft=(0, 0))

    def customDraw(self, player):
        self.offset.x = player.rect.centerx - self.halfWidth
        self.offset.y = player.rect.centery - self.halfHeight

        floorOffsetPosition = self.floorRect.topleft - self.offset
        self.displaySurface.blit(self.floorSurface, floorOffsetPosition)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offsetPosition = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, offsetPosition)

    def enemyUpdate(self, player):
        enemySprites = [sprite for sprite in self.sprites() if hasattr(
            sprite, 'spriteType') and sprite.spriteType == 'enemy']
        for enemy in enemySprites:
            enemy.enemyUpdate(player)
