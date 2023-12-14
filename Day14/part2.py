import sys
from enum import Enum
import copy

class Direction(Enum):
    Up = 0
    Down = 1
    Left = 2
    Right = 3

def setIndexList(list, x, y, value):
    list[y][x] = value

def getIndexList(list, x, y):
    return list[y][x]

def printList(l):
    for line in l:
        for c in line:
            print(c, end = '')
        print()

def transform(lines, direction):

    if direction == Direction.Up:
        outerRange = range(len(lines[0]))
        innerRange = range(len(lines))
        accessor = lambda a, b: (a, b)
        foundBlock = lambda x, j: j + 1
        foundRock = lambda x: x + 1
        startChangingIndexInit = 0
    elif direction == Direction.Down:
        outerRange = range(len(lines[0]))
        innerRange = range(len(lines) - 1, -1, -1)
        accessor = lambda a, b: (a, b)
        foundBlock = lambda x, j: j - 1
        foundRock = lambda x: x - 1
        startChangingIndexInit = len(lines) - 1
    elif direction == Direction.Right:
        outerRange = range(len(lines))
        innerRange = range(len(lines[0]) - 1, -1, -1)
        accessor = lambda a, b: (b, a)
        foundBlock = lambda x, j: j - 1
        foundRock = lambda x: x - 1
        startChangingIndexInit = len(lines[0]) - 1
    elif direction == Direction.Left:
        outerRange = range(len(lines))
        innerRange = range(len(lines[0]))
        accessor = lambda a, b: (b, a)
        foundBlock = lambda x, j: j + 1
        foundRock = lambda x: x + 1
        startChangingIndexInit = 0
    else:
        assert False, f'{direction}'
 
    for i in outerRange:
        startChangingIndex = startChangingIndexInit
        for j in innerRange:
            if getIndexList(lines, *accessor(i, j)) == '#':
                startChangingIndex = foundBlock(startChangingIndex, j)
            elif getIndexList(lines, *accessor(i, j)) == 'O':
                setIndexList(lines, *accessor(i, j), '.')
                setIndexList(lines, *accessor(i, startChangingIndex), 'O')
                startChangingIndex = foundRock(startChangingIndex)
                
def calculateSolution(lines):
    s = 0
    for j in range(len(lines[0])):
        c = len(lines)
        for (i, e) in enumerate(range(len(lines), 0, -1)):
            if lines[i][j] == 'O':
                s += c
                c -= 1
            elif lines[i][j] == '#':
                c = e - 1
    return s

def calculateSolutionOnTransformed(lines):
    s = 0
    for j in range(len(lines)):
        s += (len(lines) - j) * sum(1 for e in lines[j] if e == 'O')
    return s

def areSameLines(line1, line2):
    assert len(line1) == len(line2)
    assert all(len(line1[0]) == len(l) for l in line1), f'{line1}'
    assert all(len(line2[0]) == len(l) for l in line2), f'{line2}'
    assert len(line1[0]) == len(line2[0])

    for (l1, l2) in zip(line1, line2):
        for (c1, c2) in zip(l1, l2):
            if c1 != c2:
                return False
    
    return True

def preformCycle(lines):
    transform(lines, Direction.Up)
    transform(lines, Direction.Left)
    transform(lines, Direction.Down)
    transform(lines, Direction.Right)

def main():

    with open(sys.argv[1]) as fd:
        lines = fd.readlines()

    lines = list(map(lambda x: [e for e in x], map(lambda x: x.strip(), lines)))

    assert all(len(lines[0]) == len(line) for line in lines[1:])

    previousTransformations = []
    newLines = lines[:]

    while len(previousTransformations) == 0 or not any(areSameLines(t, newLines) for t in previousTransformations):
        previousTransformations.append(copy.deepcopy(newLines))

        preformCycle(newLines)

    index = next(i for (i, e) in enumerate(previousTransformations) if areSameLines(e, newLines))
    solution = calculateSolutionOnTransformed(previousTransformations[((1_000_000_000 - index) % (len(previousTransformations) - index)) + index])
    print(solution)
if __name__ == '__main__':
    main()