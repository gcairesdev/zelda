import pygame
from settings import *
from support import *
from entity import Entity


class Enemy(Entity):
    def __init__(self, enemyName, position, groups, obstaclesSprites):
        # general setup
        super().__init__(groups)
        self.spriteType = 'enemy'

        # graphics setup
        self.importGraphics(enemyName)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frameIndex]

        # movement
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstaclesSprites = obstaclesSprites

        # stats
        self.enemyName = enemyName
        enemyInfo = ENEMY_DATA[self.enemyName]
        self.health = enemyInfo['health']
        self.exp = enemyInfo['exp']
        self.speed = enemyInfo['speed']
        self.resistance = enemyInfo['resistance']
        self.attackType = enemyInfo['attackType']
        self.attackDamage = enemyInfo['damage']
        self.attackRadius = enemyInfo['attackRadius']
        self.noticeRadius = enemyInfo['noticeRadius']

        # player interaction
        self.canAttack = True
        self.attackTime = None
        self.attackCooldown = 400

        # invencibility timer
        self.vunarable = True
        self.hitTime = None
        self.invencibilityCooldown = 300

    def importGraphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        mainPath = f'./src/img/enemies/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = importImagesFrom(mainPath + animation)

    def getPlayerDistanceAndDirection(self, player):
        enemyVector = pygame.math.Vector2(self.rect.center)
        PlayerVector = pygame.math.Vector2(player.rect.center)
        distance = (PlayerVector - enemyVector).magnitude()

        if distance > 0:
            direction = (PlayerVector - enemyVector).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def getStatus(self, player):
        distance = self.getPlayerDistanceAndDirection(player)[0]

        if distance <= self.attackRadius and self.canAttack:
            if self.status != 'attack':
                self.frameIndex = 0
            self.status = 'attack'
        elif distance <= self.noticeRadius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attackTime = pygame.time.get_ticks()
        elif self.status == 'move':
            self.direction = self.getPlayerDistanceAndDirection(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animation):
            if self.status == 'attack':
                self.canAttack = False
            self.frameIndex = 0

        self.image = animation[int(self.frameIndex)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vunarable:
            alpha = self.waveValue()
        else:
            alpha = 255
        self.image.set_alpha(alpha)


    def cooldowns(self):
        currentTime = pygame.time.get_ticks()

        if not self.canAttack:
            if currentTime - self.attackTime >= self.attackCooldown:
                self.canAttack = True

        if not self.vunarable:
            if currentTime - self.hitTime >= self.invencibilityCooldown:
                self.vunarable = True

    def getDamage(self, player, attackType):
        if self.vunarable:
            self.direction = self.getPlayerDistanceAndDirection(player)[1]
            if attackType == 'weapon':
                self.health -= player.getFullWeaponDamage()
            else:
                # magic damage
                pass
            self.hitTime = pygame.time.get_ticks()
            self.vunarable = False

        self.checkDeath()

    def checkDeath(self):
        if self.health <= 0:
            self.kill()

    def hitReaction(self):
        if not self.vunarable:
            self.direction *= -self.resistance

    def update(self):
        self.hitReaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()

    def enemyUpdate(self, player):
        self.getStatus(player)
        self.actions(player)
