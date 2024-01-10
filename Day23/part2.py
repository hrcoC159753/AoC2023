import sys
import math
from enum import Enum
import bisect

file = sys.stdin
file = open('input1.txt')

def showPath(lines, path):
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if (y, x) not in path:
                print(lines[y][x], end = '')
            else:
                print('O', end = '')
        print()

def showPaths(lines, paths):
    paths = sum(map(lambda path: [path.p1, path.p2], paths), [])
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if (y, x) not in paths:
                print(lines[y][x], end = '')
            else:
                print('O', end = '')
        print()

def showType(lines, byType):
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            val = next((v for v in byType if v[0] == (y, x)), None)
            if val == None:
                print(lines[y][x], end = '')
            elif val[1] == Type.Single:
                print('S', end = '')
            elif val[1] == Type.Intersection:
                print('I', end = '')
            elif val[1] == Type.End:
                print('E', end = '')
            else:
                assert False
        print()


def getNextPositions(lines, currentPosition):
    y, x = currentPosition

    possibleChars = [
        '>',
        '<',
        'v',
        '^',
        '.'
    ]


    assert lines[y][x] in possibleChars, currentPosition

    possiblePositions = [
        (y + 1, x),
        (y - 1, x),
        (y, x + 1),
        (y, x - 1)
    ]

    isInValidRange = lambda pos: pos[0] < len(lines) and pos[0] >= 0 and pos[1] < len(lines[0]) and pos[1] >= 0
    isNotForest = lambda pos: lines[pos[0]][pos[1]] != '#'

    newPositions = list(filter(isNotForest, filter(isInValidRange, possiblePositions)))

    return newPositions

def positionDistance(p1, p2):
    return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2))

def showLines(lines):
    for line in lines:
        print(line)

def getStartPosition(lines):
    index = next((i for i in range(len(lines[0])) if lines[0][i] == '.'), None)
    assert index != None
    return (0, index)

def getEndPosition(lines):
    index = next((i for i in range(len(lines[-1])) if lines[-1][i] == '.'), None)
    assert index != None
    return (len(lines) - 1, index)

def findAllTypes(lines):
    retValues = []
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == '#':
                continue
            val = len(getNextPositions(lines, (y, x)))
            if val == 1:
                retValues.append(((y,x), Type.End))
            elif val == 2:
                retValues.append(((y,x), Type.Single))
            else:
                retValues.append(((y,x), Type.Intersection))
    return retValues

def findIntersections(lines):
    return list(filter(lambda x: x[1] == Type.Intersection, findAllTypes(lines)))

def tracePath(lines, begin, previous = None):
    yield begin
    while len(nextPositions := list(filter(lambda x: x != previous, getNextPositions(lines, begin)))) == 1:
        nextPosition = nextPositions[0]
        yield nextPosition

        previous = begin
        begin = nextPosition

def solve(lines, startPosition, endPosition, previousScore = 0, passedIntersection = [], previousPosition = None):
    previousPosition = previousPosition
    currentPosition = startPosition

    length = 0
    while len(nextPositions := list(filter(lambda x: x != previousPosition, getNextPositions(lines, currentPosition)))) == 1:
        previousPosition = currentPosition
        currentPosition = nextPositions[0]
        length += 1

    if currentPosition in passedIntersection:
        return -1

    if len(nextPositions) == 0 and currentPosition == endPosition:
        return previousScore + length
    elif len(nextPositions) > 1:
        newPassedIntersections = passedIntersection + [currentPosition]
        return max([0, *(
            solve(
                lines, nextPosition, endPosition, 
                previousScore = previousScore + length + 1, 
                passedIntersection = newPassedIntersections, 
                previousPosition = currentPosition
            ) for nextPosition in nextPositions)
        ])
    else:
        assert False

def solve2(lines, startPosition, endPosition):

    def goSingle(pos, prev):
        length = 0
        while len(nextPositions := list(filter(lambda x: x != prev, getNextPositions(lines, pos)))) == 1:
            prev = pos
            pos = nextPositions[0]
            length += 1
        return (pos, length, nextPositions)

    previousPosition = None
    currentPosition = startPosition

    solutions = []
    previousBatch = [(currentPosition, previousPosition, 0, [])]
    while len(previousBatch) > 0:
        nextBatch = []
        while len(previousBatch) > 0:
            currentPosition, previousPosition, previousLength, searchedIntersections = previousBatch.pop()
            currentPosition, length, nextPositions = goSingle(currentPosition, previousPosition)

            if currentPosition == endPosition:
                solutions.append(length + previousLength)

            if len(nextPositions) == 0:
                continue

            if currentPosition in searchedIntersections:
                continue

            newPassedIntersections = searchedIntersections + [currentPosition]
                        
            for nextPosition in nextPositions:
                nextBatch.append((nextPosition, currentPosition, previousLength + length + 1, newPassedIntersections))

        previousBatch = nextBatch

    return max(solutions)

def getIntersections(lines):
    intersections = []
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == '#':
                continue
            numberOfNextPositions = len(getNextPositions(lines, (y, x)))
            if numberOfNextPositions > 2:
                intersections.append((y, x))
    return intersections

def getPaths(lines):
    intersections = getIntersections(lines)
    paths = []
    for intersection in intersections:
        for start in getNextPositions(lines, intersection):
            pathTrace = list(tracePath(lines, start, previous = intersection))
            end = pathTrace[-1]
            newPath = Path(intersection, end, len(pathTrace))
            if newPath not in paths:
                paths.append(newPath)

    return paths

def findPaths(paths, position):
    yield from filter(lambda x: x.p1 == position or x.p2 == position, paths)

class Path:
    def __init__(self, p1, p2, length):
        self.p1 = p1
        self.p2 = p2
        self.length = length

    def __eq__(self, other):
        assert type(other) == Path
        return other.p1 == self.p1 and other.p2 == self.p2 or other.p1 == self.p2 and other.p2 == self.p1

    def __repr__(self):
        return f'({self.p1}, {self.p2}, {self.length})'

    def destinationPosition(self, start):
        assert self.p1 == start or self.p2 == start
        return self.p1 if self.p2 == start else self.p2


def solve3impl(paths, startPosition, endPosition):
    
    needToVisit = [(0, startPosition)]
    visited = []

    while len(needToVisit) > 0:
        currentCost, currentPosition = needToVisit.pop()
        for cost, intersection in map(lambda p: (p.length + currentCost, p.destinationPosition(currentPosition)), findPaths(paths, currentPosition)):
            if intersection == endPosition:
                return cost
            index = next((i for i, e in enumerate(needToVisit) if e[1] == intersection), None)
            if index != None:
                oldIntersection = needToVisit.pop(index)
                if oldIntersection[0] < cost:
                    bisect.insort(needToVisit, (cost, intersection), key = lambda x: x[0])
            else:
                bisect.insort(needToVisit, (cost, intersection), key = lambda x: x[0])

    return -1

def solve3(lines, startPosition, endPosition):
    paths = getPaths(lines)    
    return solve3impl(paths, startPosition, endPosition)

def main():
    lines = file.readlines()
    lines = map(lambda x: x.strip(), lines)
    lines = list(lines)

    assert all(len(line) == len(lines[0]) for line in lines[1:])

    startPosition = getStartPosition(lines)
    endPosition = getEndPosition(lines)

    solution = solve3(lines, startPosition, endPosition)
    print(solution)

if __name__ == '__main__':
    main()