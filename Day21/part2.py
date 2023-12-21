import sys
import itertools
import functools

# file = sys.stdin
file = open('input1.txt')

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

    # if y < 0 or y >= len(lines):
    #     return False

    # if x < 0 or x >= len(lines[0]):
    #     return False

    if accessLines(lines, y, x) == '#':
        return False

    return True

def calculateGridPosition(position, lines):
    return (position[0] // len(lines), position[1] // len(lines[0]))

def getNextPositions(currentPosition, lines):
    y, x = currentPosition
    possiblePositions = [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]

    return [possiblePosition for possiblePosition in possiblePositions if isValidPosition(possiblePosition, lines)]

def solveFromPosition(currentPosition, lines, numberOfRepeats):
    listOfPositions = set()
    listOfPositions.add(currentPosition)

    while numberOfRepeats != 0:
        newPositions = set()
        for position in itertools.chain.from_iterable(getNextPositions(position, lines) for position in listOfPositions):
            newPositions.add(position)
        listOfPositions = newPositions
        numberOfRepeats -= 1

    listOfPositions = list(listOfPositions)
    return len(listOfPositions)

@functools.lru_cache
def solveFromPositions(currentPositions, lines):
    currentGridPosition = calculateGridPosition(currentPositions[0], lines)

    previousPositionsInGridPosition = []
    currentPositionsInCurrentGridPosition = {*filter(lambda x: calculateGridPosition(x, lines) == currentGridPosition, currentPositions)}
    numberOfRepeats = 0

    adjecentGrids = {
        (currentGridPosition[0] - 1, currentGridPosition[1] - 1) : None,
        (currentGridPosition[0] - 1, currentGridPosition[1]) : None,
        (currentGridPosition[0] - 1, currentGridPosition[1] + 1) : None,
        (currentGridPosition[0], currentGridPosition[1] + 1) : None,
        (currentGridPosition[0] + 1, currentGridPosition[1] + 1) : None,
        (currentGridPosition[0] + 1, currentGridPosition[1]) : None,
        (currentGridPosition[0] + 1, currentGridPosition[1] - 1) : None,
        (currentGridPosition[0], currentGridPosition[1] - 1) : None,
    }

    firstPgpi = None
    firstNumberOfRepeats = None

    while (pgpi := next((i for i, pgp in enumerate(previousPositionsInGridPosition) if currentPositionsInCurrentGridPosition == pgp), None)) == None or not all(v != None for v in adjecentGrids.values()):
        previousPositionsInGridPosition.append(currentPositionsInCurrentGridPosition)
        if pgpi != None and firstPgpi == None:
            firstPgpi = pgpi
            firstNumberOfRepeats = numberOfRepeats

        restList = list(filter(lambda x: calculateGridPosition(x, lines) != currentGridPosition, currentPositions))
        restList.sort(key = lambda x: calculateGridPosition(x, lines))
        rest = {k : list(v) for k, v in itertools.groupby(restList, key = lambda x: calculateGridPosition(x, lines))}
        for k, v in rest.items():
            if k in adjecentGrids and adjecentGrids[k] == None:
                adjecentGrids[k] = (numberOfRepeats, v)

        currentPositions = list({*itertools.chain.from_iterable(getNextPositions(position, lines) for position in currentPositions)})
        currentPositionsInCurrentGridPosition = {*filter(lambda x: calculateGridPosition(x, lines) == currentGridPosition, currentPositions)}
        numberOfRepeats += 1

    if pgpi != None and firstPgpi == None:
        firstPgpi = pgpi
        firstNumberOfRepeats = numberOfRepeats

    return (firstNumberOfRepeats, tuple(map(lambda x: len(x), previousPositionsInGridPosition[pgpi:firstNumberOfRepeats])), adjecentGrids)


def main():
    lines = tuple(map(lambda x: tuple(x.strip()), file.readlines()))
    assert all(len(lines[0]) == len(line) for line in lines)

    sLocation = findS(lines)
    visited = set()
    gridLocationInit = 0
    totalCount = 0
    maxSteps = 50

    previousRepeats = 0
    previousOuterGrid = []

    outerGrid = [(0, [sLocation], gridLocationInit)]
    while totalCount < maxSteps:
        previousTotalCount = totalCount
        previousOuterGrid = outerGrid 

        newOuterGrid = []
        for (locations, gridLocation) in outerGrid:
            currentGridPosition = calculateGridPosition(locations[0], lines)
            visited.add(currentGridPosition)

            (numberOfRepeats, repeats, rest) = solveFromPositions(tuple(locations), lines)

            totalCount += numberOfRepeats

            for (gridLocation, (numberOfRepeatsTillGridLocation, locations)) in rest.items():
                if gridLocation in visited:
                    continue
                
                if gridLocation in map(lambda x: x[1], newOuterGrid):
                    continue

                newOuterGrid.append((numberOfRepeatsTillGridLocation, locations, gridLocation))
        outerGrid = newOuterGrid

    finalTotal = previousOuterGrid
    for (locations, gridId) for previousOuterGrid:
        assert len(locations) == 0
        finalTotal += 

    print(f'{previousTotalCount}, {totalCount}')
    print(f'{list(map(lambda x: x[1], previousOuterGrid))}, {list(map(lambda x: x[1], outerGrid))}')

if __name__ == '__main__':
    main()