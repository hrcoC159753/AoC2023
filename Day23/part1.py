import sys

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

def getNextPositions(lines, currentPosition, path = []):
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
    isASlope = lambda pos: lines[pos[0]][pos[1]] in slopeChars
    isNotAlreadyInPath = lambda pos: pos not in path

    def isADownwardsSlopeOrPath(pos):
        y, x = pos
        value = lines[y][x]

        assert value != '#'
        if value == '.':
            return True

        return (
            value == '>' and pos[1] - currentPosition[1] == 1 or 
            value == '<' and currentPosition[1] - pos[1] == 1 or 
            value == 'v' and pos[0] - currentPosition[0] == 1 or 
            value == '^' and currentPosition[0] - pos[0] == 1
        )
        
    newPositions = list(filter(isADownwardsSlopeOrPath, filter(isNotAlreadyInPath, filter(isNotForest, filter(isInValidRange, possiblePositions)))))

    return newPositions

def showLines(lines):
    for line in lines:
        print(line)

def getStartPosition(lines):
    index = next((i for i in range(len(lines[0])) if lines[0][i] == '.'), None)
    assert index != None
    return (0, index)

def solveRecursive(lines, startPosition, *, path):
    path = path[:]
    currentPosition = startPosition

    while len(nextPositions := getNextPositions(lines, currentPosition, path = path)) == 1:
        path.append(currentPosition)
        currentPosition = nextPositions[0]

    path.append(currentPosition)
    
    if len(nextPositions) == 0:
        return len(path)
    else:
        return max(solveRecursive(lines, newStartPosition, path = path) for newStartPosition in nextPositions)

def solve(lines, startPosition):
    return solveRecursive(lines, startPosition, path = []) - 1

def main():
    lines = file.readlines()
    lines = map(lambda x: x.strip(), lines)
    lines = list(lines)

    assert all(len(line) == len(lines[0]) for line in lines[1:])

    startPosition = getStartPosition(lines)

    solution = solve(lines, startPosition)

    print(solution)

if __name__ == '__main__':
    main()