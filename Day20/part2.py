import sys
import itertools
import enum
import re

class Pulse(enum.Enum):
    High = 0
    Low = 1

class State(enum.Enum):
    On = 0
    Off = 1

class FilpFlop:
    def __init__(self, name, output, inputs):
        self.previousState: State = None
        self.currentState: State = State.Off
        self.output: chr = output
        self.name = name
    
    def ping(self, pulse: Pulse, source: str) -> None:
        self.previousState = self.currentState
        if pulse == Pulse.Low:
            self.currentState = State.Off if self.currentState == State.On else State.On
    
    def pulse(self):
        if self.previousState != self.currentState:
            if self.currentState == State.On:
                return (self.name, Pulse.High, self.output)
            else:
                return (self.name, Pulse.Low, self.output)
        return None

    def state(self):
        return self.currentState

    def __repr__(self):
        return f'(FilpFlop: {self.name}, {self.currentState}, {self.output})'

class Broadcaster:
    def __init__(self, name, output, inputs):
        self.output: chr = output
        self.returnValue = None
        self.name = name
    
    def ping(self, pulse: Pulse, source: str) -> None:
        self.returnValue = (self.name, pulse, self.output)
    
    def pulse(self):
        return self.returnValue

    def __repr__(self):
        return f'(Broadcaster: {self.name}, {self.returnValue}, {self.output})'

    def state(self):
        return None


class Conjunction:
    def __init__(self, name, output, inputs):
        self._state = {i : Pulse.Low for i in inputs}
        self.output: chr = output
        self.name = name
    
    def ping(self, pulse: Pulse, source: str) -> None:
        self._state.update({source: pulse})
    
    def pulse(self):
        if all(value == Pulse.High for value in self._state.values()):
            return (self.name, Pulse.Low, self.output)
        else:
            return (self.name, Pulse.High, self.output)

    def __repr__(self):
        return f'(Conjunction: {self.name}, {self._state}, {self.output})'

    def state(self):
        return tuple(self._state.values())


class Button:
    def __init__(self, name, output, inputs):
        self.output = output
        self.name = name
    
    def ping(self, pulse: Pulse, source: str) -> None:
        pass

    def pulse(self):
        return (self.name, Pulse.Low, self.output)

    def __repr__(self):
        return f'(Button: {self.name}, {self.output})'

    def state(self):
        return None

stringToModuleMapping = {
    re.compile('(button)')      : Button        ,
    re.compile('(broadcaster)') : Broadcaster   ,
    re.compile('\%(.+)')        : FilpFlop      ,
    re.compile('\&(.+)')        : Conjunction   ,
}

def stringToModule(moduleInfo, moduleInfos):
    (string, output) = moduleInfo
    (module, match) = next(filter(lambda x: x[1] != None, map(lambda x: (x[1], re.match(x[0], string)), stringToModuleMapping.items())))
    inputs = [name[1:] if (name[0] == '%' or name[0] == '&') else name for (name, output) in moduleInfos if output == match.group(1)]
    return module(match.group(1), output, inputs)


file = sys.stdin
# file = open('Day20/input1.txt')

def main():
    lines = (line for line in file)
    lines = map(lambda line: line.strip(), lines)
    lines = map(lambda line: line.split(' -> '), lines)
    lines = map(lambda lineSplit: (lineSplit[0], [e.strip() for e in lineSplit[1].split(',')]), lines)
    lines = map(lambda mapping: itertools.product([mapping[0]], [e for e in mapping[1]]), lines)
    lines = itertools.chain.from_iterable(lines)
    moduleInfos = list(lines)
    modules = map(lambda moduleInfo: stringToModule(moduleInfo, moduleInfos), moduleInfos)
    modules = list(modules)
    
    button = Button('button', 'broadcaster', [])
    modules.insert(0, button)

    numberOfPressesUntilRx = None
    numberOfButtonPresses = 0
    while True:
        q = []

        button.ping(Pulse.Low, None)
        numberOfButtonPresses += 1
        # print(f'Press: {numberOfButtonPresses}')
        q.append(button.pulse())
        while len(q) > 0:
            (name, pulse, outputName) = q.pop(0)

            if outputName == 'rx':
                if pulse == Pulse.Low:
                    numberOfPressesUntilRx = numberOfButtonPresses
                    break

            modulesWithName = list(filter(lambda m: m.name == outputName, modules))

            for module in modulesWithName:
                module.ping(pulse, name)
            for module in modulesWithName:
                newPulseInfo = module.pulse()
                if newPulseInfo != None:
                    q.append(newPulseInfo)
        
        if numberOfPressesUntilRx != None:
            break            

    solution = numberOfPressesUntilRx

    print(solution)

if __name__ == '__main__':
    main()