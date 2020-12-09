

def load_stream():
    numbers = []
    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                numbers.append(int(line))
    return numbers

# Part 1:
def scan(numbers, preamble=25):
    for i in range(preamble, len(numbers)):
        valid_options = set()
        for j in range(i - preamble, i):
            for k in range(j + 1, i):
                valid_options.add(numbers[j] + numbers[k])

        num = numbers[i]
        if num not in valid_options:
            return num
    raise ValueError('Not found!')


# Part 2:
def scan2(numbers, searched_sum):
    head = tail = 0
    current_sum = numbers[head]
    while True:
        if current_sum < searched_sum:
            head += 1
            if head < len(numbers):
                current_sum += numbers[head]
            else:
                raise ValueError("Not found!")
        elif current_sum > searched_sum:
            current_sum -= numbers[tail]
            tail += 1
            if tail >= len(numbers):
                raise ValueError("Not found!")
        else:
            assert current_sum == searched_sum
            numbers = numbers[tail:head + 1]
            weakness = min(numbers) + max(numbers)
            return weakness

def main():
    numbers = load_stream()
    invalid_number = scan(numbers)
    print('Invalid char', invalid_number)
    weakness = scan2(numbers, invalid_number)
    print('Weakness', weakness)


def test_scan2():
    example = [
        35,
        20,
        15,
        25,
        47,
        40,
        62,
        55,
        65,
        95,
        102,
        117,
        150,
        182,
        127,
        219,
        299,
        277,
        309,
        576,
    ]

    weakness = scan2(example, 127)
    assert weakness == 62


if __name__ == '__main__':
    main()
