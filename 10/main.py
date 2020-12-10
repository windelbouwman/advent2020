def load_adapters():
    with open("input.txt", "r") as f:
        return [int(line.strip()) for line in f]


def part1():
    adapters = load_adapters()
    jolts = 0
    steps = []
    for adapter in sorted(adapters):
        step = adapter - jolts
        jolts = adapter

        assert 1 <= step <= 3
        steps.append(step)

    steps.append(3)

    print("part 1", steps.count(1) * steps.count(3))


def part2():
    adapters = list(sorted(load_adapters()))
    print("Combo's", combos(adapters))


def combos(adapters):
    """ Figure out possible arrangements """
    adapters = list(sorted(adapters))

    paths_to = {0: 1}
    for adapter in adapters:
        paths = sum(paths_to.get(adapter - d, 0) for d in [1, 2, 3])
        assert paths > 0
        paths_to[adapter] = paths

    return paths_to[adapters[-1]]


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()


def test_part2_example1():
    adapters = [
        16,
        10,
        15,
        5,
        1,
        11,
        7,
        19,
        6,
        12,
        4,
    ]
    assert 8 == combos(adapters)


def test_part2_example2():
    adapters = [
        28,
        33,
        18,
        42,
        31,
        14,
        46,
        20,
        48,
        47,
        24,
        23,
        49,
        45,
        19,
        38,
        39,
        11,
        1,
        32,
        25,
        35,
        8,
        17,
        7,
        9,
        4,
        2,
        34,
        10,
        3,
    ]

    assert 19208 == combos(adapters)
