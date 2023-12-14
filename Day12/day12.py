import sys
import functools
import re

pattern = re.compile('\#+')

def main():

    with open(sys.argv[1]) as fd:
        lines = fd.readlines()

    lines = map(lambda x: x.strip(), lines)
    inputData = list(map(lambda x: (x[0], [int(i) for i in x[1].split(',')]), map(lambda x : x.split(' '), lines)))

    print(inputData)


@functools.lru_cache
def myCombinations(k, q):
    assert k > 0
    assert q > 0

    if k == 1:
        return q
    elif q == 1 or q == 2:
        return 0
    else:
        s = sum(myCombinations(k - 1, i) for i in range(1, q-2 + 1))
        return s

def combinationsGen(lineGroup, groupNumbers):
    hashIndexes = [i for (i, e) in enumerate(lineGroup) if e == '#']

    lineGroupLength = len(lineGroup)
    newLineArray = ['*' * n for n in groupNumbers]
    newLineArray = '.'.join(newLineArray)
    if len(newLineArray) > len(lineGroup):
        return
    newLineArray = newLineArray + '.' * (len(lineGroup) - len(newLineArray))
    groupIndexes = [m.start() for m in re.finditer(pattern, newLineArray)]
    
    assert len(groupIndexes) == len(groupNumbers)
    newLineArray = newLineArray.split()

    yield ''.join(newLineArray)

    pickedIndex = -1
    for i in range(len(groupIndexes) - 1, -1, -1):
        if groupIndexes[i] + groupNumbers[i] >= len(newLineArray):
            pickedIndex = i
            break

def getGroupSpans(line, groupNumbers):
    assert sum(groupNumbers) + len(groupNumbers) - 1 <= len(line)
    
    leftIndexes = []
    i = 0
    for groupNumber in groupNumbers:
        leftIndexes.append(i)
        i += groupNumber + 1

    rightIndexes = []
    i = 0
    for groupNumber in groupNumbers[::-1]:
        rightIndexes.append(i)
        i += groupNumber + 1

    return list((leftIndex, rightIndex) for (leftIndex, rightIndex) in zip(leftIndexes, map(lambda x: len(line) - 1 - x, rightIndexes[::-1])))

def test():
    # f = myCombinations
    # for q in range(1, 10 + 1):
    #     for k in range(1, 10 + 1):
    #         print(f' f(k = {k}, q = {q}) = {f(k, q)} ', end = '')
    #     print()

    print(getGroupSpans('?###????????', [3, 2, 1]))
    print(getGroupSpans('?###????', [3, 2, 1]))
    print(getGroupSpans('?###????????', [3, 2, 1, 1]))

if __name__ == '__main__':
    # main()
    test()