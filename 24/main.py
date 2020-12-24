import re


def load_input():
    with open("input.txt", "r") as f:
        return load_from_lines(f)


def load_from_lines(lines):
    prog = re.compile("ne|nw|se|sw|e|w")
    tiles = []
    for line in lines:
        line = line.strip()
        if line:
            directions = [m.group() for m in prog.finditer(line)]
            tiles.append(directions)
    return tiles


def part1():
    tiles = load_input()
    tiles = solve_part1(tiles)
    print("part 1", tiles)


directions = {
    "w": (-2, 0),
    "e": (2, 0),
    "se": (1, -1),
    "sw": (-1, -1),
    "ne": (1, 1),
    "nw": (-1, 1),
}


def solve_part1(tiles):
    """Hex grid coordinate system is 2D

    north = +y
    east = +x

    white = 0
    black = 1
    """

    grid = flip_tiles(tiles)
    black_tiles = list(grid.values()).count(1)
    return black_tiles


def flip_tiles(tiles):
    grid = {}
    for tile in tiles:
        x, y = 0, 0
        for direction in tile:
            dx, dy = directions[direction]
            x += dx
            y += dy
        pos = (x, y)
        value = grid.get(pos, 0)
        value = 0 if value else 1  # flip tile!
        grid[pos] = value
    return grid


example1 = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""


def test_part1():
    tiles = load_from_lines(example1.splitlines())
    res = solve_part1(tiles)
    assert res == 10


def part2():
    data = load_input()
    res = solve_part2(data)
    print("part 2:", res)


def solve_part2(tiles):
    grid = flip_tiles(tiles)
    for day in range(1, 101):  # simulate 100 days
        # Determine bounding box:
        xs = [p[0] for p in grid.keys()]
        ys = [p[1] for p in grid.keys()]
        xmin = min(xs) - 2
        xmax = max(xs) + 2
        ymin = min(ys) - 2
        ymax = max(ys) + 2

        # Gather changes:
        changes = []
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                pos = (x, y)
                n = neighbours(grid, pos)
                v = grid.get(pos, 0)
                if v == 0 and n == 2:
                    changes.append((pos, 1))
                if v == 1 and (n == 0 or n > 2):
                    changes.append((pos, 0))

        # Apply changes:
        for pos, value in changes:
            grid[pos] = value

        black_tiles = list(grid.values()).count(1)
        print(f"day {day}: {black_tiles}")

    black_tiles = list(grid.values()).count(1)
    return black_tiles


def neighbours(grid, pos):
    x, y = pos
    n = 0
    for dx, dy in directions.values():
        n_pos = x + dx, y + dy
        n += grid.get(n_pos, 0)
    return n


def test_part2():
    tiles = load_from_lines(example1.splitlines())
    res = solve_part2(tiles)
    assert res == 2208


if __name__ == "__main__":
    part1()
    part2()
