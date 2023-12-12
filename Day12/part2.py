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
    return itertools.chain.from_iterable(streamOfIndexListsThatPointIntoMachedRangesQuestionmarks)

def printFunctionInfo(function):

    def returnFunction(*args, **kwargs):
        print(f'{args}, {kwargs}')
        value = function(*args, **kwargs)
        print(f'{args}, {kwargs} -> {value}')
        return value
    return returnFunction

def isSameAs(qLine):
    def returningFunction(line):
        assert len(qLine) == len(line)
        for (c1, c2) in zip(qLine, line):
            if c1 != c2 and (c1 != '?' and c2 != '?'):
                return False
        return True
    return returningFunction

@printFunctionInfo
def countWays(line, groupCounts, alreadyFoundSolutions = []):
    
    matches = [m for m in re.finditer(secondPattern, line)]
    if len(matches) > len(groupCounts):
        return 0
    elif len(matches) < len(groupCounts):
        lineArray = [e for e in line]
        s = 0
        for changingIndex in changingIndexes(matches):
            lineArray[changingIndex] = '.'
            newLine = ''.join(lineArray)
            s += countWays(newLine, groupCounts, alreadyFoundSolutions = alreadyFoundSolutions)
            lineArray[changingIndex] = '?'
        return s
    else:
        if len(alreadyFoundSolutions) > 0 and any(isSameAs(line)(solution) for solution in alreadyFoundSolutions): 
            return 0
        
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

        alreadyFoundSolutions.append(line)
        return p

def transformLine(line):
    # return ('?'.join([line[0]] * 5), list(itertools.chain.from_iterable([line[1]] * 5)))
    return line

def main():
    with open(sys.argv[1]) as fd:
        lines = fd.readlines()
    
    lines = list(map(lambda x: (x[0], [int(e) for e in x[1].split(',')]), map(lambda x: x.split(' '), map(lambda x: x.strip(), lines))))

    # solutions = list(map(lambda line: (line, countWays(line[0], line[1])), map(transformLine, lines)))

    # solution = sum(map(lambda x: x[1], solutions))
    # solution = countWays('?#?#?#?', [1, 1, 2])
    solution = countWays(lines[5][0], lines[5][1])
    print(solution)

if __name__ == '__main__':
    main()