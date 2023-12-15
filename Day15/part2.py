import itertools
import sys
from enum import Enum

def myHash(x):
    s = 0
    for c in x:
        s += ord(c)
        s *= 17
        s %= 256
    return s

class Operation(Enum):
    Equal = 0
    Minus = 1

def extractInput(x):
    if x.count('=') != 0:
        s = x.split("=")
        (f, n) = (s[0], int(s[1]))
        return (f, (Operation.Equal, n))
    elif x.count('-') != 0:
        s = x.split('-')
        return (s[0], (Operation.Minus, None))
    else:
        assert False, f'{x}'

def generateDo(boxes):
    def do(command):
        (s, (c, v)) = command

        h = myHash(s)
        optIndex = next((i for i in range(len(boxes[h])) if boxes[h][i][0] == s), None)
        
        if c == Operation.Equal:
            if optIndex != None:
                boxes[h][optIndex] = (s, v)
            else:
                boxes[h].append((s, v))
        elif c == Operation.Minus:
            if optIndex != None:
                del boxes[h][optIndex]
    return do

def printBoxes(boxes):
    for i in range(len(boxes)):
        if len(boxes[i]) > 0:
            print(f'{i}: {"".join(repr(v) for v in boxes[i])}')

def calculateFocusingPower(boxes):
    s = 0
    for (boxNumber, box) in enumerate(boxes):
        for (slotNumber, lens) in enumerate(box):
            s += (boxNumber + 1) * (slotNumber + 1) * lens[1]
    return s

def main():
    with open(sys.argv[1]) as fd:
        lines = fd.readlines()

    assert len(lines) == 1

    lines = list(map(lambda x: x.strip(), lines[0].split(',')))

    boxes = [[] for _ in range(256)]

    do = generateDo(boxes)
    for commandPair in map(extractInput, lines):
        do(commandPair)

    printBoxes(boxes)
    print()

    solution = calculateFocusingPower(boxes)
    print(solution)

if __name__ == '__main__':
    main()