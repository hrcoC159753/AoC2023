import sys

def main():

    with open(sys.argv[1]) as fd:
        text = fd.read()

    paragraphs = text.split('\n\n')
    paragraphLines = map(lambda x: x.split('\n'), paragraphs)

    paragraphLines = list(paragraphLines)
    paragraphRows = paragraphLines[:]
    paragraphColumns = []

    for k in range(len(paragraphLines)):

        assert all(len(line) == len(paragraphLines[k][0]) for line in paragraphLines[k][1:]) 

        for i in range(len(paragraphLines[k][0])):
            column = []
            for j in range(len(paragraphLines[k])):
                column.append(paragraphLines[k][j][i])
            paragraphColumns.append(''.join(column))

    print(paragraphRows)
    print(paragraphColumns)

if __name__ == '__main__':
    main()