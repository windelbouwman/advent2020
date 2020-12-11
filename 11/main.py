

around_deltas = [
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
]

class Seating:
    """
    L = empty
    # = occupied
    . = floor
    """
    def __init__(self, rows):
        self.rows = rows
        self.width = len(rows[0])
        self.height = len(rows)

    def get_pos(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            row = self.rows[y]
            return row[x]
    
    def set_pos(self, x, y, s):
        self.rows[y][x] = s
    
    def amount_adjecent_occupied(self, x, y):
        occupied = 0
        for dx, dy in around_deltas:
            s = self.get_pos(x + dx, y + dy)
            if s == '#':
                occupied += 1
        return occupied

    def amount_in_sight(self, x, y):
        """ Determine how many seats are in sight. """
        return sum(self.cast_ray(x, y, dx, dy) for dx, dy in around_deltas)

    def cast_ray(self, x, y, dx, dy):
        """ Follow a direction until a seat is hit, or we are off the grid.
        """
        while True:
            x += dx
            y += dy
            s = self.get_pos(x, y)
            if s == '.':
                continue
            elif s == '#':
                return 1
            else:
                return 0

    def __iter__(self):
        for x in range(self.width):
            for y in range(self.height):
                seat = self.get_pos(x, y)
                yield x, y, seat

    def count(self, s):
        total = 0
        for _, _, s2 in self:
            if s == s2:
                total += 1
        return total


def load_seats():
    rows = []
    with open("input.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(list(line))

    return Seating(rows)


def part1():
    seating = load_seats()
    while True:
        updates = []

        # Evaluate:
        for x, y, seat in seating:
            adjecent = seating.amount_adjecent_occupied(x, y)
            if seat == 'L' and adjecent == 0:
                updates.append((x, y, '#'))
            elif seat == '#' and adjecent >= 4:
                updates.append((x, y, 'L'))
        
        # Update:
        if updates:
            for x, y, seat in updates:
                seating.set_pos(x, y, seat)
        else:
            break

    print('Occupied seats (adjecent):', seating.count('#'))


def part2():
    seating = load_seats()
    while True:
        updates = []

        # Evaluate:
        for x, y, seat in seating:
            in_sight = seating.amount_in_sight(x, y)
            if seat == 'L' and in_sight == 0:
                updates.append((x, y, '#'))
            elif seat == '#' and in_sight >= 5:
                updates.append((x, y, 'L'))
        
        # Update:
        if updates:
            for x, y, seat in updates:
                seating.set_pos(x, y, seat)
        else:
            break

    print('Occupied seats (in sight):', seating.count('#'))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
