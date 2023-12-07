import re

with open('input') as input:
    text = input.read()
    time, record = text.split('\n')[:-1]

d = re.compile(r'\d+')
time_simple   = list(map(int, re.findall(d, time)))
record_simple = list(map(int, re.findall(d, record)))

time_complex   = int(''.join(map(str, time_simple)))
record_complex = int(''.join(map(str, record_simple)))

cases_simple = zip(time_simple, record_simple)
case_complex = (time_complex, record_complex)

def solve_case(case):
    time, record = case
    i = 0
    while i * (time - i) <= record and i <= time // 2: i += 1
    return time - 2 * i + 1 if time - 2 * i > 0 else 0

simple_sum = 1
for case in cases_simple:
    simple_sum *= solve_case(case)

complex_sum = solve_case(case_complex)

with open('output', 'w') as output:
    output.write(str(simple_sum) + '\n')
    output.write(str(complex_sum) + '\n')