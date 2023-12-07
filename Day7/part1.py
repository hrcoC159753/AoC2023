from collections import Counter
from enum import Enum
from random import shuffle

class Strenght(Enum):
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

def strengthToDetectionPredicate(strength):

    if strength == Strenght.FiveOfAKind:
        return lambda counts: len(counts) == 1 and counts[0] == 5
    elif strength == Strenght.FourOfAKind:
        return lambda counts: len(counts) == 2 and any(map(lambda x: x == 4, counts)) 
    elif strength == Strenght.FullHouse:
        return lambda counts: len(counts) == 3 and any(map(lambda x: x == 3, counts)) and any(map(lambda x: x == 2, counts)) 
    elif strength == Strenght.ThreeOfAKind:
        return lambda counts: len(counts) == 3 and any(map(lambda x: x == 3, counts)) 
    elif strength == Strenght.TwoPair:
        return lambda counts: len(counts) == 3 and any(map(lambda x: x == 2, counts)) 
    elif strength == Strenght.OnePair:
        return lambda counts: len(counts) == 4 and any(map(lambda x: x == 2, counts)) 
    elif strength == Strenght.HighCard:
        return lambda counts: len(counts) == 5 and all(map(lambda x: x == 1, counts)) 
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
        return 10 - int(cardStrength)
    else:
        assert False, f'{cardStrength}'

with open('input1.txt') as fd:
    lines = fd.readlines()

cardsAndBids = [(line.split(" ")[0].strip(), int(line.split(" ")[1].strip())) for line in lines]

def cardsToStrenght(cards):
    assert len(cards) == 5

    counts = Counter(cards).values()
    
    try:
        assignedStrength = next(strength for strength in Strenght if strengthToDetectionPredicate(strength)(counts))
    except:
        assert False

    return assignedStrength

cardsStrengthBid = [(cardsToStrenght(cards), cards, bid) for (cards, bid) in cardsAndBids]
shuffle(cardsStrengthBid)

def getTuple(csb):
    t = ( 
        csb[0],
        mapCardStrengthToNumber(csb[1][0]),
        mapCardStrengthToNumber(csb[1][1]),
        mapCardStrengthToNumber(csb[1][2]), 
        mapCardStrengthToNumber(csb[1][3]), 
        mapCardStrengthToNumber(csb[1][4])
    )
    print("tuple: ", t)
    return t

print(cardsStrengthBid)
sortedList = sorted(
    cardsStrengthBid,
    key = lambda csb: getTuple(csb)
)
print(sortedList)