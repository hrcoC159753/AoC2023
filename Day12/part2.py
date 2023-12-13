import sys
import re
import itertools
import math

pattern = re.compile('\#+')
secondPattern = re.compile('[\#|\?]+')

def isPossiblyValid(line, groupCounts):
    for (match, groupCount) in zip(re.finditer(pattern, line), groupCounts):
        if len(match.group()) > groupCount and '?' not in line[:match.start()]:
            return False

    return True

def isValid(line, groupCounts):
    matches = [match for match in pattern.finditer(line)]

    if len(matches) != len(groupCounts) or any(e == '?' for e in line):
        return False

    for (match, groupCount) in zip(matches, groupCounts):
        if len(match.group()) != groupCount:
            return False
    return True

def peek(x):
    print(x)
    return x
    
def fillWithPoints(line, indexes):
    newLineArray = [e for e in line]
    for i in indexes:
        newLineArray[i] = '.'
    return ''.join(newLineArray)

def changingIndexes(matches):
    matchesLargerThenThree = filter(lambda x: len(x.group()) >= 3, matches)
    streamOfIndexListsThatPointIntoMachedRangesQuestionmarks = map(lambda x: [i for i in range(x.start(), x.end()) if x.string[i] == '?'], matchesLargerThenThree)
    return list(itertools.chain.from_iterable(streamOfIndexListsThatPointIntoMachedRangesQuestionmarks))

def printFunctionInfo(function):

    def returnFunction2(*args, **kwargs):
        print(f'{args}, {kwargs}')
        value = function(*args, **kwargs)
        print(f'Result -> {value}')
        return value

    def returnFunction(line, groupCounts, previousChangingIndexes = [], solutions = []):
        transformedLine = ''.join('.' if (i in previousChangingIndexes) else e for (i, e) in enumerate(line))
        value = function(line, groupCounts, previousChangingIndexes = previousChangingIndexes, solutions = solutions)
        print(f'{transformedLine}:{previousChangingIndexes} -> {value}')
        return value
    return returnFunction2

def isSameAs(qLine):
    def returningFunction(line):
        assert len(qLine) == len(line)
        for (c1, c2) in zip(qLine, line):
            if c1 != c2 and (c1 != '?' and c2 != '?'):
                return False
        return True
    return returningFunction

def generateIndexes(end, size):
    for i in range(1, size + 1):
        yield from itertools.combinations(range(0, end), i)

def transformWithIndexes(line, indexes):
    return ''.join('.' if (i in indexes) else e for (i, e) in enumerate(line))

def check(x):
    return True

def fitDebug(fitFunciton):

    def retFunc(line, span):
        value = fitFunciton(line, span)
        print(f'{line}, {span} -> {value}')
        return value
    return retFunc

@fitDebug
def fit(line, span):
    assert span[0] >= 0
    assert span[0] <= len(line) - 1
    assert span[1] >= 0
    assert span[1] <= len(line) - 1
    assert span[0] <= span[1]

    for c in line[span[0]: span[1] + 1]:
        if c != '?' and c != '#':
            return None
    size = span[1] - span[0] + 1
    buff = '#' * size
    if span[0] != 0:
        if line[span[0] - 1] == '.' or line[span[0] - 1] == '?':
            buff = '.' + buff
            span = (span[0] - 1, span[1])
        else:
            return None
    if span[1] != len(line) - 1:
        if line[span[1] + 1] == '.' or line[span[1] + 1] == '?':
            buff = buff + '.'
            span = (span[0], span[1] + 1)
        else:
            return None
    return line[:span[0]] + buff + line[span[1] + 1:]


@printFunctionInfo
def countWays2(line, groupCounts, initalGroups, fittingRangeStart = 0, solutions = []):
    
    if len(groupCounts) == 0:
        if len(line) == fittingRangeStart or all(e == '.' or e == '?' for e in line[fittingRangeStart:]):
            if line in solutions:
                print(f'Duplicate: {line}')
                return 0
            else:
                print(f'New solution: {line}')
                solutions.append(line)
                return 1
        else:
            return 0    
    s = 0
    for groupCount in groupCounts:
        didFitAny = False
        for i in range(fittingRangeStart, len(line)):
            if i + (groupCount - 1) >= len(line):
                continue
            f = fit(line, (i, i + (groupCount - 1)))
            if f != None:
                didFitAny = True
                s += countWays2(f, groupCounts[1:], initalGroups, fittingRangeStart = i + groupCount, solutions = solutions)
            if i == '?':
                line[i] = '.'
        if not didFitAny:
            return s   
    return s

@printFunctionInfo
def countWays(line, groupCounts, previousChangingIndexes = [], solutions = []):
    transformedLine = ''.join('.' if (i in previousChangingIndexes) else e for (i, e) in enumerate(line))
    matches = [m for m in re.finditer(secondPattern, transformedLine)]
    if len(matches) > len(groupCounts):
        return 0
    elif len(matches) < len(groupCounts):
        indexes = changingIndexes(matches)
        localPreviousChangingIndex = previousChangingIndexes[:]
        s = 0
        for changingIndex in indexes:
            if changingIndex in localPreviousChangingIndex:
                continue
            if len(localPreviousChangingIndex) > 0 and changingIndex < localPreviousChangingIndex[-1]:
                continue
            
            localPreviousChangingIndex.append(changingIndex)
            s += countWays(line, groupCounts, previousChangingIndexes = localPreviousChangingIndex, solutions = solutions)
            localPreviousChangingIndex.pop()
        return s
    else:
        p = 1
        for (match, groupCount) in zip(matches, groupCounts):
            matchLength = len(match.group())

            if matchLength < groupCount:
                return 0

            countOfHashes = match.group().count('#')
            if groupCount < countOfHashes:
                return 0
            elif groupCount == countOfHashes:
                p *= 1
                continue
            else:
                assert groupCount > countOfHashes

                numberOfQuestionmarks = matchLength - countOfHashes
                neededHashes = groupCount - countOfHashes

                if all(e == '?' for e in match.group()):
                    p *= (matchLength - neededHashes) + 1
                    continue

                (firstIndex, lastIndex) = (match.group().index('#'), match.group().rindex('#'))
                if firstIndex != lastIndex:
                    numberOfQuestionmarksInBetween = sum(1 for e in match.group()[firstIndex + 1:lastIndex] if e == '?')
                    assert numberOfQuestionmarksInBetween <= neededHashes
                    freeHashes = neededHashes - numberOfQuestionmarksInBetween
                else:
                    freeHashes = neededHashes
                (leftPadding, rightPadding) = (firstIndex, len(match.group()) - (lastIndex + 1))

                p *= ((freeHashes + 1) - (freeHashes - leftPadding) - (freeHashes - rightPadding))

        if len(solutions) > 0 and any(isSameAs(transformedLine)(x) for x in solutions):
            return 0

        solutions.append(transformedLine)
        return p

def transformLine(line):
    return ('?'.join([line[0]] * 5), list(itertools.chain.from_iterable([line[1]] * 5)))
    # return line

def main():
    with open(sys.argv[1]) as fd:
        lines = fd.readlines()
    
    lines = list(map(lambda x: (x[0], [int(e) for e in x[1].split(',')]), map(lambda x: x.split(' '), map(lambda x: x.strip(), lines))))

    # solutions = list(map(lambda line: (line, countWays(line[0], line[1])), map(transformLine, lines)))

    # solution = sum(map(lambda x: x[1], solutions))
    # solution = countWays('?#?#?#?', [1, 1, 2])
    solution = countWays2(lines[5][0], lines[5][1])
    print(solution)

if __name__ == '__main__':
    # assert fit('?#.', (0, 2)) == None
    # assert fit('?#?', (0, 2)) == '###', f"{fit('?#?', (0, 2))}"
    # assert fit('?#?.', (0, 2)) == '###.'
    # assert fit('.?#?', (0, 2)) == None
    # assert fit('.?#?', (1, 3)) == '.###'
    # assert fit('.?#?.', (0, 2)) == None
    # assert fit('.?#?.', (1, 3)) == '.###.'
    # assert fit('.?#?#', (0, 2)) == None
    # assert fit('.?#?#', (1, 3)) == None
    # assert fit('???.###', (0, 0)) == '#.?.###', f"{fit('???.###', (0, 1))}"

    transformedLine = transformLine(('.??..??...?##.', [1, 1, 3]))
    s = countWays2(transformedLine[0], transformedLine[1], transformedLine[1])
    print(s)

    # main()