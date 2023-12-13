import sys
import itertools

def equal(range1, range2):
    for (e1, e2) in zip(range1, range2):
        if e1 != e2:
            return False
    return True

def getColumn(paragraph, i):
    return (paragraph[k][i] for k in range(len(paragraph)))

def searchSameRows(paragraph):
    firstRange, secondRange = range(len(paragraph)), range(1, len(paragraph))
    indexes = []
    for (i, j) in zip(firstRange, secondRange):
        if equal(paragraph[i], paragraph[j]):
            indexes.append((i, j))
    return indexes

def searchSameColumns(paragraph):
    indexes = []
    firstRange, secondRange = range(len(paragraph[0])), range(1, len(paragraph[0]))
    for (i, j) in zip(firstRange, secondRange):
        if equal(getColumn(paragraph, i), getColumn(paragraph, j)):
            indexes.append((i, j))
    return indexes

def solveHortizontalReflection(paragraph):
    indexes = searchSameRows(paragraph)
    print(indexes)
    if len(indexes) == 0:
        return 0

    for indexPair in indexes:
        (i, j) = indexPair
        for k in itertools.count():
            nI, nJ = i - k, j + k
            if nI == -1 or nJ == len(paragraph):
                return i + 1
            if not equal(paragraph[nI], paragraph[nJ]):
                break
    return 0

def solveVerticalReflection(paragraph):
    indexes = searchSameColumns(paragraph)
    print(indexes)
    if len(indexes) == 0:
        return 0

    for indexPair in indexes:
        (i, j) = indexPair
        for k in itertools.count():
            nI, nJ = i - k, j + k
            if nI == -1 or nJ == len(paragraph[0]):
                return i + 1
            if not equal((paragraph[k][nI] for k in range(len(paragraph))), (paragraph[k][nJ] for k in range(len(paragraph)))):
                break
    return 0


def main():

    with open(sys.argv[1]) as fd:
        text = fd.read()

    paragraphs = text.split('\n\n')
    paragraphs = map(lambda x: x.split('\n'), paragraphs)

    s = 0
    for (i, paragraph) in enumerate(paragraphs):
        if i == 2:
            breakpoint()
        v = solveVerticalReflection(paragraph)
        h = solveHortizontalReflection(paragraph)
        print(f'{i}: v -> {v}, h -> {h}, r -> {v + 100 * h}')
        s += v + 100 * h 

    print(s)


if __name__ == '__main__':
    main()