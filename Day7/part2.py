from collections import Counter
from enum import Enum
from random import shuffle
import sys

class Strength(Enum):
    FiveOfAKind = 7
    FourOfAKind = 6
    FullHouse = 5
    ThreeOfAKind = 4
    TwoPair = 3
    OnePair = 2
    HighCard = 1

    def __lt__(self, other):
        if self.__class__ is other.__class__:
          return self.value < other.value
        return NotImplemented

def chooseWinningSubsetImpl(cards):

    assert len(cards) == 5


    freq = dict(Counter(cards))

    values = list(sorted(freq.values(), reverse = True))
    assert len(values) > 0

    if values[0] == 5:
        return (Strength.FiveOfAKind, freq)
    elif values[0] == 4 and values[1] == 1:
        return (Strength.FourOfAKind, freq)
    elif values[0] == 3 and values[1] == 2:
        return (Strength.FullHouse, freq)
    elif values[0] == 3 and values[1] == 1 and values[2] == 1:
        return (Strength.ThreeOfAKind, freq)
    elif values[0] == 2 and values[1] == 2 and values[2] == 1:
        return (Strength.TwoPair, freq)
    elif values[0] == 2 and values[1] == 1 and values[2] == 1 and values[3] == 1:
        return (Strength.OnePair, freq)
    elif values[0] == 1 and values[1] == 1 and values[2] == 1 and values[3] == 1 and values[4] == 1:
        return (Strength.HighCard, freq)

    assert False, f'{cards} {freq}'

def chooseWinningSubsetWithJockerImpl(cards):

    strengthAndFreq = chooseWinningSubsetImpl(cards)
    (strength, freq) = strengthAndFreq

    if 'J' in freq and len(freq) > 1:
        n = freq.pop('J')
        items = [[key, value] for (key, value) in sorted(freq.items(), key = lambda e: e[1], reverse = True)]

        assert len(freq) > 0, f'{cards}'

        while n > 0:
            i = 0
            if items[i][1] < 5:
                items[i][1] += 1
                n -= 1
            i += 1
        
        newFreq = dict(items)
        newCards = ''.join(map(lambda x: x[0] * x[1], newFreq.items()))
        return chooseWinningSubsetImpl(newCards)
    return strengthAndFreq

def getStrength(cards):
    return chooseWinningSubsetImpl(cards)[0]

def getStrengthWithJocker(cards):
    return chooseWinningSubsetWithJockerImpl(cards)[0]

def strengthToDetectionPredicate(strength):

    def getPredicate(length, containingNumbers):
        def isLengthCorrectAndContainsNumbers(cardFrequencies):
            counts = list(cardFrequencies.values())

            return len(counts) == length and all(map(lambda num: num in counts, containingNumbers))
        return isLengthCorrectAndContainsNumbers

    if strength == Strength.FiveOfAKind:
        return getPredicate(1, [5])
    elif strength == Strength.FourOfAKind:
        return getPredicate(2, [4])
    elif strength == Strength.FullHouse:
        return getPredicate(2, [3, 2])
    elif strength == Strength.ThreeOfAKind:
        return getPredicate(3, [3])
    elif strength == Strength.TwoPair:
        return getPredicate(3, [2])
    elif strength == Strength.OnePair:
        return getPredicate(4, [2])
    elif strength == Strength.HighCard:
        return getPredicate(5, [1])
    else:
        assert False

def mapCardStrengthToNumber(cardStrength):
    if cardStrength == 'A':
        return 14
    elif cardStrength == 'K':
        return 13
    elif cardStrength == 'Q':
        return 12
    elif cardStrength == 'J':
        return 11
    elif cardStrength == 'T':
        return 10
    elif cardStrength in '23456789':
        return int(cardStrength)
    else:
        assert False, f'{cardStrength}'

def mapCardStrengthToNumberWithJocker(cardStrength):
    if cardStrength == 'J':
        return 1
    else:
        return mapCardStrengthToNumber(cardStrength)

def cardsToStrength(cards):
    assert len(cards) == 5

    counts = Counter(cards)
    
    try:
        assignedStrength = next(strength for strength in Strength if strengthToDetectionPredicate(strength)(counts))
    except:
        assert False, f'{cards} {counts}'

    return assignedStrength

def getTuple(csb):
    t = ( 
        csb[0],
        mapCardStrengthToNumberWithJocker(csb[1][0]),
        mapCardStrengthToNumberWithJocker(csb[1][1]),
        mapCardStrengthToNumberWithJocker(csb[1][2]), 
        mapCardStrengthToNumberWithJocker(csb[1][3]), 
        mapCardStrengthToNumberWithJocker(csb[1][4])
    )
    return t
def main():
    with open(sys.argv[1]) as fd:
        lines = fd.readlines()

    cardsAndBids = [(line.split(" ")[0].strip(), int(line.split(" ")[1].strip())) for line in lines]

    cardsStrengthBid = [(getStrengthWithJocker(cards), cards, bid) for (cards, bid) in cardsAndBids]

    sortedList = sorted(
        cardsStrengthBid,
        key = lambda csb: getTuple(csb)
    )
    results = list(map(lambda x: (x[0] * x[1][2], *x[1]), enumerate(sortedList, 1)))

    print(f'Length: {len(results)}')

    resultBids = map(lambda x: x[0], results)

    print(f'FinalResult: {sum(resultBids)}')

if __name__ == '__main__':
    main()