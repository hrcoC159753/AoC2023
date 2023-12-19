import sys
from enum import Enum
from queue import PriorityQueue
import bisect

class Direction(Enum):
    Right = 'R'
    Left = 'L'
    Up = 'U'
    Down = 'D'

class Head:
    def __init__(self, direction, position, numSameDirection = 0):
        self.direction = direction
        self.position = position
        self.numSameDirection = numSameDirection

    def __repr__(self):
        return f'{repr(self.direction), {self.position}, {self.numSameDirection}}'

def showHeads(lines, heads):
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            optHead = next((head for head in heads if (i, j) == head.position), None)
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

def debugView(currentHead, newHeads, scores):
    for i in range(len(scores)):
        for j in range(len(scores[0])):
            optNewHead = next(filter(lambda h: h.position == (i, j), newHeads), None)
            if (i, j) == currentHead.position:
                print('{: <3}'.format(currentHead.direction.value), end = ' ')
            elif optNewHead != None:
                print('{: <3}'.format(optNewHead.direction.value.lower()), end = ' ')
            elif scores[i][j] != None:
                print('{: <3}'.format(scores[i][j]), end = ' ')
            else:
                print('{: <3}'.format('N'), end = ' ')
        print()

def isValidPosition(lines, position):
    (y, x) = position
    (height, width) = (len(lines), len(lines[0]))

    return y >= 0 and y < height and x >= 0 and x < width 

def moveForward(lines, head):
    if head == None:
        return None
    (y, x) = head.position
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
    if head.numSameDirection == 3:
        return None
    return Head(head.direction, newLocation, numSameDirection = head.numSameDirection + 1)

def moveClockwise90Degrees(lines, head):
    (y, x) = head.position
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
    return Head(newDirection, newLocation, numSameDirection = 1)

def moveCounterClockwise90Degrees(lines, head):
    (y, x) = head.position
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
    return Head(newDirection, newLocation, numSameDirection = 1)

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
    secondForwardHead = moveForward(lines, forwardHead)
    thirdForwardHead = moveForward(lines, secondForwardHead)
    if head.direction != Direction.Down:
        clockwiseHead = moveClockwise90Degrees(lines, head)
    else:
        clockwiseHead = None
    if head.direction != Direction.Up:
        counterClockwiseHead = moveCounterClockwise90Degrees(lines, head)
    else:
        counterClockwiseHead = None

    for newHead in filter(lambda x: x != None, (forwardHead, clockwiseHead, counterClockwiseHead, secondForwardHead, thirdForwardHead)):
        yield newHead

def main():

    with open(sys.argv[1]) as fd:
        lines = fd.readlines()

    lines = list(map(lambda x: [int(e) for e in x.strip()], lines))
    scores = [[None for j in range(len(lines[0]))] for i in range(len(lines))]

    assert all(len(lines[0]) == len(line) for line in lines)

    head = Head(Direction.Right, (0, 0))
    scores[0][0] = 0

    endLocation = (len(lines) - 1, len(lines[0]) - 1)

    visited = set()
    q = []
    q.append(head)

    getCost = lambda head: scores[head.position[0]][head.position[1]]
    getAdditionalCost = lambda head: lines[head.position[0]][head.position[1]]
    sortKey = lambda head: getCost(head)

    while len(q) > 0:
        currentHead = q.pop(0)      

        if currentHead == endLocation:
            break

        nextHeads = list(getNextHeads(lines, currentHead))
        for newHead in nextHeads:
            newCost = getCost(currentHead) + getAdditionalCost(newHead)

            if getCost(newHead) == None or getCost(newHead) > newCost:
                (y, x) = newHead.position
                scores[y][x] = newCost
            if newHead.position is not visited:
                optIndex = next((i for i, e in enumerate(q) if e.position == newHead.position), None)
                if optIndex != None:
                    q.sort(key = sortKey)
                else:
                    bisect.insort(q, newHead, key = sortKey)


        visited.add(currentHead.position)
        debugView(currentHead, nextHeads, scores)
        print(len(q), len(visited))
        print()

    solution = scores[endLocation[0]][endLocation[1]]  
    print(solution)

if __name__ == '__main__':
    main()