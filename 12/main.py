"""
Ship moving!

0 degrees moves to east
90 degrees moves to north
180 degrees moves to west
270 degrees moves to south

rotating left increments the angle
rotating right decrements the angle

x axis positive to the east
y axis positive to the north
"""


def load_instructions():
    instructions = []
    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                opcode = line[0]
                operand = int(line[1:])
                instructions.append((opcode, operand))
    return instructions


def wrap360(a):
    while a >= 360:
        a -= 360

    while a < 0:
        a += 360

    return a

def manhattan_distance(x, y):
    return abs(x) + abs(y)


def execute(instructions):
    delta_map = {
        0: (1, 0),
        90: (0, 1),
        180: (-1, 0),
        270: (0, -1),
    }
    x, y, a = 0, 0, 0
    for opcode, operand in instructions:
        if opcode == 'S':
            y -= operand
        elif opcode == 'N':
            y += operand
        elif opcode == 'W':
            x -= operand
        elif opcode == 'E':
            x += operand
        elif opcode == 'L':
            a = wrap360(a + operand)
        elif opcode == 'R':
            a = wrap360(a - operand)
        elif opcode == 'F':
            dx, dy = delta_map[a]
            x += dx * operand
            y += dy * operand
        else:
            raise NotImplementedError(opcode)
        # print(opcode, operand, x, y, a)
    return x, y


def part1():
    instructions = load_instructions()
    x, y = execute(instructions)
    print('manhatten distance from 0,0: ', manhattan_distance(x, y))


def rotate_right(x, y, a):
    assert a >= 0
    while a > 0:
        # 90 degree right rotation:
        x, y = y, -x
        a -= 90
    assert a == 0
    return x, y


def rotate_left(x, y, a):
    assert a >= 0
    while a > 0:
        # 90 degree left rotation:
        x, y = -y, x
        a -= 90
    assert a == 0
    return x, y


def execute2(instructions):
    x, y, a = 0, 0, 0  # ship
    wx, wy = 10, 1  # way point
    for opcode, operand in instructions:
        if opcode == 'S':
            wy -= operand
        elif opcode == 'N':
            wy += operand
        elif opcode == 'W':
            wx -= operand
        elif opcode == 'E':
            wx += operand
        elif opcode == 'L':
            wx, wy = rotate_left(wx, wy, operand)
        elif opcode == 'R':
            wx, wy = rotate_right(wx, wy, operand)
        elif opcode == 'F':
            x += wx * operand
            y += wy * operand
        else:
            raise NotImplementedError(opcode)
        # print(opcode, operand, x, y, a, wx, wy)
    return x, y


def part2():
    instructions = load_instructions()
    x, y = execute2(instructions)
    print('manhatten distance from 0,0: ', manhattan_distance(x, y))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()


def test_example1():
    instructions = [
        ('F', 10),
        ('N', 3),
        ('F', 7),
        ('R', 90),
        ('F', 11),
    ]
    x, y = execute(instructions)
    assert x == 17
    assert y == -8


def test_example2():
    instructions = [
        ('F', 10),
        ('N', 3),
        ('F', 7),
        ('R', 90),
        ('F', 11),
    ]
    x, y = execute2(instructions)
    assert x == 214
    assert y == -72
