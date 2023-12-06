from functools import reduce

with open('input') as input:
    text = input.read()
    games = text.split('\n')[:-1]

def list_to_colors(l: str):
    values = l.split(',')
    values = map(lambda s: s[1:], values)
    values = map(lambda s: s.split(' '), values)
    return {color: int(n) for n, color in values}

games = { game[5:].split(':')[0] : game[5:].split(':')[1] for game in games }
games = { int(k) : v.split(';') for k, v in games.items() }
games = { k : list(map(list_to_colors, v)) for k, v in games.items() }

max_values = {
    'red' : 12,
    'green' : 13,
    'blue' : 14
}

def within(d: dict):
    return all(v <= max_values[k] for k, v in d.items())

def calculate_power(l: [dict]):
    powers = reduce(lambda r, d: { k: max(d[k], v) if k in d else v for k, v in r.items()}, l, {'red' : 0, 'green' : 0, 'blue' : 0})
    return reduce(lambda r, t: r * t, powers.values())

possible = [ k for k, v in games.items() if all(within(r) for r in v)]
possible = sum(possible)

power = [calculate_power(v) for _, v in games.items()]
power = sum(power)

with open('output', 'w') as output:
    output.write(str(possible) + '\n')
    output.write(str(power) + '\n')