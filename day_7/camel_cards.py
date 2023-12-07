from enum import IntEnum
from collections import Counter

class Card(IntEnum):
    ACE   = 0,
    KING  = 1,
    QUEEN = 2,
    JACK  = 3,
    TEN   = 4,
    NINE  = 5,
    EIGHT = 6,
    SEVEN = 7,
    SIX   = 8,
    FIVE  = 9,
    FOUR  = 10,
    THREE = 11,
    TWO   = 12,
    JOKER = 13,

D = {
    'A' : Card.ACE,
    'K' : Card.KING,
    'Q' : Card.QUEEN,
    'J' : Card.JACK,
    'T' : Card.TEN,
    '9' : Card.NINE,
    '8' : Card.EIGHT,
    '7' : Card.SEVEN,
    '6' : Card.SIX,
    '5' : Card.FIVE,
    '4' : Card.FOUR,
    '3' : Card.THREE,
    '2' : Card.TWO   
}

D_Joker = {
    'A' : Card.ACE,
    'K' : Card.KING,
    'Q' : Card.QUEEN,
    'T' : Card.TEN,
    '9' : Card.NINE,
    '8' : Card.EIGHT,
    '7' : Card.SEVEN,
    '6' : Card.SIX,
    '5' : Card.FIVE,
    '4' : Card.FOUR,
    '3' : Card.THREE,
    '2' : Card.TWO,
    'J' : Card.JOKER 
}

class Hand(IntEnum):
    FIVE    = 0,
    FOUR    = 1,
    HOUSE   = 2,
    THREE   = 3,
    TWOPAIR = 4,
    PAIR    = 5,
    HIGH    = 6

with open('input') as input:
    text = input.read()
    games = text.split('\n')[:-1]

def classify(hand):
    cards = sorted(Counter(hand).values(), reverse=True)
    match hand:
        case str(s) if cards[0] == 5:
            return Hand.FIVE
        case str(s) if cards[0] == 4:
            return Hand.FOUR
        case str(s) if cards[0] == 3 and cards[1] == 2:
            return Hand.HOUSE
        case str(s) if cards[0] == 3:
            return Hand.THREE
        case str(s) if cards[0] == 2 and cards[1] == 2:
            return Hand.TWOPAIR
        case str(s) if cards[0] == 2:
            return Hand.PAIR
        case str(s):
            return Hand.HIGH

def parse_joker(hand: str):
    if hand.count('J') > 0:
        return [h for c in ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2'] for h in parse_joker(hand.replace('J', c, 1))]
    else:
        return [hand]

def classify_joker(hand):
    return min([classify(h) for h in parse_joker(hand)])

games_simple = [game.split(' ') for game in games]
games_simple = [(classify(hand), list(map(D.get, hand)), int(bid)) for hand, bid in games_simple]
games_simple.sort(key=lambda x: (int(x[0]), x[1]), reverse=True)
games_simple = [(hand_type, bid) for hand_type, _, bid in games_simple]

simple_value = 0
for i in range(len(games_simple)):
    simple_value += (i+1) * games_simple[i][1]

games_complex = [game.split(' ') for game in games]
games_complex = [(classify_joker(hand), list(map(D_Joker.get, hand)), int(bid)) for hand, bid in games_complex]
games_complex.sort(key=lambda x: (int(x[0]), x[1]), reverse=True)
games_complex = [(hand_type, bid) for hand_type, _, bid in games_complex]

complex_value = 0
for i in range(len(games_complex)):
    complex_value += (i+1) * games_complex[i][1]

with open('output', 'w') as output:
    output.write(str(simple_value) + '\n')
    output.write(str(complex_value) + '\n')