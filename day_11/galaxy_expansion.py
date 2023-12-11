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

with open('input') as input:
    text = input.read()

grid = text.split('\n')[:-1]
grid = [[c for c in line] for line in grid]

def empty_list(list):
    return all(v == '.' for v in list)

def get_empty_rows(grid):
    result = []
    for i in range(len(grid)):
        if empty_list(grid[i]):
            result.append(i)
    return result

def get_column(j, grid):
    result = []
    for i in range(len(grid)):
        result.append(grid[i][j])
    return result

def get_empty_columns(grid):
    result = []
    for j in range(len(grid[0])):
        column = get_column(j, grid)
        if empty_list(column):
            result.append(j)
    return result

galaxies = []

for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] == '#':
            galaxies.append(Vector2(i, j))

def expand(galaxies, multiplier, empty_rows, empty_columns):
    for g in galaxies:
        g.i += sum([(multiplier-1) for r in empty_rows if g.i > r])
    for g in galaxies:
        g.j += sum([(multiplier-1) for r in empty_columns if g.j > r])
    return galaxies

def calculate_distances(grid, multiplier, galaxies):
    copy_galaxies = [Vector2(galaxy.i, galaxy.j) for galaxy in galaxies]
    copy_galaxies = expand([Vector2(galaxy.i, galaxy.j) for galaxy in galaxies], multiplier, get_empty_rows(grid), get_empty_columns(grid))

    distance_sum = 0
    for n, m in [(n, m) for n in range(len(copy_galaxies)) for m in range(n+1, len(copy_galaxies))]:
        distance_sum += abs(copy_galaxies[n].i - copy_galaxies[m].i) + abs(copy_galaxies[n].j - copy_galaxies[m].j)
    
    return distance_sum

with open('output', 'w') as output:
    output.write(str(calculate_distances(grid, 2, galaxies)) + '\n')
    output.write(str(calculate_distances(grid, 1000000, galaxies)) + '\n')