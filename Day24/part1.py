import sys
import itertools

class Hailstone:

    def __init__(self, positionVec, velocityVec):
        self.position = positionVec
        self.velocity = velocityVec

    def fromLine(line):
        return Hailstone(*map(lambda x: tuple(map(lambda y: int(y.strip()), x.split(','))), map(lambda x: x.strip(), line.split("@"))))

    def __repr__(self):
        return f'({self.position}, {self.velocity})'

def intersectionPoint(h1, h2):
    (x1, y1, _), (vx1, vy1, _) = h1.position, h1.velocity
    (x2, y2, _), (vx2, vy2, _) = h2.position, h2.velocity

    avx1, avx2, avy1, avy2 = abs(vx1), abs(vx2), abs(vy1), abs(vy2)
    if max(vx1, vx2) % min(vx1, vx2) == 0 and max(vy1, vy2) % min(vy1, vy2) == 0:
        return None

    dx, dy = x1 - x2, y1 - y2
    dvx, dvy = vx1 - vx2, vy1 - vy2

    breakpoint()
    gky = lambda : -(dy / dvy)
    gkx = lambda : -(dx / dvx)

    if dvy == 0:
        k = gkx()
    elif dvx == 0:
        k = gky()
    else:
        if abs(gky() - gkx()) > 10e-6:
            return None
        k = gkx()
    return (x1 + k * dvx, y1 + k * dvy)

def solvePart1(lines):
    # minPoint, maxPoint = 200000000000000, 400000000000000
    minPoint, maxPoint = 7, 27
    def inRange(x, y):
        return x >= minPoint and y >= minPoint and x <= maxPoint and y <= maxPoint 

    hailStones = list(map(Hailstone.fromLine, lines))
    hailStonesPairs = ((hailStones[x], hailStones[y]) for y in range(len(hailStones)) for x in range(len(hailStones)) if x != y)
    intersections = map(lambda x: (x, intersectionPoint(*x)), hailStonesPairs)
    filtered = filter(lambda x: x[1] != None, intersections)
    hailStonesCombinationIntersectionPointsInRangeGenerator = map(lambda x: x, filter(lambda x: inRange(*x[1]), filtered))

    return list(hailStonesCombinationIntersectionPointsInRangeGenerator)
def main():
    with open(sys.argv[1]) as fd:
        lines = list(map(lambda x: x.strip(), fd.readlines()))
    
    solution = solvePart1(lines)
    print(solution)

if __name__ == '__main__':
    print(intersectionPoint(Hailstone((19, 13, 30), (-2, 1, -2)), Hailstone((18, 19, 22), (-1, -1, -2))))
    # main()