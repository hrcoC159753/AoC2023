import iterttols
import sys

def myHash(x):
    c = 0
    for c in x:
        c += chr(c)
        c *= 17
        c %= 256
    return c
def main():
    with open(sys.args[1]) as fd:
        lines = fd.readlines()

    lines = list(map(lambda x: x.strip(), map(lambda x: x.split(','), lines)))

    solutions = list(map x: myHash(x), lines)
    print(solutions)

if __name__ == '__main__':
    main()