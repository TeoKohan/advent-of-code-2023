import re
import bisect
from functools import reduce

with open('input') as input:
    text = input.read()
    seeds, *mappings = text.split('\n\n')

class Range:
    def __init__(self, start, end) -> None:
        self.start = start
        self.end   = end
    
    def trisect(self, r):
        A = Range(r.start, min(r.end, self.start)) if r.start < self.start else None
        B = Range(max(r.start, self.start) , min(r.end, self.end)) if r.start <= self.end and r.end >= self.start else None
        C = Range(max(r.start, self.end  ), r.end) if r.end   > self.end else None

        return A, B, C
    
    def offset(self, n):
        self.start += n
        self.end   += n

    def intersects(self, r):
        return (r.start <= self.end + 1 and r.end + 1 >= self.start) or (r.start + 1 >= self.start and r.end - 1 <= self.end)

    def union(self, r):
        self.start = min(self.start, r.start)
        self.end   = max(self.end, r.end)

    def __repr__(self) -> str:
        return f'[{self.start}, {self.end}]'

class RangeList:
    def __init__(self, l) -> None:
        self.list = l
    
    def add(self, r : Range):
        if len(self.list) == 0:
            self.list = [r]
        else:
            i = bisect.bisect_left(self.list, r.start, key=lambda x: x.start)
            self.list[i:i] = [r]
            while len(self.list) > i+1 and self.list[i].intersects(self.list[i+1]):
                self.list[i].union(self.list[i+1])
                self.list.pop(i+1)
            
            if len(self.list) > 1 and self.list[i].intersects(self.list[i-1]):
                self.list[i].union(self.list[i-1])
                self.list.pop(i-1)
        
    def union(self, rl):
        for r in rl.list:
            self.add(r)

    def __repr__(self) -> str:
        res  = '-['
        res += ', '.join([r.__repr__() for r in self.list])
        res += ']-'
        return res

class MappingEntry:
    def __init__(self, value) -> None:
        dst_start, src_start, length = map(int, value.split(' '))
        self.range  = Range(src_start, src_start+length-1)
        self.offset = dst_start - src_start
        self.next   = None
    
    def travel(self, rl : RangeList):
        rangelist = RangeList([])
        for r in rl.list:
            A, B, C = self.range.trisect(r)
            if A != None:
                rangelist.add(A)
            if B != None:
                B.offset(self.offset)
                rangelist.add(B)
            if C != None:
                if self.next:
                    C = self.next.travel(RangeList([C]))
                    rangelist.union(C)
                else:
                    rangelist.add(C)

        return rangelist

    def __repr__(self) -> str:
        res = f'({self.range} | {self.offset})'
        if next:
            res += ', ' + self.next.__repr__()
        return res

d = re.compile(r'\d+')
seeds = list(map(int, re.findall(d, seeds)))

mappings = list(map(lambda s: s.split('\n')[1:], mappings))
mappings[-1] = mappings[-1][:-1]
mappings = [[MappingEntry(entry) for entry in mapping] for mapping in mappings]
mappings = [sorted(mapping, key=lambda k: k.range.start) for mapping in mappings]

for mapping in mappings:
    spider = mapping[0]
    for entry in mapping[1:]:
        spider.next = entry
        spider = entry

mappings = [mapping[0] for mapping in mappings]

ranges = [ Range(seed, seed) for seed in seeds]
simple_soil = [reduce( lambda x, r: r.travel(x), mappings, RangeList([r]) ) for r in ranges]
simple_soil = min([rl.list[0].start for rl in simple_soil])

ranges = [ Range(s, s+o-1) for s, o in zip(seeds[::2], seeds[1::2])]
complex_soil = [reduce( lambda x, r: r.travel(x), mappings, RangeList([r]) ) for r in ranges]
complex_soil = min([rl.list[0].start for rl in complex_soil])

with open('output', 'w') as output:
    output.write(str(simple_soil) + '\n')
    output.write(str(complex_soil) + '\n')