import os
import sys
import pygame
from csv import reader


def importCsvLayout(path):
    terrainMap = []
    with open(path) as levelMap:
        layout = reader(levelMap, delimiter=',')
        for row in layout:
            terrainMap.append(list(row))
        return terrainMap


def importImagesFrom(path):
    surfaceList = []

    for filename in sorted(os.listdir(path)):
        fullPath = path + '/' + filename
        assetUrl = resourcePath(fullPath)
        imageSurf = pygame.image.load(assetUrl).convert_alpha()
        surfaceList.append(imageSurf)

    return surfaceList

def resourcePath(relativePath):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relativePath)
