import sys
from enum import Enum
from queue import Queue

class Direction(Enum):
    Up = 0
    Down = 1
    Right = 2
    Left = 3

def showSolution(lines, visitedRays):
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if (i, j) in map(lambda x: x.nextPosition, visitedRays):
                print('#', end = '')
            else:
                print('.', end = '')
        print()

def showLines(lines):
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            print(lines[i][j], end = '')
        print()

def showRay(lines, ray):
    print(ray.nextPosition)
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if (i, j) != ray.nextPosition:
                print(lines[i][j], end = '')
            else:
                print('O', end = '')
        print()

def leftTopRightBottomMirror(inDirection: Direction) -> Direction:
    if inDirection == Direction.Right:
        return Direction.Down
    elif inDirection == Direction.Up:
        return Direction.Left
    elif inDirection == Direction.Left:
        return Direction.Up
    elif inDirection == Direction.Down:
        return Direction.Right
    else:
        assert False

def rightTopLeftBottomMirror(inDirection: Direction) -> Direction:
    if inDirection == Direction.Right:
        return Direction.Up
    elif inDirection == Direction.Up:
        return Direction.Right
    elif inDirection == Direction.Left:
        return Direction.Down
    elif inDirection == Direction.Down:
        return Direction.Left
    else:
        assert False
    
def emptySpace(inDirection: Direction) -> Direction:
    return inDirection

def horizontalSplitter(inDirection: Direction) -> [Direction]:
    if inDirection == Direction.Left or inDirection == Direction.Right:
        return [inDirection]
    elif inDirection == Direction.Up or inDirection == Direction.Down:
        return [Direction.Left, Direction.Right]
    else:
        assert False

def verticalSplitter(inDirection: Direction):
    if inDirection == Direction.Down or inDirection == Direction.Up:
        return [inDirection]
    elif inDirection == Direction.Left or inDirection == Direction.Right:
        return [Direction.Down, Direction.Up]
    else:
        assert False

def nextSteps(symbol, direction):
    if symbol == '.':
        return [emptySpace(direction)]
    elif symbol == '\\':
        return [leftTopRightBottomMirror(direction)]
    elif symbol == '/':
        return [rightTopLeftBottomMirror(direction)]
    elif symbol == '-':
        return horizontalSplitter(direction)
    elif symbol == '|':
        return verticalSplitter(direction)
    else:
        assert False, f'{symbol}'

def nextPosition(currentPosition: (int, int), outDirection: Direction):
    if outDirection == Direction.Up:
        return (currentPosition[0] - 1, currentPosition[1])
    elif outDirection == Direction.Down:
        return (currentPosition[0] + 1, currentPosition[1])
    elif outDirection == Direction.Left:
        return (currentPosition[0], currentPosition[1] - 1)
    elif outDirection == Direction.Right:
        return (currentPosition[0], currentPosition[1] + 1)
    else:
        assert False, f'{outDirection}'

class RayHead:

    def __init__(self, direction: Direction, nextPosition: (int, int)):
        self.direction = direction
        self.nextPosition = nextPosition

    def __repr__(self):
        return ' '.join([repr(self.direction), repr(self.nextPosition)])

    def __eq__(self, other):
        return self.direction == other.direction and self.nextPosition == other.nextPosition
    
    def __hash__(self):
        return hash(self.direction) + hash(self.nextPosition)

def forwardRay(head: RayHead, lines: [str]) -> [(int, int)]:
    (y, x) = head.nextPosition

    assert x >= 0
    assert x < len(lines[0])
    assert y >= 0
    assert y < len(lines)

    c = lines[y][x]

    steps = nextSteps(c, head.direction)

    return list(map(lambda positionStepPair: RayHead(positionStepPair[1], positionStepPair[0]), ((nextPosition(head.nextPosition, step), step) for step in steps)))

def inRange(lines, position):
    (y, x) = position
    (width, height) = (len(lines[0]), len(lines))

    return not (x < 0 or x >= width or y < 0 or y >= height)

def getSolutionFor(lines, head):
    visited = set()
    q = Queue()
    q.put(head)

    isInValidRange = lambda h: inRange(lines, h.nextPosition)
    isNotAlreadyVisited = lambda h: h not in visited 
    isEmptySpace = lambda h: lines[h.nextPosition[0], h.nextPosition[1]]
    uniquePositions = 0
    while not q.empty():
        rayHead = q.get()
        # showRay(lines, rayHead)
        newRayHeads = forwardRay(rayHead, lines)
        for newRayHead in filter(isNotAlreadyVisited, filter(isInValidRange, newRayHeads)):
            q.put(newRayHead)

        if rayHead.nextPosition not in map(lambda x: x.nextPosition, visited):
            uniquePositions += 1
        visited.add(rayHead)
    
    return uniquePositions
    # print()
    # showLines(lines)
    # print()
    # breakpoint()
    # showSolution(lines, visited)
    # print()
    print(f'Solution: {uniquePositions}')
def main():

    with open(sys.argv[1]) as fd:
        lines = fd.readlines()

    lines = list(map(lambda x: x.strip(), lines))

    assert all(len(lines[0]) == len(line) for line in lines[1:])

    head = RayHead(Direction.Right, (0, 0))
    heads = []
    for i in range(len(lines)):
        heads.append(RayHead(Direction.Right, (i, 0)))
    for i in range(len(lines)):
        heads.append(RayHead(Direction.Left, (i, len(lines[0]) - 1)))
    for i in range(len(lines[0])):
        heads.append(RayHead(Direction.Down, (0, i)))
    for i in range(len(lines)):
        heads.append(RayHead(Direction.Up, (len(lines) - 1, i)))

    maxSolution = 0
    for (i, head) in enumerate(heads):
        solution = getSolutionFor(lines, head)
        print(f'{i}: Working on {head}')
        if solution > maxSolution:
            print(f'Changing max solution from {maxSolution} to {solution}')
            maxSolution = solution
    print(maxSolution)

if __name__ == '__main__':
    main()
