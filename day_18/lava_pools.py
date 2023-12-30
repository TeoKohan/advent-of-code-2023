from enum import IntEnum
import re

class Direction(IntEnum):
    Up = 3
    Right = 0
    Down = 1
    Left = 2

    def D2V(self):
        match self:
            case Direction.Up:
                return Vector2(-1,  0)
            case Direction.Right:
                return Vector2( 0,  1)
            case Direction.Down:
                return Vector2( 1,  0)
            case Direction.Left:
                return Vector2( 0, -1)
            
class Vector2:
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j

    def __add__(self, w):
        return Vector2(self.i + w.i, self.j + w.j)

    def __mul__(self, a):
        return Vector2(self.i * a, self.j * a)

    def __repr__(self) -> str:
        return f'({self.i}, {self.j})'
    
class Grid:
    def __init__(self, values) -> None:
        self.values = [[value for value in line] for line in values]
        self.rows = len(self.values)
        self.cols = len(self.values[0])
    
    def flood(self):
        print('flooding')
        unvisited = [Vector2(0, 0)]
        while unvisited:
            v = unvisited.pop()
            if 0 <= v.i < self.rows and 0 <= v.j < self.cols:
                match self.values[v.i][v.j]:
                    case '.':
                        for direction in Direction:
                            unvisited.append(v + direction.D2V())
                        self.values[v.i][v.j] = '~'
                    case '#':
                        pass
    
    def holes(self):
        result = 0
        for line in self.values:
            for c in line:
                result += 1 if c in ['.', '#'] else 0
        return result

    def __repr__(self) -> str:
        repr = ''
        for line in self.values:
            repr += ''.join(line) + '\n'
        return repr
    
with open('input') as input:
    text = input.read()

lines = text.split('\n')[:-1]
lines = [re.match(r'([URDL]) (\d+) \(\#([a-z0-9]{6})\)', line).groups() for line in lines]
simple_lines  = [(D, int(L)) for D, L, _ in lines]
swapped_lines = [(Direction(int(H[5])), int(H[:5], 16)) for _, _, H in lines]

j = 0
holes = { (0, 0) }
spider = Vector2(0, 0)
for line in simple_lines:
    direction, length = line
    match direction:
        case 'U':
            direction = Direction.Up
        case 'R':
            direction = Direction.Right
        case 'D':
            direction = Direction.Down
        case 'L':
            direction = Direction.Left

    print(length, (j := j + 1), '/', len(lines))
    for i in range(length):
        spider += direction.D2V()
        holes.add( (spider.i, spider.j) )

min_row, min_col = min([i for i, _ in holes]), min([j for _, j in holes])
max_row, max_col = max([i for i, _ in holes]), max([j for _, j in holes])

grid = Grid([['.' for _ in range(max_col - min_col + 3)] for _ in range(max_row - min_row + 3)])

print(min_row, min_col)
print(max_row, max_col)

for i, j in holes:
    grid.values[i-min_row+1][j-min_col+1] = '#'

grid.flood()

print(grid.holes())

with open('output', 'w') as output:
    output.write('\n')
    output.write('\n')