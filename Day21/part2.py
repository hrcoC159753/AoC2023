import sys
import itertools

file = sys.stdin
# file = open('input1.txt')

def findS(lines):
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == 'S':
                return (i, j)
    assert False

def isValidPosition(position, lines):
    y, x = position

    if y < 0 or y >= len(lines):
        return False

    if x < 0 or x >= len(lines[0]):
        return False

    if lines[y][x] == '#':
        return False

    return True

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


def main():
    lines = list(map(lambda x: x.strip(), file.readlines()))
    assert all(len(lines[0]) == len(line) for line in lines)

    sLocation = findS(lines)
    solution = solveFromPosition(sLocation, lines, 64)

    print(solution)

    
if __name__ == '__main__':
    main()