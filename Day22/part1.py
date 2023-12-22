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
    firstBrick = bricks[0]
    restBricks = bricks[1:]

    levels = []
    bricks = dict()
    i = 0
    def getId():
        nonlocal i
        k = i
        v = chr(ord('A') + k)
        k += 1
        i = k
        return v
        
    for z in range(firstBrick.zRange[1] - firstBrick.zRange[0] + 1):
        l = []
        if z == len(levels):
            levels.append([])
        v = Brick.fromOther(firstBrick, z = 1 + z)
        levels[z].append(v)
        l.append(v)
    bricks.update({getId() : l})

    for brick in restBricks:
        # breakpoint()
        indexOfFirstCrossingLevel = next((i for i, lastLevel in enumerate(levels[::-1]) if any(isSquaresCrossing(lastLevelBrick, brick) for lastLevelBrick in lastLevel)), None)
        if indexOfFirstCrossingLevel == None:
            l = []
            for z in range(brick.zRange[1] - brick.zRange[0] + 1):
                if len(levels) == z:
                    levels.append([])
                v = Brick.fromOther(brick, z = 1 + z)
                levels[z].append(v)
                l.append(v)
            bricks.update({getId() : l})
        else:
            index = len(levels) - 1 - indexOfFirstCrossingLevel
            if index == len(levels) - 1:
                l = []
                for _ in range(brick.zRange[1] - brick.zRange[0] + 1):
                    v = Brick.fromOther(brick, z = len(levels) + 1)
                    levels.append([v])
                    l.append(v)
                bricks.update({getId() : l})
            else:
                l = []
                for z in range(brick.zRange[1] - brick.zRange[0] + 1):
                    if index + z + 1 == len(levels):
                        levels.append([])
                    v = Brick.fromOther(brick, z = 1 + index + z + 1)
                    levels[index + z + 1].append(v)
                    l.append(v)
                bricks.update({getId() : l})

    return levels, bricks

def bricksToBricksPerLevel(bricks):
    bricks = bricks.items()
    bricks = list(itertools.chain.from_iterable(map(lambda x: [(b, x[0]) for b in x[1]], bricks)))
    bricks.sort(key = lambda x: x[0].zRange[0])

    bricksPerLevel = []
    for i, brickGroup in itertools.groupby(bricks, key = lambda x: x[0].zRange[0]):
        bricksPerLevel.append((i, list(brickGroup)))

    return bricksPerLevel

def countMovableBricks(bricksPerLevel, bricksDict):

    n = 0

    for i, (level, bricks) in enumerate(bricksPerLevel[:-1]):
        nextLevel, nextBricks = bricksPerLevel[i + 1]
        
        for currentBrick, currentBrickId in bricks:
            if max(map(lambda x: x.zRange[0], bricksDict[currentBrickId])) != level:
                continue
            
            bricksInNextLevelThatCrossCurrentBrick = list(filter(lambda nextBrick: nextBrick[1] != currentBrickId, filter(lambda nextBrick: isSquaresCrossing(nextBrick[0], currentBrick), nextBricks)))
            if len(bricksInNextLevelThatCrossCurrentBrick) == 0:
                n += 1
                continue

            allBricksButCurrent = filter(lambda b: b[0] != currentBrick, bricks)
            for b in allBricksButCurrent:
                if any(isSquaresCrossing(b[0], n[0]) for n in bricksInNextLevelThatCrossCurrentBrick):
                    n += 1
                    continue
    return n + len(bricksPerLevel[-1][1])

def main():
    lines = map(lambda x: x.strip(), file.readlines())
    lines = map(brickLineToBrick, lines)
    bricks = list(lines)
    bricks.sort(key = lambda b: b.zRange[0])

    _, bricks = placeBricks(bricks)

    bricksPerLevel = bricksToBricksPerLevel(bricks)

    solution = countMovableBricks(bricksPerLevel, dict(bricks))

    print(solution)

if __name__ == '__main__':
    main()