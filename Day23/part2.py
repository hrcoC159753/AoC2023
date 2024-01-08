import sys
import math
from enum import Enum

file = sys.stdin
# file = open('input1.txt')

def showPath(lines, path):
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if (y, x) not in path:
                print(lines[y][x], end = '')
            else:
                print('O', end = '')
        print()

def showPaths(lines, paths):
    paths = sum(map(lambda path: [path[0], path[1]], paths), [])
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
    return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[q]))

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

class Type(Enum):
    Single = 0
    Intersection = 1
    End = 2

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

    return

def tracePathsBetweenIntersections(lines, intersections):
    paths = []
    for intersection in map(lambda x: x[0], intersections):
        for startPosition in getNextPositions(lines, intersection):
            path = list(tracePath(lines, startPosition, previous = intersection))
            pathEnd = path[-1]
            pathLength = len(path)
            if (pathEnd, intersection) not in map(lambda p: p[0], paths):
                paths.append(((intersection, pathEnd), pathLength, path))
    return paths

def findPathsThatBeginWith(paths, startPosition):
    return list(filter(lambda path: path[0][0] == startPosition or path[0][1] == startPosition, paths))

def doPathsIntersect(path1, path2):
    return any(p in path2[2] for p in path1[2])

def solve(paths, startPosition, endPosition, previousScore = 0, usedPaths = []):
    if startPosition == endPosition:
        return previousScore
    usedPaths = usedPaths[:]
    foundPaths = list(filter(lambda x: x[0] not in usedPaths, findPathsThatBeginWith(paths, startPosition)))

    params = []
    # breakpoint()
    for path in foundPaths:
        newStartPosition = path[0][1] if path[0][0] == startPosition else path[0][0]
        newUsedPaths = usedPaths + [path[0]]
        params.append((newStartPosition, newUsedPaths, previousScore + path[1]))

    results = list(solve(paths, sp, endPosition, previousScore = ps, usedPaths = up) for sp, up, ps in params)    
    return max([0, *results])

def main():
    lines = file.readlines()
    lines = map(lambda x: x.strip(), lines)
    lines = list(lines)

    assert all(len(line) == len(lines[0]) for line in lines[1:])

    startPosition = getStartPosition(lines)
    endPosition = getEndPosition(lines)

    allIntersections = findIntersections(lines)
    pathsBetweenIntersections = tracePathsBetweenIntersections(lines, allIntersections)

    # print(len(pathsBetweenIntersections))
    # print(pathsBetweenIntersections)

    solution = solve(pathsBetweenIntersections, startPosition, endPosition)
    print(solution)

if __name__ == '__main__':
    main()