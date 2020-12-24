def part1():
    res = solve_part1("974618352", 100)
    print("part 1:", res)


def solve_part1(labels, num_moves):
    labels = list(map(int, labels))
    min_label = min(labels)
    max_label = max(labels)

    # Ensure current cup is alway cup 0
    for _round_nr in range(num_moves):
        # print('cups', labels)

        # remove 3 cups:
        taken = [labels.pop(1), labels.pop(1), labels.pop(1)]
        # print('pick up', taken)

        # select destination cup:
        current = labels[0]
        destination = current - 1
        while destination not in labels[1:]:
            destination -= 1
            if destination < min_label:
                destination = max_label

        # Place cups back:
        index = labels.index(destination) + 1
        for t in reversed(taken):
            labels.insert(index, t)

        # Make next cup the first cup
        labels.append(labels.pop(0))

    index = labels.index(1)
    tail = labels[index + 1 :]
    front = labels[:index]

    return "".join(map(str, tail + front))


def test_part1_10_moves():
    example = "389125467"
    labels = list(map(int, example))
    res = solve_part1(labels, 10)
    assert res == "92658374"


def test_part1_100_moves():
    example = "389125467"
    labels = list(map(int, example))
    res = solve_part1(labels, 100)
    assert res == "67384529"


def part2():
    res = solve_part2("974618352")
    print("part 2:", res)


class Cup:
    __slots__ = ("number", "previous", "next")

    def __init__(self, number):
        self.number = number
        self.previous = None
        self.next = None

    def forward_link(self, other):
        self.next = other

    def back_link(self, other):
        self.previous = other


class Ring:
    def __init__(self, labels):
        self._map = {}
        assert len(labels) > 1
        first = Cup(labels[0])
        self._map[first.number] = first

        cup = first
        for label in labels[1:]:
            new_cup = Cup(label)
            self._map[new_cup.number] = new_cup

            # Insert into chain:
            cup.forward_link(new_cup)
            new_cup.back_link(cup)

            cup = new_cup

        # complete loop:
        cup.forward_link(first)
        first.back_link(cup)

        self.current_cup = first

    def __contains__(self, item):
        return item in self._map

    def find(self, number):
        return self._map[number]

    def proceed(self):
        self.current_cup = self.current_cup.next

    def insert_after(self, cup, cups):
        before = self._map[cup]
        after = before.next

        cup1, cup2, cup3 = cups
        self._map[cup1.number] = cup1
        self._map[cup2.number] = cup2
        self._map[cup3.number] = cup3

        # Patch links:
        before.next = cup1
        cup1.previous = before

        cup3.next = after
        after.previous = cup3

    def take_three(self):

        # Select cups to take:
        before = self.current_cup
        cup1 = self.current_cup.next
        cup2 = cup1.next
        cup3 = cup2.next
        after = cup3.next

        # update mapping:
        self._map.pop(cup1.number)
        self._map.pop(cup2.number)
        self._map.pop(cup3.number)

        # Patch links:
        before.next = after
        after.previous = before

        return (cup1, cup2, cup3)


def solve_part2(labels):
    labels = list(map(int, labels))

    # extend to one million labels:
    new_label = max(labels) + 1
    while len(labels) < 1_000_000:
        labels.append(new_label)
        new_label += 1
    print("extended")
    ring = Ring(labels)

    min_label = min(labels)
    max_label = max(labels)
    print("min / maxed")

    num_rounds = 10_000_000
    for _round_nr in range(num_rounds):
        if _round_nr % 10000 == 0:
            pct = 100 * _round_nr / num_rounds
            print(f"{pct:0.2f} %")

        # remove 3 cups:
        taken = ring.take_three()
        # print('pick up', taken)

        # select destination cup:
        destination = ring.current_cup.number - 1
        while destination not in ring:
            destination -= 1
            if destination < min_label:
                destination = max_label

        ring.insert_after(destination, taken)

        ring.proceed()

    one_cup = ring.find(1)
    nr1 = one_cup.next.number
    nr2 = one_cup.next.next.number
    return nr1 * nr2


def test_part2():
    res = solve_part2("389125467")
    assert res == 149245887792


if __name__ == "__main__":
    part1()
    part2()
