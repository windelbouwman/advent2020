def load_initial():
    with open("input.txt", "r") as f:
        return load_map_from_lines(f)


def load_map_from_lines(lines):
    m = []
    for line in lines:
        line = line.strip()
        if line:
            m.append(line)
    return m


def part1():
    m = load_initial()
    s = solve_part1(m)
    print("part 1", s)


def solve_part1(m):
    state = set()

    # Initial state:
    z = 0
    for y, line in enumerate(m):
        for x, c in enumerate(line):
            if c == "#":
                state.add((x, y, z))

    for _ in range(6):
        # Determine bounding box:
        min_x = min(s[0] for s in state) - 1
        max_x = max(s[0] for s in state) + 1
        min_y = min(s[1] for s in state) - 1
        max_y = max(s[1] for s in state) + 1
        min_z = min(s[2] for s in state) - 1
        max_z = max(s[2] for s in state) + 1

        # Determine changes:
        changes = []
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                for z in range(min_z, max_z + 1):
                    s = (x, y, z)
                    n = neigbours3(state, s)
                    # print('neighbours', n)
                    if s in state:
                        # active
                        if not (n == 2 or n == 3):
                            changes.append(("remove", s))
                    else:
                        # in-active
                        if n == 3:
                            changes.append(("add", s))

        # Apply changes:
        for change, s in changes:
            # print(change, s)
            if change == "remove":
                assert s in state
                state.discard(s)
            elif change == "add":
                assert s not in state
                state.add(s)

    return len(state)


def neigbours3(state, s):
    x, y, z = s
    n = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                p = (x + dx, y + dy, z + dz)
                if p in state and p != s:
                    n += 1
    return n


def test_part1():
    example1 = """
    .#.
    ..#
    ###
    """
    m = load_map_from_lines(example1.splitlines())
    r = solve_part1(m)
    assert r == 112


def part2():
    m = load_initial()
    r = solve_part2(m)
    print("part 2", r)


def solve_part2(m):
    state = set()

    # Initial state:
    z, w = 0, 0
    for y, line in enumerate(m):
        for x, c in enumerate(line):
            if c == "#":
                state.add((x, y, z, w))

    for _ in range(6):
        # Determine bounding box:
        min_x = min(s[0] for s in state) - 1
        max_x = max(s[0] for s in state) + 1
        min_y = min(s[1] for s in state) - 1
        max_y = max(s[1] for s in state) + 1
        min_z = min(s[2] for s in state) - 1
        max_z = max(s[2] for s in state) + 1
        min_w = min(s[3] for s in state) - 1
        max_w = max(s[3] for s in state) + 1

        # Determine changes:
        changes = []
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                for z in range(min_z, max_z + 1):
                    for w in range(min_w, max_w + 1):
                        s = (x, y, z, w)
                        n = neigbours4(state, s)
                        # print('neighbours', n)
                        if s in state:
                            # active
                            if not (n == 2 or n == 3):
                                changes.append(("remove", s))
                        else:
                            # in-active
                            if n == 3:
                                changes.append(("add", s))

        # Apply changes:
        for change, s in changes:
            # print(change, s)
            if change == "remove":
                assert s in state
                state.discard(s)
            elif change == "add":
                assert s not in state
                state.add(s)

    return len(state)


def neigbours4(state, s):
    x, y, z, w = s
    n = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                for dw in [-1, 0, 1]:
                    p = (x + dx, y + dy, z + dz, w + dw)
                    if p in state and p != s:
                        n += 1
    return n


def test_part2():
    example1 = """
    .#.
    ..#
    ###
    """
    m = load_map_from_lines(example1.splitlines())
    r = solve_part2(m)
    assert r == 848


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
