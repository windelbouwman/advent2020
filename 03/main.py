import functools

class Map:
    def __init__(self, rows):
        self.rows = rows
        self.height = len(rows)
        self._w = len(rows[0])
    
    def get_tile(self, x, y):
        assert 1 <= y <= self.height
        assert x >= 1
        x = (x - 1) % self._w
        return self.rows[y - 1][x]


def load_map():
    with open('input.txt', 'r') as f:
        rows = []
        for line in f:
            line = line.strip()
            if line:
                rows.append(line)
    return Map(rows)

grid = load_map()


def calculate_tree_encounters(dx, dy):
    x, y = 1, 1
    encounters = 0
    while y <= grid.height:
        tile = grid.get_tile(x, y)
        # print(x, y, tile)
        if tile == '#':
            encounters += 1
        x += dx
        y += dy
    return encounters

# Part 1:
print('encounters', calculate_tree_encounters(3, 1))

# Part 2:
slopes = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]

tree_encounters = [calculate_tree_encounters(*s) for s in slopes]

print('products:', functools.reduce(lambda a, b: a * b, tree_encounters))
