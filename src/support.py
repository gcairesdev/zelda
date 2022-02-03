import os
import pygame
from csv import reader

def importCsvLayout(path):
    terrainMap = []
    with open(path) as levelMap:
        layout = reader(levelMap, delimiter = ',')
        for row in layout:
            terrainMap.append(list(row))
        return terrainMap

def importImagesFrom(path):
    surfaceList = []

    for filename in sorted(os.listdir(path)):
        fullPath = path + '/' + filename
        imageSurf = pygame.image.load(fullPath).convert_alpha()
        surfaceList.append(imageSurf)

    return surfaceList