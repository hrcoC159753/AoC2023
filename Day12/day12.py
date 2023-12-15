import sys
import functools
import re

pattern = re.compile('\#+')
secondPattern = re.compile('[\#|\?]+')

def main():

    with open(sys.argv[1]) as fd:
        lines = fd.readlines()

    def toGroupSet(example):
        (line, groupNumbers) = example
        lineSpans = getLineSpans(line, groupNumbers)
        lineGroups = getLineGroups(line)
        groups = list(map(lambda x: Group(x[0], x[1], groupNumbers), map(lambda x : (x, getLocalizedSpansForGroup(x, lineSpans)), lineGroups)))

        return Groups(groups)

    lines = map(lambda x: x.strip(), lines)
    inputData = list(map(lambda x: (x[0], [int(i) for i in x[1].split(',')]), map(lambda x : x.split(' '), lines)))
    lineInput = list(map(lambda x: (toGroupSet(x), x[1]), inputData))
    solutions = list(zip(map(lambda data: data[0]([i for i in range(len(data[1]))]), lineInput), inputData))

    for (i, (s, d)) in enumerate(solutions, start = 1):
        print(f'{i}: {d} -> {s}')

    solution = sum(map(lambda x: x[0], solutions))

    print(f'Solution: {solution}')

@functools.lru_cache
def myCombinations(k, q):
    assert k >= 0

    if k < 0:
        assert q > 0

    if k == 0:
        return 1
    elif k == 1:
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

def getLineSpans(line, groupNumbers):
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

def getLineGroups(line):
    return [m for m in re.finditer(secondPattern, line)]

def getSpanIntersection(span1, span2):
    if span1[0] < span2[0] and span1[1] < span2[0] or span1[0] > span2[1] and span1[1] > span2[1]:
        return None
    
    if span1[0] >= span2[0] and span1[1] <= span2[1]:
        return (span1[0], span1[1])
    elif span1[0] >= span2[0] and span1[1] > span2[1]:
        return (span1[0], span2[1])
    elif span1[0] < span2[0] and span1[1] <= span2[1]:
        return (span2[0], span1[1])
    elif span1[0] <= span2[0] and span1[1] >= span2[1]:
        return (span2[0], span2[1])

def realSubsetOf(maybeSubset, s):
    return maybeSubset[0] >= s[0] and maybeSubset[1] <= s[1]

def getLocalizedSpansForGroup(groupMatch, lineSpans):
    groupSpan = (groupMatch.span()[0], groupMatch.span()[1] - 1)

    returns = []
    for span in lineSpans:
        intersection = getSpanIntersection(groupSpan, span)
        if intersection != None:
            returns.append((intersection[0] - groupMatch.start(), intersection[1] - groupMatch.start()))
        else:
            returns.append(None)

    return returns

def generateSubsets(span, subsetSize):
    spanSize = (span[1] - span[0]) + 1 
    
    if spanSize < subsetSize:
        return

    effectiveSpanSize = spanSize - subsetSize + 1

    for i in range(effectiveSpanSize):
        yield (span[0] + i, span[0] + i + (subsetSize - 1))

def calculateGroupWithHashes(groupLine, groupSpans, groupNumbers, givenNumberIndexes, searchRange):
    assert any(c == '#' for c in groupLine[searchRange[0]: searchRange[1]])
    assert len(groupSpans) == len(groupNumbers)
    
    if len(givenNumberIndexes) == 0:
        return 0
    currentNumberIndex = givenNumberIndexes[0]
    currentNumber = groupNumbers[currentNumberIndex]
    currentNumberSpan = groupSpans[currentNumberIndex]

    if currentNumberSpan == None:
        return 0

    if currentNumberSpan[0] < searchRange[1]:
        currentNumberSpan = (searchRange[0], currentNumberSpan[1])
        if currentNumberSpan[1] < currentNumberSpan[0]:
            return 0
    
    m = re.search(pattern, groupLine[searchRange[0]: searchRange[1]])
    matchedSpan = (searchRange[0] + m.span()[0], searchRange[0] + m.span()[1] - 1)
    assert m != None

    allRealSubsets = list(filter(lambda x: realSubsetOf(matchedSpan, x), generateSubsets(currentNumberSpan, currentNumber)))
    if len(allRealSubsets) == 0:
        return 0

    s = 0
    for realSubset in allRealSubsets:
        previousNumberOfGroups = sum(1 for e in range(len(groupNumbers[:currentNumberIndex])) if groupSpans[e] != None)
        sumOfNumbersOfPreviousGroups = sum(e for (i, e) in enumerate(groupNumbers[:currentNumberIndex]) if groupSpans[i] != None)
        effectiveSizeOfPreviousSpan = (realSubset[0] - 1) - (sumOfNumbersOfPreviousGroups - previousNumberOfGroups)

        if previousNumberOfGroups < 0 and effectiveSizeOfPreviousSpan <= 0:
            return 0
        
        q = effectiveSizeOfPreviousSpan
        k = previousNumberOfGroups

        coef = myCombinations(k, q)

        if realSubset[1] + 2 >= len(groupLine):
            newSearchRange = (len(groupLine), len(groupLine))
        else:
            newSearchRange = (realSubset[1] + 2, len(groupLine))
        if '#' in groupLine[newSearchRange[0]: newSearchRange[1]]:
            s += calculateGroupWithHashes(groupLine, groupSpans, groupNumbers, givenNumberIndexes[1:], newSearchRange)
        else:
            s += calculateGroupWithoutHashes(groupLine, groupNumbers, givenNumberIndexes[1:], newSearchRange)
    return s

def calculateGroupWithoutHashes(groupLine, groupNumbers, givenNumberIndexes, searchRange):
    assert all(c == '?' for c in groupLine[searchRange[0]: searchRange[1]]), f'{groupLine}'
    transformedGroupLength = len(groupLine[searchRange[0]: searchRange[1]]) - (sum(groupNumbers[i] for i in givenNumberIndexes) - len(givenNumberIndexes))
    q = transformedGroupLength
    k = len(givenNumberIndexes)
    
    if q <= 0 and k != 0:
        return 0
    else:
        return myCombinations(k, q)

def getIterationLists(indexes):
    data = []
    for i in range(len(indexes) + 1):
        data.append((indexes[:i], indexes[i:]))
    return data


def recurseGroups(groups, givenIndexes):
    data = getIterationLists(givenIndexes)

    if len(groups) == 0 and len(givenIndexes) > 0:
        return 0
    elif len(groups) == 0 and len(givenIndexes) == 0:
        return 1

    currentGroup = groups[0]

    s = 0
    for (inputData, restData) in data:
        newFactor = currentGroup(inputData)
        if newFactor != 0:
            r = newFactor * recurseGroups(groups[1:], restData)
            s += r

    return s

class Groups:
    def __init__(self, groups):
        self.groups = groups

    def __call__(self, givenIndexes):        
        return recurseGroups(self.groups, givenIndexes)
            


class Group:

    def __init__(self, matcher, groupSpans, groupNumbers):
        self.matcher = matcher
        self.groupSpans = groupSpans
        self.groupNumbers = groupNumbers

    def __call__(self, groupIndexes):
        groupStr = self.matcher.group()
        hashGroupMatchers = [m for m in re.finditer(pattern, groupStr)]

        if len(hashGroupMatchers) == 0:
            return calculateGroupWithoutHashes(groupStr, self.groupNumbers, groupIndexes, (0, len(groupStr)))
        else:
            return calculateGroupWithHashes(groupStr, self.groupSpans, self.groupNumbers, groupIndexes, (0, len(groupStr)))
    
    def __repr__(self):
        return f'{repr(self.matcher), repr(self.groupSpans)}'

def testingExamples(example):
    (line, groupNumbers) = example

    print(example)
    lineSpans = getLineSpans(line, groupNumbers)
    print(lineSpans)
    lineGroups = getLineGroups(line)
    print(lineGroups)
    groups = list(map(lambda x: Group(x[0], x[1], groupNumbers), map(lambda x : (x, getLocalizedSpansForGroup(x, lineSpans)), lineGroups)))
    print(groups)

    groupSets = Groups(groups)

    allIndexes = [i for i in range(len(groupNumbers))]

    solution = groupSets(allIndexes)

    print(solution)

def test():
    # f = myCombinations
    # for q in range(1, 10 + 1):
    #     for k in range(1, 10 + 1):
    #         print(f' f(k = {k}, q = {q}) = {f(k, q)} ', end = '')
    #     print()

    examples = [
        # ('???.###', [1, 1, 3]),
        # ('.??..??...?##.', [1, 1, 3]),
        # ('?#?#?#?#?#?#?#?', [1, 3, 1, 6]),
        # ('????.#...#...', [4, 1, 1]),
        # ('????.######..#####.', [1, 6, 5]),
        ('?###????????', [3, 2, 1]),
    ]

    for example in examples:
        testingExamples(example)
        print()

if __name__ == '__main__':
    main()
    # test()