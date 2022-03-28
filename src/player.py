import pygame
from support import *
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, obstaclesSprites, createAttack, destroyAttack, createMagic):
        super().__init__(groups)
        self.image = pygame.image.load('./src/img/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -26)
        self.importPlayerAssets()
        self.status = 'down'
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attackCooldown = 400
        self.atackTime = None
        self.obstaclesSprites = obstaclesSprites

        # weapon
        self.createAttack = createAttack
        self.destroyAttack = destroyAttack
        self.weaponIndex = 0
        self.weapon = list(WEAPON_DATA.keys())[self.weaponIndex]
        self.canSwitchWeapon = True
        self.weaponSwitchTime = None
        self.switchDurationCooldown = 200

        # magic
        self.createMagic = createMagic
        self.magicIndex = 0
        self.magic = list(MAGIC_DATA.keys())[self.magicIndex]
        self.canSwitchMagic = True
        self.magicSwitchTime = None

        # stats
        self.stats = {
            'health': 100,
            'energy': 60,
            'attack': 10,
            'magic': 4,
            'speed': 5
        }
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.exp = 123

    def importPlayerAssets(self):
        characterPath = './src/img/player/'
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
            'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []
        }

        for animation in self.animations.keys():
            fullPath = characterPath + animation
            self.animations[animation] = importImagesFrom(fullPath)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            # weapon input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.atackTime = pygame.time.get_ticks()
                self.createAttack()

            # magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.atackTime = pygame.time.get_ticks()
                style = list(MAGIC_DATA.keys())[self.magicIndex]
                strength = list(MAGIC_DATA.values())[
                    self.magicIndex]['strength'] + self.stats['magic']
                cost = list(MAGIC_DATA.values())[self.magicIndex]['cost']
                self.createMagic(style, strength, cost)

            if keys[pygame.K_q] and self.canSwitchWeapon:
                self.canSwitchWeapon = False
                self.weaponSwitchTime = pygame.time.get_ticks()

                if self.weaponIndex < len(list(WEAPON_DATA.keys())) - 1:
                    self.weaponIndex += 1
                else:
                    self.weaponIndex = 0

                self.weapon = list(WEAPON_DATA.keys())[self.weaponIndex]

            if keys[pygame.K_e] and self.canSwitchMagic:
                self.canSwitchMagic = False
                self.magicSwitchTime = pygame.time.get_ticks()

                if self.magicIndex < len(list(MAGIC_DATA.keys())) - 1:
                    self.magicIndex += 1
                else:
                    self.magicIndex = 0

                self.magic = list(MAGIC_DATA.keys())[self.magicIndex]

    def setStatus(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.colission('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.colission('vertical')
        self.rect.center = self.hitbox.center

    def colission(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstaclesSprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstaclesSprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        currentTime = pygame.time.get_ticks()
        if self.attacking:
            if currentTime - self.atackTime >= self.attackCooldown:
                self.attacking = False
                self.destroyAttack()

        if not self.canSwitchWeapon:
            if currentTime - self.weaponSwitchTime >= self.switchDurationCooldown:
                self.canSwitchWeapon = True

        if not self.canSwitchMagic:
            if currentTime - self.magicSwitchTime >= self.switchDurationCooldown:
                self.canSwitchMagic = True

    def animate(self):
        animation = self.animations[self.status]

        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animation):
            self.frameIndex = 0

        self.image = animation[int(self.frameIndex)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.setStatus()
        self.animate()
        self.move(self.speed)
