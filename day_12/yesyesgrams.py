import re
from functools import reduce
from math import inf

with open('input') as input:
    text = input.read()

puzzles = text.split('\n')[:-1]
puzzles = [line.split(' ') for line in puzzles]
puzzles = [(puzzle, list(map(int, clues.split(',')))) for puzzle, clues in puzzles]
large_puzzles = [('?'.join([puzzle]*5), clues*5) for puzzle, clues in puzzles]

M = dict()

def solve1(puzzle : str, clue):
    puzzle = puzzle.strip('.')
    solid = puzzle.count('#')
    difference = clue - solid
    if '.' in puzzle:
        return 0
    if difference < 0:
        return 0
    elif len(puzzle) < clue:
        return 0
    elif not '#' in puzzle:
        return len(puzzle) - difference + 1
    elif re.match(r'^\?*#*\?*$', puzzle):
        left, right = re.split(r'#+', puzzle)
        left, right = len(left), len(right)
        assert(left + right >= difference)

        result = 0
        for i in range(left+1):
            if i <= difference and i + right >= difference:
                result += 1

        return result
    else:
        left, center, right = re.match(r'(\?*)(#.*#)(\?*)', puzzle).groups()
        center = center.replace('?', '#')
        return solve1(left + center + right, clue)

def solve(puzzle : str, clues):
    key = (puzzle, tuple(clues))
    if not key in M:
        puzzle = puzzle.lstrip('.')

        non_nullable = re.findall(r'[?#]*#[?#]*', puzzle)
        difference = len(clues) - len(non_nullable)
        if difference < 0:
            M[key] = 0
        elif difference == 0:
            if len(non_nullable) == len(clues):
                M[key] = reduce(lambda x, y: x * y, [solve1(group, clue) for group, clue in zip(non_nullable, clues)], 1)
            else:
                M[key] = 0
        else:

            def match_clue(puzzle : str, clue):
                puzzle = puzzle.lstrip('.')
                regex  = r'^[?#]{' + str(clue) + r'}(?:[?.]|$)'
                if re.match(regex, puzzle):
                    return True
                return False
            
            if len(puzzle) == 0 and len(clues) == 0:
                M[key] = 1
            elif len(puzzle) == 0:
                M[key] = 0
            else:
                match puzzle[0]:
                    case '.':
                        M[key] = solve(puzzle[1:], clues)
                    case '?':
                        M[key] = (solve(puzzle[clues[0]+1:], clues[1:]) if match_clue(puzzle, clues[0]) else 0) + solve(puzzle[1:], clues)
                    case '#':
                        M[key] =  solve(puzzle[clues[0]+1:], clues[1:]) if match_clue(puzzle, clues[0]) else 0
    return M[key]

sum_simple = sum([solve(*puzzle) for puzzle in puzzles])
sum_complex = sum([solve(*puzzle) for puzzle in large_puzzles])

with open('output', 'w') as output:
    output.write(str(sum_simple ) + '\n')
    output.write(str(sum_complex) + '\n')