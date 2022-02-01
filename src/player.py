import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, obstaclesSprites):
        super().__init__(groups)
        self.image = pygame.image.load('./src/img/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.obstaclesSprites = obstaclesSprites

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed
        self.colission('horizontal')
        self.rect.y += self.direction.y * speed
        self.colission('vertical')

    def colission(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstaclesSprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstaclesSprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom

    def update(self):
        self.input()
        self.move(self.speed)