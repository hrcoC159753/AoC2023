import sys
import itertools
import more_itertools
import functools

# file = sys.stdin
file = open('Day21/input1.txt')

def findS(lines):
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == 'S':
                return (i, j)
    assert False

def accessLines(lines, y, x):
    y %= len(lines)
    x %= len(lines[0])

    return lines[y][x]

def isValidPosition(position, lines):
    y, x = position
    return not (accessLines(lines, y, x) == '#')

def calculateGridPosition(position, lines):
    return (position[0] // len(lines), position[1] // len(lines[0]))

def getNextPositions(currentPosition, lines):
    y, x = currentPosition
    possiblePositions = [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]

    return [possiblePosition for possiblePosition in possiblePositions if isValidPosition(possiblePosition, lines)]

def getNextPositionsMult(lines, currentPositions):
    return {*itertools.chain.from_iterable(getNextPositions(position, lines) for position in currentPositions)}


def getNextPositionsByGrid(lines, currentPositions):
    groupedPositionsByGrid = more_itertools.bucket(getNextPositionsMult(lines, currentPositions), key = lambda x: calculateGridPosition(x, lines))
    r = dict()
    for k in groupedPositionsByGrid:
        r.update({k : set(groupedPositionsByGrid[k])})
    return r

def getPositionsByGrid(lines, positions):
    groupedPositionsByGrid = more_itertools.bucket(positions, key = lambda x: calculateGridPosition(x, lines))
    r = dict()
    for k in groupedPositionsByGrid:
        r.update({k : set(groupedPositionsByGrid[k])})
    return r

def getSolution(lines, startPositions, numberOfSteps, visitedGrids = set()):
    assert len(startPositions) > 0
    nextPositions = getNextPositionsMult(lines, startPositions)
    currentGrid = calculateGridPosition(next(iter(startPositions)), lines)

    previousPositionsInGrid = set()
    currentPositions = {*startPositions}
    if numberOfSteps == 0:
        return len(currentPositions)
    
    counter = 0
    nextPositions = getNextPositionsMult(lines, currentPositions) 

    while (nextPositionsInGrid := getPositionsByGrid(lines, nextPositions)[currentGrid]) != previousPositionsInGrid and counter < numberOfSteps:
        previousPositionsInGrid = getPositionsByGrid(lines, currentPositions)[currentGrid]
        currentPositions = nextPositions
        nextPositions = getNextPositionsMult(lines, currentPositions)
        counter += 1

    visitedGrids.add(currentGrid)

    numberOfPositionsInCurrentGrid = len(getPositionsByGrid(lines, currentPositions)[currentGrid])
    if counter == numberOfSteps:
        s = numberOfPositionsInCurrentGrid
    else:
        s = len(previousPositionsInGrid) if numberOfSteps % 2 == 0 else numberOfPositionsInCurrentGrid

    for gridId, numberOfStepsToGrid, newStartPositions in map(lambda x: (x[0], x[1][0], x[1][1]), filter(lambda x: x[1][0] < counter, getStepsToAdjecentGrids(lines, startPositions).items())):
        if gridId not in visitedGrids:
            s += getSolution(lines, newStartPositions, numberOfSteps - numberOfStepsToGrid, visitedGrids = visitedGrids)

    return s
    
def getStepsToAdjecentGrids(lines, startPositions):
    assert len(startPositions) > 0
    currentGrid = calculateGridPosition(next(iter(startPositions)), lines)
    adjecentGrids = {
        (currentGrid[0] - 1, currentGrid[1] - 1): None,
        (currentGrid[0] - 1, currentGrid[1]): None,
        (currentGrid[0] - 1, currentGrid[1] + 1): None,
        (currentGrid[0], currentGrid[1] + 1): None,
        (currentGrid[0] + 1, currentGrid[1] + 1): None,
        (currentGrid[0] + 1, currentGrid[1]): None,
        (currentGrid[0] + 1, currentGrid[1] - 1): None,
        (currentGrid[0], currentGrid[1] - 1): None,
    }

    numberOfSteps = 0
    currentPositions = {*startPositions}
    while any(v == None for v in adjecentGrids.values()):
        currentPositions = getNextPositionsMult(lines, currentPositions)
        numberOfSteps += 1
        for k, v in filter(lambda x: x[0] in adjecentGrids and adjecentGrids[x[0]] == None, getPositionsByGrid(lines, currentPositions).items()):
            assert len(v) > 0
            adjecentGrids[k] = (numberOfSteps, list(v))

    return adjecentGrids


def main():
    lines = list(map(lambda x: x.strip(), file.readlines()))
    testData = [
        # (6, 16),
        # (10, 50),
        (50, 1594),
        (100, 6536),
        (5000, 16733044)
    ]

    startPosition = findS(lines)
    for numberOfSteps, expected in testData:
        solution = getSolution(lines, {startPosition}, numberOfSteps, visitedGrids = set())
        print(f'{solution} -> {expected}')

if __name__ == '__main__':
    main()