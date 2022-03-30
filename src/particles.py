import pygame
from support import importImagesFrom
from random import choice


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic
            'flame': importImagesFrom('./src/img/particles/flame/frames'),
            'aura': importImagesFrom('./src/img/particles/aura'),
            'heal': importImagesFrom('./src/img/particles/heal/frames'),

            # attacks
            'claw': importImagesFrom('./src/img/particles/claw'),
            'slash': importImagesFrom('./src/img/particles/slash'),
            'sparkle': importImagesFrom('./src/img/particles/sparkle'),
            'leaf_attack': importImagesFrom('./src/img/particles/leaf_attack'),
            'thunder': importImagesFrom('./src/img/particles/thunder'),

            # monster deaths
            'squid': importImagesFrom('./src/img/particles/smoke_orange'),
            'raccoon': importImagesFrom('./src/img/particles/raccoon'),
            'spirit': importImagesFrom('./src/img/particles/nova'),
            'bamboo': importImagesFrom('./src/img/particles/bamboo'),

            # leafs
            'leaf': (
                importImagesFrom('./src/img/particles/leaf1'),
                importImagesFrom('./src/img/particles/leaf2'),
                importImagesFrom('./src/img/particles/leaf3'),
                importImagesFrom('./src/img/particles/leaf4'),
                importImagesFrom('./src/img/particles/leaf5'),
                importImagesFrom('./src/img/particles/leaf6'),
                self.flipFrames(importImagesFrom(
                    './src/img/particles/leaf1')
                ),
                self.flipFrames(importImagesFrom(
                    './src/img/particles/leaf2')
                ),
                self.flipFrames(importImagesFrom(
                    './src/img/particles/leaf3')
                ),
                self.flipFrames(importImagesFrom(
                    './src/img/particles/leaf4')
                ),
                self.flipFrames(importImagesFrom(
                    './src/img/particles/leaf5')
                ),
                self.flipFrames(importImagesFrom(
                    './src/img/particles/leaf6'))
            )
        }

    def flipFrames(self, frames):
        flippedFrames = []
        for frame in frames:
            flippedFrame = pygame.transform.flip(frame, True, False)
            flippedFrames.append(flippedFrame)
        return flippedFrames

    def createGrassParticles(self, position, groups):
        animationFrames = choice(self.frames['leaf'])
        ParticleEffect(position, animationFrames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, position, animationFrames, groups):
        super().__init__(groups)
        self.frameIndex = 0
        self.animationSpeed = 0.35
        self.frames = animationFrames
        self.image = self.frames[self.frameIndex]
        self.rect = self.image.get_rect(center=position)

    def animate(self):
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frameIndex)]

    def update(self):
        self.animate()
