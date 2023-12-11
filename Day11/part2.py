import sys

from itertools import combinations

def printLines(lines):

    for line in lines:
        for c in line:
            print(c, end = '')
        print()

def findEmptyRowsAndColumns(lines):
    emptyRows = []
    emptyColumns = []

    for i in range(len(lines)):
        if all(c == '.' for c in lines[i]):
            emptyRows.append(i)

    for i in range(len(lines[0])):
        allDot = True
        for j in range(len(lines)):
            if lines[j][i] != '.':
                allDot = False
                break
        if allDot:
            emptyColumns.append(i)
    return (emptyRows, emptyColumns)

def expandGalaxy(lines):

    (emptyRows, emptyColumns) = findEmptyRowsAndColumns(lines)

    for emptyColumnIndex in emptyColumns[::-1]:
        for j in range(len(lines)):
            lines[j].insert(emptyColumnIndex, '.')
        
    for emptyRowIndex in emptyRows[::-1]:
        lines.insert(emptyRowIndex, '.' * len(lines[emptyRowIndex]))

    return lines

def addNumberingToGalaxies(lines):

    j = 0
    for line in lines:
        for i in range(len(line)):
            if line[i] == '#':
                line[i] = chr(ord('1') + j)
                j += 1
    return lines

def numberLocations(lines):
    for k in range(len(lines)):
        for i in range(len(lines[k])):
            if lines[k][i] != '.':
                yield (lines[k][i], (i, k))

def calculateShortestPath(loc1, loc2):
    return abs(loc2[0] - loc1[0]) + abs(loc2[1] - loc1[1])

def inBetween(e, a, b):
    if a > b:
        return b < e < a
    elif a < b:
        return b > e > a
    else:
        return False

def calculateShortestPath2(loc1, loc2, emptyRowsAndColumns, distanceMultiply = 2):
    baseSolution = calculateShortestPath(loc1, loc2)
    # breakpoint()
    (passedColumns, passedRows) = (list(filter(lambda x: inBetween(x, loc1[0], loc2[0]), emptyRowsAndColumns[1])), list(filter(lambda x: inBetween(x, loc1[1], loc2[1]), emptyRowsAndColumns[0])))
    solution = baseSolution + (distanceMultiply - 1) * (len(passedColumns) + len(passedRows))
    return solution

def main():

    with open(sys.argv[1]) as fd:
        lines = fd.readlines()

    lines = list(map(lambda x: [c for c in x], map(lambda x: x.strip(), lines)))

    assert all(len(line) == len(lines[0])for line in lines[1:]), f'{lines}'

    emptyRowsAndColumns = findEmptyRowsAndColumns(lines)
    # lines = expandGalaxy(lines)
    # printLines(lines)

    lines = addNumberingToGalaxies(lines)
    # printLines(lines)

    # print(len(list(combinations(numberLocations(lines), 2))))

    # for ((n1, loc1), (n2, loc2)) in combinations(numberLocations(lines), 2):
    #     print(f'({n1}, {loc1}) x ({n2}, {loc2})') 

    solution = sum(map(lambda x: calculateShortestPath2(x[0][1], x[1][1], emptyRowsAndColumns, distanceMultiply = 2), combinations(numberLocations(lines), 2)))
    print(solution)
    solution = sum(map(lambda x: calculateShortestPath2(x[0][1], x[1][1], emptyRowsAndColumns, distanceMultiply = 10), combinations(numberLocations(lines), 2)))
    print(solution)
    solution = sum(map(lambda x: calculateShortestPath2(x[0][1], x[1][1], emptyRowsAndColumns, distanceMultiply = 100), combinations(numberLocations(lines), 2)))
    print(solution)
    solution = sum(map(lambda x: calculateShortestPath2(x[0][1], x[1][1], emptyRowsAndColumns, distanceMultiply = 1000), combinations(numberLocations(lines), 2)))
    print(solution)
    solution = sum(map(lambda x: calculateShortestPath2(x[0][1], x[1][1], emptyRowsAndColumns, distanceMultiply = 10_000), combinations(numberLocations(lines), 2)))
    print(solution)
    solution = sum(map(lambda x: calculateShortestPath2(x[0][1], x[1][1], emptyRowsAndColumns, distanceMultiply = 100_000), combinations(numberLocations(lines), 2)))
    print(solution)
    solution = sum(map(lambda x: calculateShortestPath2(x[0][1], x[1][1], emptyRowsAndColumns, distanceMultiply = 1_000_000), combinations(numberLocations(lines), 2)))
    print(solution)

if __name__ == '__main__':
    main()