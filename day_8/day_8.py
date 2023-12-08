import re
from enum import Enum
from itertools import cycle
from math import lcm

class Direction(Enum):
    LEFT  = 0
    RIGHT = 1

class Node:
    def __init__(self, value, left, right) -> None:
        self.value = value
        self.left  = left
        self.right = right
    
    def walk(self, dir : Direction):
        if dir == Direction.LEFT:
            return self.left
        else:
            return self.right

D = {
    'L' : Direction.LEFT,
    'R' : Direction.RIGHT
}

with open('input') as input:
    text = input.read()

N = re.compile(r'(\w\w\w)\s=\s\((\w\w\w),\s(\w\w\w)\)')

walk, nodes = text.split('\n\n')
walk_simple = cycle(map(D.get, walk))
walk_ghost  = cycle(map(D.get, walk))

nodes = nodes.split('\n')[:-1]
nodes = [N.match(node).groups() for node in nodes]

node_map = {node[0] : Node(node[0], node[1], node[2]) for node in nodes}
for node in node_map.values():
    node.left = node_map[node.left]
    node.right = node_map[node.right]

steps = 0
spider = node_map['AAA']
while spider.value != 'ZZZ':
   instruction = walk_simple.__next__()
   spider = spider.walk(instruction)
   steps += 1

def cycle_spiders(spider : Node):
    steps = 0
    while spider.value[2] != 'Z':
        instruction = walk_ghost.__next__()
        spider = spider.walk(instruction)
        steps += 1
    return steps

spiders = [node for node in node_map.values() if node.value[2] == 'A']
goals   = [cycle_spiders(spider) for spider in spiders]

with open('output', 'w') as output:
    output.write(str(steps) + '\n')
    output.write(str(lcm(*goals)) + '\n')