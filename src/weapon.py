import pygame
from support import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.spriteType = 'weapon'
        direction = player.status.split('_')[0]

        # graphic
        fullPath = f'src/img/weapons/{player.weapon}/{direction}.png'
        assetUrl = resourcePath(fullPath)
        self.image = pygame.image.load(assetUrl).convert_alpha()

        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(
                midleft=player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(
                midright=player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(
                midtop=player.rect.midbottom + pygame.math.Vector2(0, 0))
        else:
            self.rect = self.image.get_rect(
                midbottom=player.rect.midtop + pygame.math.Vector2(-10, 0))
