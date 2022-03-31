import pygame
from settings import *


class MagicPlayer():
    def __init__(self, animationPlayer):
        self.animationPlayer = animationPlayer

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost and player.health < player.stats['health']:
            player.health += strength
            player.energy -= cost
            if player.health > player.stats['health']:
                player.health = player.stats['health']
            offset = pygame.math.Vector2(0, 60)
            self.animationPlayer.createParticles('heal', player.rect.center - offset, groups, 0.24)
            self.animationPlayer.createParticles('aura', player.rect.center, groups, 0.24)