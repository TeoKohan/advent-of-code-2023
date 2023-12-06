from functools import reduce
from itertools import cycle
from copy import deepcopy

with open('input') as input:
    text = input.read()
    engine = text.split('\n')[:-1]
    engine = [[char for char in line] for line in engine]

empty = ['.']
digits = list(map(chr, range(ord('0'), ord('9')+1)))
directions = {
    (-1, -1), (-1, 0), (0, -1), (-1, 1), (1, -1), (1, 0), (0, 1), (1, 1)
}

cols, rows = len(engine[0]), len(engine)

def in_bounds(j, i):
    return 0 <= j < rows and 0 <= i < cols

def check_neighbours(j, i):
    for x, y in directions:
        m, n = j + y, i + x
        if in_bounds(m, n) and engine[m][n] not in digits + empty:
            return True
    return False

def record_number(j, i, input_engine, erase=True):
    while (i - 1 >= 0) and (input_engine[j][i-1] in digits):
        i = i-1
    number = ''
    while i < cols and input_engine[j][i] in digits:
        number += input_engine[j][i]
        input_engine[j][i] = '.' if erase else input_engine[j][i]
        i = i+1
    return (input_engine, int(number)) if erase else int(number)

sum_parts = 0
sum_gears = 0

parts_engine = deepcopy(engine)
gears_engine = deepcopy(engine)

for j in range(rows):
    for i in range(cols):
        if parts_engine[j][i] in digits and check_neighbours(j,i):
            parts_engine, number = record_number(j, i, parts_engine)
            sum_parts += number

for j in range(rows):
    for i in range(cols):
        if gears_engine[j][i] == '*':
            numbers = []
            if in_bounds(j, i-1) and gears_engine[j][i-1] in digits:
                numbers += [record_number(j, i-1, gears_engine, erase=False)]
            if in_bounds(j, i+1) and gears_engine[j][i+1] in digits:
                numbers += [record_number(j, i+1, gears_engine, erase=False)]
            if in_bounds(j+1, i) and gears_engine[j+1][i] in digits:
                numbers += [record_number(j+1, i, gears_engine, erase=False)]
            else:
                if in_bounds(j+1, i-1) and gears_engine[j+1][i-1] in digits:
                    numbers += [record_number(j+1, i-1, gears_engine, erase=False)]
                if in_bounds(j+1, i+1) and gears_engine[j+1][i+1] in digits:
                    numbers += [record_number(j+1, i+1, gears_engine, erase=False)]
            if in_bounds(j-1, i) and gears_engine[j-1][i] in digits:
                numbers += [record_number(j-1, i, gears_engine, erase=False)]
            else:
                if in_bounds(j-1, i-1) and gears_engine[j-1][i-1] in digits:
                    numbers += [record_number(j-1, i-1, gears_engine, erase=False)]
                if in_bounds(j-1, i+1) and gears_engine[j-1][i+1] in digits:
                    numbers += [record_number(j-1, i+1, gears_engine, erase=False)]
            if len(numbers) == 2:
                sum_gears += numbers[0] * numbers[1]

with open('output', 'w') as output:
    output.write(str(sum_parts) + '\n')
    output.write(str(sum_gears) + '\n')