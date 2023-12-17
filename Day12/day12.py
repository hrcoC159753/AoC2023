import sys

def countNumberOfPreviousHashes(line, lastIndex):
    if lastIndex < 0:
        return 0

    i = 0
    for c in line[lastIndex:: -1]:
        if c == '#':
            i += 1
        if c == '.':
            break
    return i

def count(line, groups, i = 0):
    # print(f'{line}, {groups}, {i}')
    if i == len(line) and len(groups) == 0:
        return 1
    
    if i == len(line) and len(groups) > 0:
        if len(groups) == 1:
            numberOfPreviousHashes = countNumberOfPreviousHashes(line, i)
            if numberOfPreviousHashes == groups[0]:
                return 1
            else:
                return 0
        else: 
            return 0

    if len(line) > i and len(groups) == 0:
        isThereHashLeft = next((True for e in line[i:] if e == '#'), False)
        return 0 if isThereHashLeft else 1

    if line[i] == '.':
        numberOfPreviousHashes = countNumberOfPreviousHashes(line, i - 1)
        if numberOfPreviousHashes > 0:
            if len(groups) == 0:
                return 0
            if numberOfPreviousHashes == groups[0]:
                return count(line, groups[1:], i = i + 1)
            else:
                return 0
        else:
            return count(line, groups, i = i + 1)
    elif line[i] == '#':
        if len(groups) == 0:
            return 0
        return count(line, groups, i = i + 1)
    elif line[i] == '?':
        dotPart = count(line[:i] + '.' + line[i + 1:], groups, i = i)
        hashPart = count(line[:i] + '#' + line[i + 1:], groups, i = i)
        return dotPart + hashPart
    else:
        assert False

    assert False

def transform(x):
    (line, numbers) = x
    return x
    # return ('?'.join([line] * 5), numbers * 5)

def main():
    with open(sys.argv[1]) as fd:
        lines = fd.readlines()
    
    lines = map(lambda x: x.strip(), lines)
    lines = map(lambda x: x.split(' '), lines)
    lines = map(lambda x: (x[0], [int(e) for e in x[1].split(',')]), lines)
    lines = map(lambda x: transform(x), lines)

    # lines = [
    #     # ('???.###', [1, 1, 3]),
    #     # ('.??..??...?##.', [1, 1, 3]),
    #     # ('?#?#?#?#?#?#?#?', [1, 3, 1, 6]),
    #     # ('????.#...#...', [4, 1, 1]),
    #     # ('????.######..#####.', [1, 6, 5]),
    #     # ('?###????????', [3, 2, 1]),
    # ]

    solution = 0
    for (i, (line, groups)) in enumerate(lines):
        s = count(line, groups)
        print(f'{i}: {line}, {groups} -> {s}')
        solution += s
    
    print(f'Solution: {solution}')

if __name__ == '__main__':
    main()