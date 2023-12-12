import sys
import re
import itertools

def isPossiblyValid(line, groupCounts):
    pattern = re.compile('\#+')
    
    for (match, groupCount) in zip(re.finditer(pattern, line), groupCounts):
        if len(match.group()) > groupCount and '?' not in line[:match.start()]:
            return False
    return True

def isValid(line, groupCounts):
    pattern = re.compile('\#+')
    matches = [match for match in pattern.finditer(line)]

    if len(matches) != len(groupCounts) or any(e == '?' for e in line):
        return False

    for (match, groupCount) in zip(matches, groupCounts):
        if len(match.group()) != groupCount:
            return False
    return True

def countWays(line, groupCounts):
    print(f'{line}: {isValid(line, groupCounts)}')
    if isValid(line, groupCounts):
        return 1
    
    if not isPossiblyValid(line, groupCounts):
        return 0
            
    count = 0
    lineArray = [e for e in line]
    try:
        index = lineArray.index('?')
    except:
        return 0
    lineArray[index] = '#'
    c = countWays(''.join(lineArray), groupCounts)
    lineArray[index] = '.'
    c += countWays(''.join(lineArray), groupCounts)
    count += c
    return count

def fillIndexes(line, indexes):
    return ''.join(e if i not in indexes else '#' for (i, e) in enumerate(line))

def countWays2(line, groupCounts):

    indexes = [i for i, ltr in enumerate(line) if ltr == '?']
    countOfHashes = line.count('#')

    line = ''.join(e if e == '#' else '.' for e in line)

    t = sum(groupCounts)
    return sum(map(lambda _: 1, filter(lambda x: isValid(x, groupCounts), map(lambda x: fillIndexes(line, x), itertools.combinations(indexes, t - countOfHashes)))))
    

def main():
    with open(sys.argv[1]) as fd:
        lines = fd.readlines()
    
    lines = list(map(lambda x: (x[0], [int(e) for e in x[1].split(',')]), map(lambda x: x.split(' '), map(lambda x: x.strip(), lines))))

    def peek(x):
        print(x)
        return x

    solutions = map(lambda line: countWays2(line[0], line[1]), map(peek, lines))
    # for (line, solution) in zip(lines, solutions):
    #     print(f'{line}: {solution}')

    solution = sum(solutions)
    print(solution)

if __name__ == '__main__':
    assert isValid('#.#.###', [1,1,3])
    assert isPossiblyValid('#?#.###', [1,1,3])
    assert isPossiblyValid('???.###', [1,1,3])
    assert not isPossiblyValid('....###', [1,1,3])
    assert isPossiblyValid('#.?##.?', [1,3,1])
    assert isValid('#.###.#', [1,3,1])

    main()