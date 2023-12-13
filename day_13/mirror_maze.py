import re
from enum import Enum

class AxisType(Enum):
    Horizontal = 0
    Vertical   = 1

class Grid:
    def __init__(self, values) -> None:
        self.values = [[value for value in line] for line in values]
        self.rows = len(self.values)
        self.cols = len(self.values[0])
    
    def row(self, i):
        return self.values[i]
    
    def col(self, j):
        return [self.values[i][j] for i in range(len(self.values))]

with open('input') as input:
    text = input.read()

grids = text.split('\n\n')
grids = [ grid.split('\n') for grid in grids]
grids[-1] = grids[-1][:-1]
grids = [Grid(grid) for grid in grids]

def get_axis(grid: Grid):
    for i in range(0, grid.rows-1):
        up, down = i, i+1
        while up >= 0 and down < grid.rows and grid.row(up) == grid.row(down):
            up   -= 1
            down += 1
        if up < 0 or down >= grid.rows:
            return i+1, AxisType.Horizontal
    for j in range(0, grid.cols-1):
        left, right = j, j+1
        while left >= 0 and right < grid.cols and grid.col(left) == grid.col(right):
            left  -= 1
            right += 1
        if left < 0 or right >= grid.cols:
            return j+1, AxisType.Vertical


def get_smudged_axis(grid: Grid, axis, axis_type):
    for n in range(grid.rows):
        for m in range(grid.cols):
            new_grid = Grid(grid.values)
            new_grid.values[n][m] = '.' if grid.values[n][m] == '#' else '#'
            for i in range(0, new_grid.rows-1):
                up, down = i, i+1
                while up >= 0 and down < new_grid.rows and new_grid.row(up) == new_grid.row(down):
                    up   -= 1
                    down += 1
                if (up < 0 or down >= new_grid.rows) and ((i+1) != axis or AxisType.Horizontal != axis_type):
                    return i+1, AxisType.Horizontal
            for j in range(0, new_grid.cols-1):
                left, right = j, j+1
                while left >= 0 and right < new_grid.cols and new_grid.col(left) == new_grid.col(right):
                    left  -= 1
                    right += 1
                if (left < 0 or right >= new_grid.cols) and ((j+1) != axis or AxisType.Vertical != axis_type):
                    return j+1, AxisType.Vertical

simple_result = 0
smudged_result = 0
for grid in grids:
    axis, axis_type = get_axis(grid)
    simple_result += axis if axis_type == AxisType.Vertical else 100 * axis
    axis, axis_type = get_smudged_axis(grid, axis, axis_type)
    smudged_result += axis if axis_type == AxisType.Vertical else 100 * axis

with open('output', 'w') as output:
    output.write(str(simple_result) + '\n')
    output.write(str(smudged_result) + '\n')