
# Check passwords to policy

import re

# Parsing:
prog = re.compile('^(\d+)-(\d+) (.): (.+)$')
lines = []

with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            mo = prog.match(line)
            assert mo
            low = int(mo.group(1))
            high = int(mo.group(2))
            char = mo.group(3)
            password = mo.group(4)
            lines.append((low, high, char, password))

def count_valid(is_valid):
    return len(list(filter(lambda x: is_valid(*x), lines)))

# Part 1:
def is_valid1(low, high, char, password):
    occurences = password.count(char)
    return low <= occurences <= high

print(count_valid(is_valid1))

# Part 2:
def is_valid2(pos1, pos2, char, password):
    selected_chars = password[pos1 - 1] + password[pos2 - 1]
    occurences = selected_chars.count(char)
    return occurences == 1

print(count_valid(is_valid2))
