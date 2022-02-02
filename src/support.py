from csv import reader

def importCsvLayout(path):
    terrainMap = []
    with open(path) as levelMap:
        layout = reader(levelMap, delimiter = ',')
        for row in layout:
            terrainMap.append(list(row))
        return terrainMap
