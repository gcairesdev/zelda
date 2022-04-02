import pygame
from settings import *
from random import randint


class MagicPlayer():
    def __init__(self, animationPlayer):
        self.animationPlayer = animationPlayer
        self.sounds = {
            'heal': pygame.mixer.Sound('./src/audio/heal.wav'),
            'flame': pygame.mixer.Sound('./src/audio/flame.wav')
        }

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost and player.health < player.stats['health']:
            self.sounds['heal'].set_volume(0.2)
            self.sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            if player.health > player.stats['health']:
                player.health = player.stats['health']
            offset = pygame.math.Vector2(0, 60)
            self.animationPlayer.createParticles('heal', player.rect.center - offset, groups, 0.24)
            self.animationPlayer.createParticles('aura', player.rect.center, groups, 0.24)

    def flame(self, player, strength, cost, groups):
        if player.energy >= cost:
            self.sounds['flame'].set_volume(0.2)
            self.sounds['flame'].play()
            player.energy -= cost

            playerDirection = player.status.split('_')[0]
            if playerDirection == 'up':
                playerDirection = pygame.math.Vector2(0, -1)
            if playerDirection == 'down':
                playerDirection = pygame.math.Vector2(0, 1)
            if playerDirection == 'left':
                playerDirection = pygame.math.Vector2(-1, 0)
            if playerDirection == 'right':
                playerDirection = pygame.math.Vector2(1, 0)

            for i in range(1, 6):
                randomized = randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                if playerDirection.x:
                    offset = playerDirection.x * i * TILE_SIZE
                    x = player.rect.centerx + offset + randomized
                    y = player.rect.centery + randomized
                if playerDirection.y:
                    offset = playerDirection.y * i * TILE_SIZE
                    x = player.rect.centerx + randomized
                    y = player.rect.centery + offset + randomized
                self.animationPlayer.createParticles('flame', (x, y), groups, 0.24)