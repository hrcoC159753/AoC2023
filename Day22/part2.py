import sys
import itertools

file = sys.stdin
# file = open('Day22/input1.txt')

class Brick:

    def __init__(self, xRange, yRange, zRange):
        self.xRange = xRange
        self.yRange = yRange
        self.zRange = zRange

    def __repr__(self):
        return f'({self.xRange[0]}, {self.yRange[0]}, {self.zRange[0]} ~ {self.xRange[1]}, {self.yRange[1]}, {self.zRange[1]})'

    def fromOther(other, z = None):
        if z == None:
            zRange = other.zRange
        else:
            zRange = (z, z)
        return Brick(other.xRange, other.yRange, zRange)

def brickLineToBrick(brickLine: str) -> Brick:
    beginPart, endPart = brickLine.split('~')
    (xbStr, ybStr, zbStr), (xeStr, yeStr, zeStr) = beginPart.split(','), endPart.split(',')
    (xb, yb, zb), (xe, ye, ze) = (int(xbStr), int(ybStr), int(zbStr)), (int(xeStr), int(yeStr), int(zeStr))
    return Brick((xb, xe), (yb, ye), (zb, ze))

def isRangesCrossing(range1, range2):
    return not (range1[1] < range2[0] or range1[0] > range2[1])

def isSquaresCrossing(b1, b2):
    return isRangesCrossing(b1.xRange, b2.xRange) and isRangesCrossing(b1.yRange, b2.yRange)

def placeBricks(bricks):
    mX, mY = max(map(lambda x: x.xRange[1], bricks)), max(map(lambda x: x.yRange[1]))    

    isHoldingOn = dict()

    i = 0
    def getId():
        nonlocal i
        k = i
        v = chr(ord('A') + k)
        k += 1
        i = k
        return v

    def idGen():
        while True:
            yield getId()   


    levels = []
    firstBrick = bricks[0]
    restBricks = bricks[1:]
    
    for brickId, brick in zip(idGen(), restBricks):
        indexOfFirstCrossingLevel = next((i for i, lastLevel in enumerate(levels[::-1]) if any(isSquaresCrossing(lastLevelBrick, brick) for lastLevelBrick in lastLevel)), None)

        if indexOfFirstCrossingLevel == None:
            for z in range(brick.zRange[1] - brick.zRange[0] + 1):
                levels.append([])
                levels[z].append(brick)
        else:
            bricksThatAreCrossing = list(crossingBrick for crossingBrick in levels[indexOfFirstCrossingLevel] if isSquaresCrossing(crossingBrick, brick))
            assert len(bricksThatAreCrossing) > 0

            isHoldingOn[brick] = bricksThatAreCrossing


def main():
    lines = map(lambda x: x.strip(), file.readlines())
    lines = map(brickLineToBrick, lines)
    bricks = list(lines)
    bricks.sort(key = lambda b: b.zRange[0])

    _, bricks = placeBricks(bricks)


if __name__ == '__main__':
    main()