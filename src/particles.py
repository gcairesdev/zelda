import pygame
from support import *
from random import choice


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic
            'flame': importImagesFrom(resourcePath('src/img/particles/flame/frames')),
            'aura': importImagesFrom(resourcePath('src/img/particles/aura')),
            'heal': importImagesFrom(resourcePath('src/img/particles/heal/frames')),

            # attacks
            'claw': importImagesFrom(resourcePath('src/img/particles/claw')),
            'slash': importImagesFrom(resourcePath('src/img/particles/slash')),
            'sparkle': importImagesFrom(resourcePath('src/img/particles/sparkle')),
            'leaf_attack': importImagesFrom(resourcePath('src/img/particles/leaf_attack')),
            'thunder': importImagesFrom(resourcePath('src/img/particles/thunder')),

            # monster deaths
            'squid': importImagesFrom(resourcePath('src/img/particles/smoke_orange')),
            'raccoon': importImagesFrom(resourcePath('src/img/particles/raccoon')),
            'spirit': importImagesFrom(resourcePath('src/img/particles/nova')),
            'bamboo': importImagesFrom(resourcePath('src/img/particles/bamboo')),

            # leafs
            'leaf': (
                importImagesFrom(resourcePath('src/img/particles/leaf1')),
                importImagesFrom(resourcePath('src/img/particles/leaf2')),
                importImagesFrom(resourcePath('src/img/particles/leaf3')),
                importImagesFrom(resourcePath('src/img/particles/leaf4')),
                importImagesFrom(resourcePath('src/img/particles/leaf5')),
                importImagesFrom(resourcePath('src/img/particles/leaf6')),
                self.flipFrames(importImagesFrom(
                    resourcePath('src/img/particles/leaf1'))
                ),
                self.flipFrames(importImagesFrom(
                    resourcePath('src/img/particles/leaf2'))
                ),
                self.flipFrames(importImagesFrom(
                    resourcePath('src/img/particles/leaf3'))
                ),
                self.flipFrames(importImagesFrom(
                    resourcePath('src/img/particles/leaf4'))
                ),
                self.flipFrames(importImagesFrom(
                    resourcePath('src/img/particles/leaf5'))
                ),
                self.flipFrames(importImagesFrom(
                    resourcePath('src/img/particles/leaf6')))
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

    def createParticles(self, name, position, groups, animationFrames=0.2):
        ParticleEffect(position, self.frames[name], groups, animationFrames)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, position, animationFrames, groups, animationSpeed=0.2):
        super().__init__(groups)
        self.spriteType = 'magic'
        self.frameIndex = 0
        self.animationSpeed = animationSpeed
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
