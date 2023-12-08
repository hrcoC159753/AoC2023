import sys

from itertools import cycle

def main():

    with open(sys.argv[1]) as fd:
        lines = fd.readlines()

    lines = list(filter(lambda x: len(x) != 0, map(str.strip, lines)))

    firstLine = lines[0]
    mappings = dict(map(lambda x: (x[0], (x[1][0], x[1][1])), map(lambda x: (x[0], x[1][1:-1].split(", ")), map(lambda x: x.split(' = '), lines[1:]))))

    currentMapping = 'AAA'
    result = -1
    for (i, e) in enumerate(cycle(firstLine)):
        mappingPair = mappings[currentMapping]
        if e == 'L':
            currentMapping = mappingPair[0]
        elif e == 'R':
            currentMapping = mappingPair[1]
        else:
            assert False, f'{currentMapping}, {e}'
        
        if currentMapping == 'ZZZ':
            result = i + 1
            break

    print(result)


if __name__ == '__main__':
    main()