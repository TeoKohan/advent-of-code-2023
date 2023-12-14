from enum import Enum
import bisect

class Object(Enum):
    SquareRock = 0
    RoundRock  = 1

class ObstacleGrid:
    def __init__(self, values) -> None:
        self.row = dict()
        self.col = dict()
        self.rows = len(values   )
        self.cols = len(values[0])
        for i in range(self.rows):
            for j in range(self.cols):
                match values[i][j]:
                    case '#':
                        if i not in self.row:
                            self.row[i] = []
                        if j not in self.col:
                            self.col[j] = []
                        bisect.insort(self.row[i], (j, Object.SquareRock))
                        bisect.insort(self.col[j], (i, Object.SquareRock))
                    case 'O':
                        if i not in self.row:
                            self.row[i] = []
                        if j not in self.col:
                            self.col[j] = []
                        bisect.insort(self.row[i], (j, Object.RoundRock))
                        bisect.insort(self.col[j], (i, Object.RoundRock))
    
    def roll_north(self):
        for col in self.col:
            obstacle = -1
            for row, obj in self.col[col]:
                match obj:
                    case Object.SquareRock:
                        obstacle = row
                    case Object.RoundRock:
                        new_row = obstacle + 1
                        self.col[col].remove( (row, obj) )
                        self.row[row].remove( (col, obj) )
                        bisect.insort(self.col[col], (new_row, Object.RoundRock))
                        bisect.insort(self.row[new_row], (col,     Object.RoundRock))
                        obstacle = new_row

    def roll_south(self):
        for col in self.col:
            obstacle = self.rows
            for row, obj in reversed(self.col[col]):
                match obj:
                    case Object.SquareRock:
                        obstacle = row
                    case Object.RoundRock:
                        new_row = obstacle - 1
                        self.col[col].remove( (row, obj) )
                        self.row[row].remove( (col, obj) )
                        bisect.insort(self.col[col], (new_row, Object.RoundRock))
                        bisect.insort(self.row[new_row], (col,     Object.RoundRock))
                        obstacle = new_row
    
    def roll_west(self):
        for row in self.row:
            obstacle = -1
            for col, obj in self.row[row]:
                match obj:
                    case Object.SquareRock:
                        obstacle = col
                    case Object.RoundRock:
                        new_col = obstacle + 1
                        self.row[row].remove( (col, obj) )
                        self.col[col].remove( (row, obj) )
                        bisect.insort(self.row[row], (new_col, Object.RoundRock))
                        bisect.insort(self.col[new_col], (row,     Object.RoundRock))
                        obstacle = new_col
    
    def roll_east(self):
        for row in self.row:
            obstacle = self.cols
            for col, obj in reversed(self.row[row]):
                match obj:
                    case Object.SquareRock:
                        obstacle = col
                    case Object.RoundRock:
                        new_col = obstacle - 1
                        self.row[row].remove( (col, obj) )
                        self.col[col].remove( (row, obj) )
                        bisect.insort(self.row[row], (new_col, Object.RoundRock))
                        bisect.insort(self.col[new_col], (row,     Object.RoundRock))
                        obstacle = new_col

    def spin_cycle(self):
        self.roll_north()
        self.roll_west ()
        self.roll_south()
        self.roll_east ()

    def round_rocks(self):
        return tuple([(row, col) for row in self.row for col, obj in self.row[row] if obj == Object.RoundRock])

    def load_north(self):
        result = 0
        for col in self.col:
            for row, obj in self.col[col]:
                match obj:
                    case Object.SquareRock:
                        pass
                    case Object.RoundRock:
                        result += self.rows - row
        return result

    def __repr__(self) -> str:
        result = ''
        for row in range(self.rows):
            row_str = ['.' for i in range(self.cols)]
            if row in self.row:
                for (col, obstacle) in self.row[row]:
                    row_str[col] = '#' if obstacle == Object.SquareRock else 'O'
                result += ''.join(row_str) + '\n'
        return result

with open('input') as input:
    text = input.read()

grid = ObstacleGrid(text.split('\n')[:-1])
grid.roll_north()
roll_simple_test = grid.load_north()
grid.roll_west ()
grid.roll_south()
grid.roll_east ()

cycles  = 1
results = dict()
state   = grid.round_rocks()
while not state in results:
    results[state] = cycles
    grid.spin_cycle()
    cycles += 1
    state = grid.round_rocks()

cycles = (1000000000 - cycles) % (cycles - results[state])
for _ in range(cycles):
    grid.spin_cycle()
roll_stress_test = grid.load_north()

with open('output', 'w') as output:
    output.write(str(roll_simple_test) + '\n')
    output.write(str(roll_stress_test) + '\n')