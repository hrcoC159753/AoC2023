import sys
import re

from collections import Counter

def main():

    with open(sys.argv[1]) as fd:
        lines = fd.readlines()
    
    l = list(map(lambda x: int(x.split(':')[0]), lines))
    c = Counter(l)
    a = list(key for (key, value) in c.items() if value == 1)
    a = list(key for (key, value) in c.items() if value == 1)
    
    for i in lines:
        if int(i.split(':')[0]) in a:
            print(i)
    
if __name__ == '__main__':
    main()