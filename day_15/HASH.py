
import re
from enum import Enum
from functools import reduce

with open('input') as input:
    text = input.read()

line = text.replace('\n', '')
codes = line.split(',')

class Lens:
    def __init__(self, label, power) -> None:
        self.label = label
        self.power = power
    
    def __eq__(self, __value) -> bool:
        return self.label == __value.label

    def __hash__(self) -> int:
        return self.label.__hash__()

class Box:
    def __init__(self, number) -> None:
        self.lenses : [Lens] = []
        self.number = number
    
    def remove(self, lens):
        if lens in self.lenses:
            self.lenses.remove(lens)
    
    def add(self, lens):
        if lens in self.lenses:
            i = self.lenses.index(lens)
            self.lenses[i].power = lens.power
        else:
            self.lenses.append(lens)

    def focusing_powers(self):
        number = self.number + 1
        return [number * (i+1) * int(self.lenses[i].power) for i in range(len(self.lenses))]


M = dict()     
def HASH(s : str):
    if not s in M:
        result = 0
        for c in s:
            result += ord(c)
            result *= 17
            result %= 256
        M[s] = result
    return M[s]

hash_sum = sum([HASH(code) for code in codes])

boxes = [Box(i) for i in range(256)]

for code in codes:
    groups = re.match(r'(.*)(=|-)(\d+)?', code)
    label, op = groups.group(1), groups.group(2)
    box = HASH(label)
    match op:
        case '=':
            power = groups.group(3)
            boxes[box].add(Lens(label, power))
        case '-':
            boxes[box].remove(Lens(label, 0))

focusing_power = sum([sum(box.focusing_powers()) for box in boxes])

with open('output', 'w') as output:
    output.write(str(hash_sum) + '\n')
    output.write(str(focusing_power) + '\n')