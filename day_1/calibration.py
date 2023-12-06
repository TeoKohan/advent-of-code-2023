with open('input') as input:
    text = input.read()
    
calibrations = text.split('\n')[:-1]
digits = list(map(chr, range(ord('0'), ord('9')+1)))

def filter_digits(s: str) -> [chr]:
    return list(filter(lambda c: c in digits, s))

D = {
    'one'   : '1',
    'two'   : '2',
    'three' : '3',
    'four'  : '4',
    'five'  : '5',
    'six'   : '6',
    'seven' : '7',
    'eight' : '8',
    'nine'  : '9'
}

def filter_digits_complex(s: str) -> [chr]:
    result = []
    for i in range(0, len(s)):
        if s[i] in digits:
            result += [s[i]]
        else:
            for k in D:
                if s[i:].startswith(k):
                    result += [D[k]]
    return result

def calculate_sum(l):
    l = map(lambda c: c[0] + c[-1], l)
    l = map(int, l)
    l = list(l)
    return sum(l)

calibrations_simple = map(filter_digits, calibrations)
calibrations_simple = calculate_sum(calibrations_simple)

calibrations_complex = map(filter_digits_complex, calibrations)
calibrations_complex = calculate_sum(calibrations_complex)

with open('output', 'w') as output:
    output.write(str(calibrations_simple ) + '\n')
    output.write(str(calibrations_complex) + '\n')