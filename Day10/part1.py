import sys
from enum import Enum


class Direction(Enum):
    Right = 0
    Left = 1
    Up = 2
    Down = 3

def invert(d: Direction):
    if d == Direction.Right:
        return Direction.Left
    elif d == Direction.Left:
        return Direction.Right
    elif d == Direction.Up:
        return Direction.Down
    elif d == Direction.Down:
        return Direction.Up

def tuplePlusDirection(t, d: Direction):
    if d == Direction.Right:
        return (t[0] + 1, t[1])
    elif d == Direction.Left:
        return (t[0] - 1, t[1])
    elif d == Direction.Up:
        return (t[0], t[1] - 1)
    elif d == Direction.Down:
        return (t[0], t[1] + 1)
    else:
        assert False, f'{t}, {d}'


class Pipe(Enum):
    NorthSouth = (Direction.Up, Direction.Down)
    EastWest = (Direction.Left, Direction.Right)
    NorthEast = (Direction.Up, Direction.Right)
    NorthWest = (Direction.Up, Direction.Left)
    SouthWest = (Direction.Down, Direction.Left)
    SouthEast = (Direction.Down, Direction.Right)

    def __repr__(self):
        if self == Pipe.NorthSouth:
            return 'NS'
        elif self == Pipe.EastWest:
            return 'EW'
        elif self == Pipe.NorthEast:
            return 'NE'
        elif self == Pipe.NorthWest:
            return 'NW'
        elif self == Pipe.SouthEast:
            return 'SE'
        elif self == Pipe.SouthWest:
            return 'SW'
        else:
            assert False, f'{self}'

def letterToDirection(l):
    if l == '|':
        return Pipe.NorthSouth
    elif l == '-':
        return Pipe.EastWest
    elif l == 'L':
        return Pipe.NorthEast
    elif l == 'J':
        return Pipe.NorthWest
    elif l == '7':
        return Pipe.SouthWest
    elif l == 'F':
        return Pipe.SouthEast
    else:
        assert False, f'{l}'

def transformAllLetters(l):
    if l == 'S':
        return l
    elif l == '.':
        return None
    else:
        return letterToDirection(l)


class Matrix:

    def __init__(self, elements):
        assert all((len(elementLine) == len(elements[0]) for elementLine in elements[1:]))

        self.height = len(elements)
        self.width = len(elements[0])
        self.elements = elements
    
    def __getitem__(self, index):
        return self.elements[index[1]][index[0]]

    def getSafe(self, x, y):
        if y < 0 or x < 0 or y >= self.height or x >= self.width:
            return None
        return self[x, y]

    def __repr__(self):
        lines = [' '.join((repr(e) for e in line)) for line in self.elements]
        s = '\n'.join(lines)
        return s

def findStart(matrix):
    for i in range(matrix.width):
        for j in range(matrix.height):
            if matrix[i, j] == 'S':
                return (i, j)

    assert False, f'{matrix}'

def goNext(matrix, currentPosition, outDirection):
    newPosition = tuplePlusDirection(currentPosition, outDirection)

    print(f'{currentPosition}, {outDirection}')
    # breakpoint()

    newValue = matrix.getSafe(newPosition[0], newPosition[1])
    if newValue == None:
        return None

    if type(newValue) != Pipe and newValue == 'S':
        return (newPosition, ())

    inDirection = invert(outDirection)
    inDirectionList = list(newValue.value)
    if not (inDirection in inDirectionList):
        return None

    return (newPosition, next(e for e in inDirectionList if e != inDirection))

def searchPath(matrix, currentPosition, outDirection, finalPosition):
    first = True

    l = []
    while currentPosition != finalPosition or first:
        first = False
        newTuple = goNext(matrix, currentPosition, outDirection)

        if newTuple == None:
            return None            

        l.append(newTuple)

        (newPosition, newOutDirection) = newTuple

        currentPosition = newPosition
        outDirection = newOutDirection

    return l

def main():

    with open(sys.argv[1]) as fd:
        lines = fd.readlines()

    elements = list(map(lambda x: [transformAllLetters(e) for e in x], map(lambda x: x.strip(), lines)))

    matrix = Matrix(elements)
    start = findStart(matrix)

    print(matrix)

    l = searchPath(matrix, start, Direction.Down, start)
    
    print(len(l) // 2)

if __name__ == '__main__':
    main()
    