import sys

from itertools import cycle
from threading import Thread
import math

class ThreadWithReturnValue(Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def thread_function(firstLine, currentMapping, mappings):
    result = -1
    for (i, e) in enumerate(cycle(firstLine)):
        mappingPair = mappings[currentMapping]
        assert e == 'L' or e == 'R', f'{e}'
        
        currentMapping = mappingPair[0] if e == 'L' else mappingPair[1]
        
        if currentMapping[-1] == 'Z':
            result = i + 1
            break
    return result

def main():

    with open(sys.argv[1]) as fd:
        lines = fd.readlines()

    lines = list(filter(lambda x: len(x) != 0, map(str.strip, lines)))

    firstLine = lines[0]
    mappings = dict(map(lambda x: (x[0], (x[1][0], x[1][1])), map(lambda x: (x[0], x[1][1:-1].split(", ")), map(lambda x: x.split(' = '), lines[1:]))))

    currentMappings = list(filter(lambda x: x[-1] == 'A', mappings.keys()))
    print(f'{currentMappings}')

    threads = []
    for currentMapping in currentMappings:
        threads.append(ThreadWithReturnValue(target = thread_function, args = (firstLine, currentMapping, mappings)))

    for thread in threads:
        thread.start()

    results = []
    for thread in threads:
        results.append(thread.join())

    print(results)
    result = math.lcm(*results)
    print(result)


if __name__ == '__main__':
    main()