import re
from functools import reduce

with open('input') as input:
    text = input.read()

d = re.compile(r'\s*(-?\d+)\s*')

sequences = text.split('\n')[:-1]

sequences = [d.findall(sequence) for sequence in sequences]
sequences = [[int(number) for number in sequence] for sequence in sequences]


def extrapolate_forwards(values):
    if all(value == 0 for value in values):
        return 0
    else:
        below = [ values[i+1] - values[i] for i in range(len(values)-1) ]
        value = extrapolate_forwards(below)
        return value + values[-1]

def extrapolate_backwards(values):
    if all(value == 0 for value in values):
        return 0
    else:
        below = [ values[i+1] - values[i] for i in range(len(values)-1) ]
        value = extrapolate_backwards(below)
        return values[0] - value

extrapolations_fwd = [extrapolate_forwards (sequence) for sequence in sequences]
extrapolations_bkw = [extrapolate_backwards(sequence) for sequence in sequences]

with open('output', 'w') as output:
    output.write(str(sum(extrapolations_fwd)) + '\n')
    output.write(str(sum(extrapolations_bkw)) + '\n')