
numbers = []
with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            number = int(line)
            numbers.append(number)

print(numbers)

# Find two numbers that add up to 2020, and then multiply those two

for n1 in numbers:
    for n2 in numbers:
        s = n1 + n2
        if s == 2020:
            print('Add up to 2020:', n1, n2, 'product=', n1 * n2)

# Part 2:
for n1 in numbers:
    for n2 in numbers:
        for n3 in numbers:
            s = n1 + n2 + n3
            if s == 2020:
                print('Add up to 2020:', n1, n2, n3, 'product=', n1 * n2 * n3)
