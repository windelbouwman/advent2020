def load_input():
    with open("input.txt", "r") as f:
        return load_from_lines(f)


def load_deck(lines, caption):
    p1 = next(lines).strip()
    assert p1 == caption
    deck = []
    for line in lines:
        line = line.strip()
        if line:
            deck.append(int(line))
        else:
            break
    return deck


def load_from_lines(lines):
    lines = iter(lines)
    deck1 = load_deck(lines, "Player 1:")
    deck2 = load_deck(lines, "Player 2:")
    return deck1, deck2


def part1():
    deck1, deck2 = load_input()
    score = solve_part1(deck1, deck2)
    print("part 1", score)


def solve_part1(deck1, deck2):
    while deck1 and deck2:
        t1, t2 = deck1.pop(0), deck2.pop(0)
        if t1 > t2:
            deck1.extend([t1, t2])
        else:
            assert t2 > t1
            deck2.extend([t2, t1])

    return deck_score(deck1 or deck2)


def deck_score(deck):
    return sum(i * c for i, c in enumerate(reversed(deck), 1))


example = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
"""


def test_part1():
    deck1, deck2 = load_from_lines(example.splitlines())
    score = solve_part1(deck1, deck2)
    assert score == 306


def part2():
    deck1, deck2 = load_input()
    score = solve_part2(deck1, deck2)
    print("part 2", score)


def solve_part2(deck1, deck2):
    _, deck = play_game(deck1, deck2)
    return deck_score(deck)


def play_game(deck1, deck2):
    """ Play a single game of Recursive Combat """
    history = set()

    while deck1 and deck2:
        key = str(deck1) + str(deck2)
        if key in history:
            return 1, deck1
        else:
            history.add(key)
            # Draw cards:
            t1, t2 = deck1.pop(0), deck2.pop(0)
            if len(deck1) >= t1 and len(deck2) >= t2:
                # sub game!
                sub_deck1 = list(deck1[:t1])
                sub_deck2 = list(deck2[:t2])
                pid, _ = play_game(sub_deck1, sub_deck2)
            else:
                # high card wins
                assert t1 != t2
                pid = 1 if t1 > t2 else 2

            if pid == 1:
                deck1.extend([t1, t2])
            else:
                deck2.extend([t2, t1])

    if deck1:
        return 1, deck1
    else:
        return 2, deck2


def test_part2():
    deck1, deck2 = load_from_lines(example.splitlines())
    res = solve_part2(deck1, deck2)
    assert res == 291


if __name__ == "__main__":
    part1()
    part2()
