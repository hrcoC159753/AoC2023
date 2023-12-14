import sys

def main():

    with open(sys.argv[1]) as fd:
        lines = fd.readlines()

    lines = list(map(lambda x: x.strip(), lines))


    print(len(lines), len(lines[0]))

    assert all(len(lines[0]) == len(line) for line in lines[1:])

    s = 0
    for j in range(len(lines[0])):
        c = len(lines)
        for (i, e) in enumerate(range(len(lines), 0, -1)):
            if lines[i][j] == 'O':
                s += c
                c -= 1
            elif lines[i][j] == '#':
                c = e - 1

    print(s)

if __name__ == '__main__':
    main()