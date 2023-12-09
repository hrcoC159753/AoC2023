import sys
from itertools import tee

def window(iterable, size):
    iters = tee(iterable, size)
    for i in range(1, size):
        for each in iters[i:]:
            next(each, None)
    return zip(*iters)

def getNextLine(numbers):
    newLine = []
    for each in window(numbers, 2):
        newLine.append(each[1] - each[0])

    return newLine

def solveOneLine(numbers):
    
    # print(f'numbers: {numbers}')

    results = [numbers[0]]

    newLine = getNextLine(numbers)
    while any(map(lambda x: x != 0, newLine)):
        results.append(newLine[0])
        newLine = getNextLine(newLine)
        # print(newLine, results)

    # print(results)
    result = 0
    for e in reversed(results):
        result = e - result

    # print(result)
    return result

def main():

    with open(sys.argv[1]) as fd:
        lines = list(map(lambda x: x.strip(), fd.readlines()))
    
    numbersInLine = list(map(lambda l: [int(e) for e in l], map(lambda x: x.split(' '), lines)))

    solution = 0
    for numbers in numbersInLine:
        solution += solveOneLine(numbers)

    print(solution)
    

if __name__ == '__main__':
    main()