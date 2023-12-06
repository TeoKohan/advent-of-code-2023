import re

with open('input') as input:
    text = input.read()
    scratchcards = text.split('\n')[:-1]

r = re.compile(r'Card\s*\d*: ([^|]*) \| (.*)')
d = re.compile(r'\d+')

scratchcards = map(r.match, scratchcards)
scratchcards = [[list(map(int, d.findall(group))) for group in scratch.groups()] for scratch in scratchcards]
winners = [sum([1 for winner in winners if winner in numbers]) for winners, numbers in scratchcards]

points = [0 if quantity == 0 else 2**(quantity-1) for quantity in winners]
points = sum(points)

last = len(scratchcards) - 1
count = { i: (1, winners[i]) for i in range(len(scratchcards)) }

for k, v in count.items():
    q, w = v
    for i in range(w):
        if k+i+1 in count:
            count[k+i+1] = (count[k+i+1][0] + q, count[k+i+1][1])

quantity = sum([q for q, w in count.values()])

with open('output', 'w') as output:
    output.write(str(points) + '\n')
    output.write(str(quantity) + '\n')