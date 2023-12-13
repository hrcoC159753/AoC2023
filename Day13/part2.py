import sys
import itertools

def equal(range1, range2):
    for (e1, e2) in zip(range1, range2):
        if e1 != e2:
            return False
    return True

def equalWithSmudge(range1, range2):
    smudge = 1
    for (e1, e2) in zip(range1, range2):
        if e1 != e2:
            smudge -= 1
    if smudge == 0:
        return True
    else:
        return False

def getColumn(paragraph, i):
    return (paragraph[k][i] for k in range(len(paragraph)))

def searchSameRows(paragraph):
    firstRange, secondRange = range(len(paragraph)), range(1, len(paragraph))
    indexes = []
    for (i, j) in zip(firstRange, secondRange):
        if equal(paragraph[i], paragraph[j]):
            indexes.append((False, (i, j)))
        elif equalWithSmudge(paragraph[i], paragraph[j]):
            indexes.append((True, (i, j)))
    return indexes

def searchSameColumns(paragraph):
    indexes = []
    firstRange, secondRange = range(len(paragraph[0])), range(1, len(paragraph[0]))
    for (i, j) in zip(firstRange, secondRange):
        if equal(getColumn(paragraph, i), getColumn(paragraph, j)):
            indexes.append((False, (i, j)))
        elif equalWithSmudge(getColumn(paragraph, i), getColumn(paragraph, j)):
            indexes.append((True, (i, j)))
    return indexes

def solveHortizontalReflection(paragraph):
    indexes = searchSameRows(paragraph)
    print(indexes)
    if len(indexes) == 0:
        return 0

    for indexPair in indexes:
        (usedSmudge, (i, j)) = indexPair
        smudge = 0 if usedSmudge else 1
        for k in itertools.count(start = 1):
            nI, nJ = i - k, j + k
            if nI == -1 or nJ == len(paragraph):
                break
            if not equal(paragraph[nI], paragraph[nJ]):
                if equalWithSmudge(paragraph[nI], paragraph[nJ]):
                    if smudge == 1:
                        smudge = 0
                    else:
                        smudge = -1
                        break
                else:
                    smudge = -1
                    break
        if smudge == 0:
            return i + 1
    return 0

def solveVerticalReflection(paragraph):
    indexes = searchSameColumns(paragraph)
    print(indexes)
    if len(indexes) == 0:
        return 0

    for indexPair in indexes:
        (usedSmudge, (i, j)) = indexPair
        smudge = 0 if usedSmudge else 1
        for k in itertools.count(start = 1):
            nI, nJ = i - k, j + k
            if nI == -1 or nJ == len(paragraph[0]):
                break
            if not equal(getColumn(paragraph, nI), getColumn(paragraph, nJ)):
                if equalWithSmudge(getColumn(paragraph, nI), getColumn(paragraph, nJ)):
                    if smudge == 1:
                        smudge = 0
                    else:
                        smudge = -1
                        break
                else:
                    smudge = -1
                    break
        if smudge == 0:
            return i + 1
    return 0


def main():

    with open(sys.argv[1]) as fd:
        text = fd.read()

    paragraphs = text.split('\n\n')
    paragraphs = map(lambda x: x.split('\n'), paragraphs)

    s = 0
    for (i, paragraph) in enumerate(paragraphs):
        v = solveVerticalReflection(paragraph)
        h = solveHortizontalReflection(paragraph)
        print(f'{i}: v -> {v}, h -> {h}, r -> {v + 100 * h}')
        s += v + 100 * h 

    print(s)


if __name__ == '__main__':
    main()