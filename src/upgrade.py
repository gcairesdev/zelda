import pygame
from settings import *


class Upgrade:
    def __init__(self, player):
        # general setup
        self.displaySurface = pygame.display.get_surface()
        self.player = player
        self.totalAtributtes = len(player.stats)
        self.attributeNames = list(player.stats.keys())
        self.maxValues = list(player.maxStats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # item creation
        self.height = self.displaySurface.get_size()[1] * 0.8
        self.width = self.displaySurface.get_size()[0] // 6
        self.createItems()

        # selection system
        self.selectionIndex = 0
        self.selectionTime = None
        self.canMove = True

    def input(self):
        keys = pygame.key.get_pressed()

        if self.canMove:
            if keys[pygame.K_RIGHT] and self.selectionIndex < self.totalAtributtes - 1:
                self.selectionIndex += 1
                self.canMove = False
                self.selectionTime = pygame.time.get_ticks()
            if keys[pygame.K_LEFT] and self.selectionIndex >= 1:
                self.selectionIndex -= 1
                self.canMove = False
                self.selectionTime = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.canMove = False
                self.selectionTime = pygame.time.get_ticks()
                self.itemList[self.selectionIndex].trigger(self.player)

    def selectionCooldown(self):
        if not self.canMove:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.selectionTime >= 300:
                self.canMove = True

    def createItems(self):
        self.itemList = []
        for item, index in enumerate(range(self.totalAtributtes)):
            fullWidth = self.displaySurface.get_size()[0]
            increment = fullWidth // self.totalAtributtes
            left = (item * increment) + (increment - self.width) // 2
            top = self.displaySurface.get_size()[1] * 0.1

            item = Item(left, top, self.width, self.height, index, self.font)
            self.itemList.append(item)

    def display(self):
        self.input()
        self.selectionCooldown()

        for index, item in enumerate(self.itemList):
            name = self.attributeNames[index]
            value = self.player.getStatsValueByIndex(index)
            maxValue = self.maxValues[index]
            cost = self.player.getCostByIndex(index)
            item.display(self.displaySurface, self.selectionIndex, name, value, maxValue, cost)

class Item:
    def __init__(self, left, top, width, height, index, font):
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font

    def displayNames(self, surface, name, cost, selected):
        color = TEXT_COLOR_SELECTED if selected else UI_TEXT_COLOR

        titleSurface = self.font.render(name, False, color)
        titleRect = titleSurface.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0, 20))

        costSurface = self.font.render(str(cost), False, color)
        costRect = costSurface.get_rect(midbottom=self.rect.midbottom - pygame.math.Vector2(0, 20))

        surface.blit(titleSurface, titleRect)
        surface.blit(costSurface, costRect)

    def displayBar(self, surface, value, maxValue, selected):
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        fullHeight = bottom[1] - top[1]
        relativeNumber = (value / maxValue) * fullHeight
        valueRect = pygame.Rect(top[0] - 15, bottom[1] - relativeNumber, 30, 10)

        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, valueRect)

    def trigger(self, player):
        upgradeAttribute = list(player.stats.keys())[self.index]

        if player.exp >= player.upgradeCost[upgradeAttribute] and player.stats[upgradeAttribute] < player.maxStats[upgradeAttribute] :
            player.exp -= player.upgradeCost[upgradeAttribute]
            player.stats[upgradeAttribute] *= 1.2
            player.upgradeCost[upgradeAttribute] *= 1.4

        if player.stats[upgradeAttribute] > player.maxStats[upgradeAttribute]:
            player.stats[upgradeAttribute] = player.maxStats[upgradeAttribute]

    def display(self, surface, selectionNum, name, value, maxValue, cost):
        if self.index == selectionNum:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        self.displayNames(surface, name, cost, self.index == selectionNum)
        self.displayBar(surface, value, maxValue, self.index == selectionNum)
