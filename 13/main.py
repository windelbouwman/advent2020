import math
import functools


def main():
    part1()
    part2()


def load_data():
    with open("input.txt", "r") as f:
        for row, line in enumerate(f, 1):
            line = line.strip()
            if row == 1:
                earliest_departure = int(line)
            elif row == 2:
                buses = line.split(",")
    return earliest_departure, buses


def calculate_departure_after(bus_id, after_timestamp):
    remain = after_timestamp % bus_id
    timestamp = after_timestamp - remain
    assert timestamp <= after_timestamp
    assert timestamp % bus_id == 0
    while timestamp < after_timestamp:
        timestamp += bus_id
    return timestamp


def part1():
    earliest_departure, buses = load_data()

    bus_ids = [int(b) for b in buses if b != "x"]
    print("Bus ids", bus_ids)
    bus_departures = [
        (b, calculate_departure_after(b, earliest_departure)) for b in bus_ids
    ]
    print("Bus departues", bus_departures)
    bus_id, bus_departure = min(bus_departures, key=lambda x: x[1])
    wait_time = bus_departure - earliest_departure
    answer = bus_id * wait_time
    print(f"Earliest bus: {bus_id}, time to wait {wait_time}, multiplied: {answer}")


def is_prime(n):
    """Test if the given integer is prime.

    Ripped from Wikipedia

    """
    if n <= 3:
        # The small primes, 2, 3
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        # divisible by 2 or 3
        return False

    # 6k+-1 mode:
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def part2():
    _, buses = load_data()
    bus_offset_pairs = [(int(b), o) for o, b in enumerate(buses) if b != "x"]

    # Idea 2: this looks like the chinese remainder theorem.
    t = solve_buses(bus_offset_pairs)
    print("time at which all buses are departing in line", t)


def solve_buses(bus_offset_pairs):
    # print("bus offset pairs", bus_offset_pairs)

    bus_ids = [b[0] for b in bus_offset_pairs]

    if all(is_prime(b) for b in bus_ids):
        print("Bus id are all primes")
    else:
        return

    # offsets = [b[1] % b[0] for b in bus_offset_pairs]
    offsets = [b[1] for b in bus_offset_pairs]
    mo = max(offsets)
    offsets2 = [mo - o for o in offsets]

    gcd = math.gcd(*bus_ids)
    print(f"GCD of bus ids = {gcd} (must be 1 for co primes)")
    # If this is true, we have co-prime number set!
    assert gcd == 1

    return chinese_remainder(bus_ids, offsets2) - mo


def chinese_remainder(n, a):
    # print("primes", n, "remainers", a)
    assert len(n) == len(a)
    prod = functools.reduce(lambda x, y: x * y, n)
    s = 0
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        s += a_i * mul_inv(p, n_i) * p
    return s % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1

    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def test_chinese_remainder():
    n = [3, 5, 7]
    a = [2, 3, 2]
    r = chinese_remainder(n, a)
    assert r == 23


def test_example2():
    buses = "7,13,x,x,59,x,31,19".split(",")
    bus_offset_pairs = [(int(b), o) for o, b in enumerate(buses) if b != "x"]
    r = solve_buses(bus_offset_pairs)
    assert r == 1068781


if __name__ == "__main__":
    main()
