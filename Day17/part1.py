import sys
from enum import Enum
from queue import Queue
from queue import LifoQueue

class Direction(Enum):
    Right = 0
    Left = 1
    Up = 2
    Down = 3

class Head:
    def __init__(self, direction, nextPosition, sum, numSameDirection = 0):
        self.direction = direction
        self.nextPosition = nextPosition
        self.sum = sum
        self.numSameDirection = numSameDirection

def showHeads(lines, heads):
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            optHead = next((head for head in heads if (i, j) == head.nextPosition), None)
            if optHead != None:
                d = optHead.direction
                if d == Direction.Right:
                    print('>', end = '')
                elif d == Direction.Left:
                    print('<', end = '')
                elif d == Direction.Up:
                    print('^', end = '')
                elif d == Direction.Down:
                    print('v', end = '')
            else:
                print(f'{lines[i][j]}', end = '')
        print()

def showScores(scores):
    for i in range(len(scores)):
        for j in range(len(scores[0])):
            if scores[i][j] != None:
                print('{: <3}'.format(scores[i][j]), end = ' ')
            else:
                print('{: <3}'.format('N'), end = ' ')
        print()

def isValidPosition(lines, position):
    (y, x) = position
    (height, width) = (len(lines), len(lines[0]))

    return y >= 0 and y < height and x >= 0 and x < width 

def isValidHead(lines, head):
    return isValidPosition(lines, head.nextPosition) and head.numSameDirection < 3

def moveForward(lines, head):
    (y, x) = head.nextPosition
    if head.direction == Direction.Right:
        newLocation = (y, x + 1)
    elif head.direction == Direction.Left:
        newLocation = (y, x - 1)
    elif head.direction == Direction.Up:
        newLocation = (y - 1, x)
    elif head.direction == Direction.Down:
        newLocation = (y + 1, x)

    if not isValidPosition(lines, newLocation):
        return None
    if head.numSameDirection + 1 == 3:
        return None
    return Head(head.direction, newLocation, head.sum + lines[newLocation[0]][newLocation[1]], numSameDirection = head.numSameDirection + 1)

def moveClockwise90Degrees(lines, head):
    (y, x) = head.nextPosition
    if head.direction == Direction.Right:
        newLocation = (y + 1, x)
        newDirection = Direction.Down
    elif head.direction == Direction.Left:
        newLocation = (y - 1, x)
        newDirection = Direction.Up
    elif head.direction == Direction.Up:
        newLocation = (y, x + 1)
        newDirection = Direction.Right
    elif head.direction == Direction.Down:
        newLocation = (y, x - 1)
        newDirection = Direction.Left

    if not isValidPosition(lines, newLocation):
        return None
    return Head(newDirection, newLocation, head.sum + lines[newLocation[0]][newLocation[1]], numSameDirection = 1)

def moveCounterClockwise90Degrees(lines, head):
    (y, x) = head.nextPosition
    if head.direction == Direction.Right:
        newLocation = (y - 1, x)
        newDirection = Direction.Up
    elif head.direction == Direction.Left:
        newLocation = (y + 1, x)
        newDirection = Direction.Down
    elif head.direction == Direction.Up:
        newLocation = (y, x - 1)
        newDirection = Direction.Left
    elif head.direction == Direction.Down:
        newLocation = (y, x + 1)
        newDirection = Direction.Right

    if not isValidPosition(lines, newLocation):
        return None
    return Head(newDirection, newLocation, head.sum + lines[newLocation[0]][newLocation[1]], numSameDirection = 1)

def moveForward2(position, direction):
    (y, x) = position
    if direction == Direction.Right:
        newLocation = (y, x + 1)
    elif direction == Direction.Left:
        newLocation = (y, x - 1)
    elif direction == Direction.Up:
        newLocation = (y - 1, x)
    elif direction == Direction.Down:
        newLocation = (y + 1, x)

    return (newLocation, direction)

def moveClockwise90Degrees2(position, direction):
    (y, x) = position
    if direction == Direction.Right:
        newLocation = (y + 1, x)
        newDirection = Direction.Down
    elif direction == Direction.Left:
        newLocation = (y - 1, x)
        newDirection = Direction.Up
    elif direction == Direction.Up:
        newLocation = (y, x + 1)
        newDirection = Direction.Right
    elif direction == Direction.Down:
        newLocation = (y, x - 1)
        newDirection = Direction.Left

    return (newLocation, newDirection)

def moveCounterClockwise90Degrees2(position, direction):
    (y, x) = position
    if direction == Direction.Right:
        newLocation = (y - 1, x)
        newDirection = Direction.Up
    elif direction == Direction.Left:
        newLocation = (y + 1, x)
        newDirection = Direction.Down
    elif direction == Direction.Up:
        newLocation = (y, x - 1)
        newDirection = Direction.Left
    elif direction == Direction.Down:
        newLocation = (y, x + 1)
        newDirection = Direction.Right

    return (newLocation, newDirection)


def getNextHeads(lines, head):
    forwardHead = moveForward(lines, head)
    clockwiseHead = moveClockwise90Degrees(lines, head)
    counterClockwiseHead = moveCounterClockwise90Degrees(lines, head)

    yield forwardHead
    yield clockwiseHead
    yield counterClockwiseHead

def recursiveSolution(lines, currentPosition, endPosition, previousDirections):
    if currentPosition == endPosition:
        return lines[endPosition[0]][endPosition[1]]

    newData = []
    prevDir = previousDirections[-2:-4:-1]
    reversed(prevDir)

    if not (len(previousDirections) > 3 and all(previousDirections[-1] == direction for direction in prevDir)):
        newData.append(moveForward2(currentPosition, previousDirections[-1]))
    newData.append(moveClockwise90Degrees2(currentPosition, previousDirections[-1]))
    newData.append(moveCounterClockwise90Degrees2(currentPosition, previousDirections[-1]))

    v = lines[currentPosition[0]][currentPosition[1]]

    return v + min((recursiveSolution(lines, pos, endPosition, prevDir + [direction]) for (pos, direction) in newData if isValidPosition(lines, pos)))

def main():

    with open(sys.argv[1]) as fd:
        lines = fd.readlines()

    lines = list(map(lambda x: [int(e) for e in x.strip()], lines))
    scores = [[None for j in range(len(lines[0]))] for i in range(len(lines))]

    assert all(len(lines[0]) == len(line) for line in lines)

    head = Head(Direction.Right, (0, 0), 0, numSameDirection = 0)

    endLocation = (len(lines) - 1, len(lines[0]) - 1)

    q = LifoQueue()
    q.put(head)

    v = recursiveSolution(lines, (0, 0), endLocation, [Direction.Right])
    print(v)

if __name__ == '__main__':
    main()