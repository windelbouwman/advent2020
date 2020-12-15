from collections import defaultdict


def load_data():
    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()


def part1():
    inp = '0,13,1,8,6,15'
    numbers = list(map(int, inp.split(',')))
    print('2020th number spoken:', get_nth_spoken(numbers, 2020))


def get_nth_spoken(start_sequence, nth_turn):
    spoken_in_turn = {}
    last_spoken = None

    turn = 1

    for spoken in start_sequence:
        # speak number:
        last_spoken = spoken
        spoken_in_turn[spoken] = turn
        turn += 1

    while True:
        if last_spoken in spoken_in_turn:
            spoken = turn - 1 - spoken_in_turn[last_spoken]
        else:
            spoken = 0
        spoken_in_turn[last_spoken] = turn - 1

        # speak number:
        last_spoken = spoken

        if turn % 1000000 == 0:
            print('turn', turn, spoken)

        if turn == nth_turn:
            return last_spoken

        turn += 1


def test_example1():
    assert 436 == get_nth_spoken([0,3,6], 2020)
    assert 1 == get_nth_spoken([1,3,2], 2020)
    assert 10 == get_nth_spoken([2,1,3], 2020)
    assert 27 == get_nth_spoken([1,2,3], 2020)
    assert 78 == get_nth_spoken([2,3,1], 2020)
    assert 438 == get_nth_spoken([3,2,1], 2020)
    assert 1836 == get_nth_spoken([3,1,2], 2020)


def part2():
    inp = '0,13,1,8,6,15'
    numbers = list(map(int, inp.split(',')))
    # This takes too long:
    print('30_000_000th number spoken:', get_nth_spoken(numbers, 30_000_000))


def test_example2():
    assert 175594 == get_nth_spoken([0,3,6], 30_000_000)
# Probably works, but takes a long time
#     assert 2578 == get_nth_spoken([1,3,2], 30_000_000)
#     assert 3544142 == get_nth_spoken([2,1,3], 30_000_000)
#     assert 261214 == get_nth_spoken([1,2,3], 30_000_000)
#     assert 6895259 == get_nth_spoken([2,3,1], 30_000_000)
#     assert 18 == get_nth_spoken([3,2,1], 30_000_000)
#     assert 362 == get_nth_spoken([3,1,2], 30_000_000)


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()