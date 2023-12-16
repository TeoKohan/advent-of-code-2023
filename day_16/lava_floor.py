from enum import Enum
from functools import reduce

class Orientation(Enum):
    Horizontal = 0
    Vertical = 1

class Direction(Enum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3

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
            
    def orientation(self) -> Orientation:
        return Orientation.Horizontal if self in [Direction.Left, Direction.Right] else Orientation.Vertical
    
class Vector2:
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j

    def __add__(self, w):
        return Vector2(self.i + w.i, self.j + w.j)

    def __repr__(self) -> str:
        return f'({self.i}, {self.j})'

class Ray(Vector2):
    def __init__(self, v : Vector2, direction) -> None:
        super().__init__(v.i, v.j)
        self.direction : Direction = direction

    def march(self) -> None:
        self.i += self.direction.D2V().i
        self.j += self.direction.D2V().j
    
    def reflect_left(self):
        match self.direction:
            case Direction.Up:
                self.direction = Direction.Right
            case Direction.Right:
                self.direction = Direction.Up
            case Direction.Down:
                self.direction = Direction.Left
            case Direction.Left:
                self.direction = Direction.Down
    
    def reflect_right(self):
        match self.direction:
            case Direction.Up:
                self.direction = Direction.Left
            case Direction.Right:
                self.direction = Direction.Down
            case Direction.Down:
                self.direction = Direction.Right
            case Direction.Left:
                self.direction = Direction.Up
    
    def __eq__(self, w):
        return self.i == w.i and self.j == w.j
    
    def __hash__(self) -> int:
        return (self.i, self.j).__hash__()

class Grid:
    def __init__(self, values) -> None:
        self.values = [[value for value in line] for line in values]
        self.rows = len(self.values)
        self.cols = len(self.values[0])

with open('input') as input:
    text = input.read()

grid = text.split('\n')[:-1]
grid = Grid(grid)

def energizing_ray(grid : Grid, ray : Ray) -> None:

    def walk(energized : set, grid : Grid, ray : Ray) -> [Ray]:

        def in_bound(grid : Grid, position : Vector2):
            return 0 <= position.i < grid.rows and 0 <= position.j < grid.cols
        
        if in_bound(grid, ray):
            key = (ray.i, ray.j)
            if key in energized:
                if ray.direction in energized[key]:
                    return []
                else:
                    energized[key].add(ray.direction)
            else:
                energized[key] = { ray.direction }
                
            match grid.values[ray.i][ray.j]:
                case '.':
                    rays = [ray]
                case '-':
                    match ray.direction.orientation():
                        case Orientation.Horizontal:
                            rays = [ray]
                        case Orientation.Vertical:
                            position = Vector2(ray.i, ray.j)
                            rays = [Ray(position, Direction.Left), Ray(position, Direction.Right)]
                case '|':
                    match ray.direction.orientation():
                        case Orientation.Horizontal:
                            position = Vector2(ray.i, ray.j)
                            rays = [Ray(position, Direction.Up), Ray(position, Direction.Down)]
                        case Orientation.Vertical:
                            rays = [ray]
                case '/':
                    ray.reflect_left()
                    rays = [ray]
                case '\\':
                    ray.reflect_right()
                    rays = [ray]
        else:
            return []
        
        for ray in rays:
            ray.march()

        return rays
    
    energized = dict()
    rays = [ray]
    while rays:
        new_rays = []
        for ray in rays:
            new_rays += walk(energized, grid, ray)
        rays = new_rays
    return energized

energized_top_left = len(energizing_ray(grid, Ray(Vector2(0, 0), Direction.Right)))

max_energized = reduce(max, [len(energizing_ray(grid, Ray(Vector2(i, 0), Direction.Right))) for i in range(grid.rows)], 0)
max_energized = reduce(max, [len(energizing_ray(grid, Ray(Vector2(0, j), Direction.Down))) for j in range(grid.cols)], max_energized)
max_energized = reduce(max, [len(energizing_ray(grid, Ray(Vector2(i, grid.cols-1), Direction.Left))) for i in range(grid.rows)], max_energized)
max_energized = reduce(max, [len(energizing_ray(grid, Ray(Vector2(grid.rows-1, j), Direction.Up))) for j in range(grid.cols)], max_energized)

with open('output', 'w') as output:
    output.write(str(energized_top_left) + '\n')
    output.write(str(max_energized) + '\n')