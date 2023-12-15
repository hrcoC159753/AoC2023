import itertools
import sys

def myHash(x):
    s = 0
    for c in x:
        s += ord(c)
        s *= 17
        s %= 256
    return s

def main():
    with open(sys.argv[1]) as fd:
        lines = fd.readlines()

    assert len(lines) == 1

    lines = list(map(lambda x: x.strip(), lines[0].split(',')))

    solutions = map(lambda x: myHash(x), lines)
    solution = sum(solutions)
    print(solution)

if __name__ == '__main__':
    main()