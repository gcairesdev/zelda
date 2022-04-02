import pygame
from settings import *


class UI:
    def __init__(self):
        # general
        self.displaySurface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.healthBarRect = pygame.Rect(
            10, 10, UI_HEALTH_BAR_WIDTH, UI_BAR_HEIGHT)
        self.energyBarRect = pygame.Rect(
            10, 34, UI_ENERGY_BAR_WIDTH, UI_BAR_HEIGHT)

        # convert weapon dictionary
        self.weaponGraphics = []
        for weapon in WEAPON_DATA.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weaponGraphics.append(weapon)

        # convert magic dictionary
        self.magicGraphics = []
        for magic in MAGIC_DATA.values():
            path = magic['graphic']
            magic = pygame.image.load(path).convert_alpha()
            self.magicGraphics.append(magic)

    def showBar(self, current, maxAmount, bgRect, color):
        # draw background
        pygame.draw.rect(self.displaySurface, UI_BG_COLOR, bgRect)

        # convert stat to pixel
        ratio = current / maxAmount
        currentWidth = bgRect.width * ratio
        currentRect = bgRect.copy()
        currentRect.width = currentWidth

        # draw bar
        pygame.draw.rect(self.displaySurface, color, currentRect)
        pygame.draw.rect(self.displaySurface, UI_BG_COLOR, currentRect, 3)

    def showExp(self, exp):
        textSurf = self.font.render(str(int(exp)), False, UI_TEXT_COLOR)
        x = self.displaySurface.get_size()[0] - 20
        y = self.displaySurface.get_size()[1] - 20
        textRect = textSurf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.displaySurface, UI_BG_COLOR,
                         textRect.inflate(8, 8))
        self.displaySurface.blit(textSurf, textRect)
        pygame.draw.rect(self.displaySurface, UI_BORDER_COLOR,
                         textRect.inflate(8, 8), 3)

    def selectionBox(self, left, top, hasSwitched):
        bgRect = pygame.Rect(left, top, UI_ITEM_BOX_SIZE, UI_ITEM_BOX_SIZE)
        pygame.draw.rect(self.displaySurface, UI_BG_COLOR, bgRect)
        if not hasSwitched:
            pygame.draw.rect(self.displaySurface,
                             UI_BORDER_COLOR_ACTIVE, bgRect, 3)
        else:
            pygame.draw.rect(self.displaySurface, UI_BORDER_COLOR, bgRect, 3)
        return bgRect

    def weaponOverlay(self, weaponIndex, hasSwitched):
        x = 20
        y = self.displaySurface.get_size()[1] - UI_ITEM_BOX_SIZE - 20
        bgRect = self.selectionBox(x, y, hasSwitched)
        weaponSurf = self.weaponGraphics[weaponIndex]
        weaponRect = weaponSurf.get_rect(center=bgRect.center)

        self.displaySurface.blit(weaponSurf, weaponRect)

    def magicOverlay(self, magicIndex, hasSwitched):
        x = UI_ITEM_BOX_SIZE + 10
        y = self.displaySurface.get_size()[1] - UI_ITEM_BOX_SIZE - 35
        bgRect = self.selectionBox(x, y, hasSwitched)
        magicSurf = self.magicGraphics[magicIndex]
        magicRect = magicSurf.get_rect(center=bgRect.center)

        self.displaySurface.blit(magicSurf, magicRect)

    def gameOver(self):
        textSurf = self.font.render('Game Over', False, UI_TEXT_COLOR)
        x = self.displaySurface.get_size()[0] // 2
        y = self.displaySurface.get_size()[1] // 2
        textRect = textSurf.get_rect(center=(x, y))

        pygame.draw.rect(self.displaySurface, UI_BG_COLOR,
                         textRect.inflate(250, 100))
        self.displaySurface.blit(textSurf, textRect)
        pygame.draw.rect(self.displaySurface, UI_BORDER_COLOR,
                         textRect.inflate(250, 100), 3)

    def display(self, player):
        self.showBar(player.health, player.stats['health'],
                     self.healthBarRect, UI_HEALTH_COLOR)
        self.showBar(player.energy, player.stats['energy'],
                     self.energyBarRect, UI_ENERGY_COLOR)
        self.showExp(player.exp)

        self.weaponOverlay(player.weaponIndex, player.canSwitchWeapon)
        self.magicOverlay(player.magicIndex, player.canSwitchMagic)
