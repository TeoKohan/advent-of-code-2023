from enum import Enum

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class Vector2:

    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j

    def __add__(self, w):
        return Vector2(self.i + w.i, self.j + w.j)
    
    def __eq__(self, w):
        return self.i == w.i and self.j == w.j
    
    def __hash__(self) -> int:
        return (self.i, self.j).__hash__()

    def __repr__(self) -> str:
        return f'({self.i}, {self.j})'

D = {
    '|' : {Direction.NORTH, Direction.SOUTH},
    '-' : {Direction.EAST, Direction.WEST},
    'L' : {Direction.NORTH, Direction.EAST},
    'J' : {Direction.NORTH, Direction.WEST},
    '7' : {Direction.SOUTH, Direction.WEST},
    'F' : {Direction.SOUTH, Direction.EAST},
    '.' : { },
    'S' : {Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST}
}

D2M = {
    Direction.NORTH : Vector2(-1, 0),
    Direction.EAST : Vector2(0, 1),
    Direction.SOUTH : Vector2(1, 0),
    Direction.WEST : Vector2(0, -1)
}

receive = {
    Direction.NORTH : Direction.SOUTH,
    Direction.EAST : Direction.WEST,
    Direction.SOUTH : Direction.NORTH,
    Direction.WEST : Direction.EAST
}

with open('input') as input:
    text = input.read()

grid = text.split('\n')[:-1]
grid = [[c for c in line] for line in grid]

def starting_position(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'S':
                return Vector2(i, j)

n, m = len(grid), len(grid[0])
def in_bounds(v):
    return 0 <= v.i < n and 0 <= v.j < m

S = starting_position(grid)
dir_grid = [list(map(D.get, line)) for line in grid]

furthest = 0
for dir in Direction:
    steps = 1
    LOOP = set()
    heading = dir
    spider = S + D2M[heading]
    LOOP.add(spider)
    while spider != S and in_bounds(spider) and receive[heading] in dir_grid[spider.i][spider.j]:
        position = dir_grid[spider.i][spider.j]
        heading = [d for d in position if d != receive[heading]][0]
        spider = spider + D2M[heading]
        LOOP.add(spider)
        steps += 1
    if spider == S:
        furthest = max(furthest, steps//2)

simple_grid = [line[:] for line in grid]
for i in range(len(grid)):
    line = ''
    for j in range(len(grid[i])):
        if Vector2(i, j) in LOOP:
            simple_grid[i][j] = simple_grid[i][j]
        else:
            simple_grid[i][j] = '.'

expanded_grid = []
for i in range(len(grid)):
    expanded_grid += [[]]
    for j in range(len(grid[i])):
        expanded_grid[i*2] += simple_grid[i][j]
        expanded_grid[i*2] += '.'
    expanded_grid.append(['.' for _ in expanded_grid[i*2]])

for v in LOOP:
    for dir in dir_grid[v.i][v.j]:
        d = D2M[dir]
        c = '|' if d.i != 0 else '-'
        expanded_grid[v.i*2+d.i][v.j*2+d.j] = c

def in_expanded_bounds(v):
    return 0 <= v.i < n * 2 and 0 <= v.j < m * 2

UNVISITED = [Vector2(0, 0)]
while len(UNVISITED) != 0:
    visit = UNVISITED.pop()
    for dir in Direction:
        step = visit + D2M[dir]
        if in_expanded_bounds(step) and expanded_grid[step.i][step.j] == '.':
            UNVISITED.append(step)
            expanded_grid[step.i][step.j] = 'x'

with open('output_expanded', 'w') as output:
    for line in expanded_grid:
        output.write(''.join(line) + '\n')

contracted_grid = expanded_grid[0::2]
contracted_grid = [line[0::2] for line in contracted_grid]

with open('output_expanded', 'w') as output:
    for line in expanded_grid:
        output.write(''.join(line) + '\n')

inner_tiles = 0
for i in range(len(contracted_grid)):
    for j in range(len(contracted_grid[i])):
        if contracted_grid[i][j] == '.':
            inner_tiles += 1

with open('output_contracted', 'w') as output:
    for line in contracted_grid:
        output.write(''.join(line) + '\n')

with open('output', 'w') as output:
    output.write(str(furthest) + '\n')
    output.write(str(inner_tiles) + '\n')