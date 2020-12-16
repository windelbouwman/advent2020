from pprint import pprint
import functools
import re


def load_tickets():
    with open("input.txt", "r") as f:
        return load_tickets_from_lines(f)


def load_tickets_from_lines(lines):
    prog = re.compile(r"^(.+): (\d+)-(\d+) or (\d+)-(\d+)$")
    criteria = []
    my_ticket = None
    nearby_tickets = []

    section = 1
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line == "your ticket:":
            section = 2
        elif line == "nearby tickets:":
            section = 3
        else:
            if section == 1:
                mo = prog.match(line)
                field = mo.group(1)
                s1 = int(mo.group(2))
                e1 = int(mo.group(3))
                s2 = int(mo.group(4))
                e2 = int(mo.group(5))
                ranges = (range(s1, e1 + 1), range(s2, e2 + 1))
                criteria.append((field, ranges))
            elif section == 2:
                assert not my_ticket
                my_ticket = list(map(int, line.split(",")))
            elif section == 3:
                ticket = list(map(int, line.split(",")))
                nearby_tickets.append(ticket)
            else:
                raise NotImplementedError(str(section))

    return criteria, my_ticket, nearby_tickets


def part1():
    criteria, my_ticket, nearby_tickets = load_tickets()
    print("Error rate:", solve_part1(criteria, nearby_tickets))


def solve_part1(criteria, nearby_tickets):
    # pprint(criteria)

    # valid ranges:
    valid_ranges = []
    for field, ranges in criteria:
        valid_ranges.extend(ranges)

    error_rate = 0
    for ticket in nearby_tickets:
        for value in ticket:
            if not in_range_set(value, valid_ranges):
                # print('Error:', value)
                error_rate += value
            # else:
            #     print('OK', value)
    return error_rate


def test_example1():
    example = """
    class: 1-3 or 5-7
    row: 6-11 or 33-44
    seat: 13-40 or 45-50

    your ticket:
    7,1,14

    nearby tickets:
    7,3,47
    40,4,50
    55,2,20
    38,6,12
    """
    criteria, _, nearby_tickets = load_tickets_from_lines(example.splitlines())
    error_rate = solve_part1(criteria, nearby_tickets)
    assert error_rate == 71


def part2():
    criteria, my_ticket, nearby_tickets = load_tickets()
    ticket = solve_part2(criteria, my_ticket, nearby_tickets)
    departure_values = [v for n, v in ticket.items() if n.startswith("departure")]
    assert len(departure_values) == 6
    print("part 2", functools.reduce(lambda x, y: x * y, departure_values))


def in_range_set(value, range_set):
    return any(value in r for r in range_set)


def solve_part2(criteria, my_ticket, nearby_tickets):
    valid_ranges = []
    for field, ranges in criteria:
        valid_ranges.extend(ranges)

    valid_tickets = []
    for ticket in nearby_tickets:
        is_valid = True
        for value in ticket:
            # Check if value can be used or not:
            if not in_range_set(value, valid_ranges):
                is_valid = False

        if is_valid:
            valid_tickets.append(ticket)

    # construct columns:
    columns = list([] for _ in my_ticket)
    for ticket in valid_tickets:
        for i, num in enumerate(ticket):
            columns[i].append(num)

    # Determine column options per field:
    column_options = {}
    for field, ranges in criteria:
        options = set()
        for idx, column in enumerate(columns):
            if all(in_range_set(v, ranges) for v in column):
                options.add(idx)
        column_options[field] = options

    field_columns = {}
    while column_options:
        # Select candidate:
        for field, options in column_options.items():
            if len(options) == 1:
                break
        else:
            raise ValueError("No solution!")

        # Remove this column, as it certainly is this one.
        options = column_options.pop(field)
        assert len(options) == 1
        idx = next(iter(options))

        # Store field-index map:
        field_columns[field] = idx

        # Update other options:
        for field in column_options:
            column_options[field].discard(idx)

    # Contrapt ticket dict:
    ticket = {name: my_ticket[index] for name, index in field_columns.items()}
    return ticket


def test_example2():
    example = """
    class: 0-1 or 4-19
    row: 0-5 or 8-19
    seat: 0-13 or 16-19

    your ticket:
    11,12,13

    nearby tickets:
    3,9,18
    15,1,5
    5,14,9
    """
    criteria, my_ticket, nearby_tickets = load_tickets_from_lines(example.splitlines())
    ticket = solve_part2(criteria, my_ticket, nearby_tickets)
    assert ticket == {
        "class": 12,
        "row": 11,
        "seat": 13,
    }


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
