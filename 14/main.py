import re
import itertools


def load_program():
    with open("input.txt", "r") as f:
        instructions = load_lines(line.strip() for line in f)
    return instructions


def load_lines(lines):
    mask_prog = re.compile(r"^mask = ([10X]+)$")
    mem_prog = re.compile(r"^mem\[(\d+)\] = (\d+)$")
    instructions = []
    for line in lines:
        if m := mem_prog.match(line):
            address = int(m.group(1))
            value = int(m.group(2))
            instructions.append(("mem", (address, value)))
        elif m := mask_prog.match(line):
            mask = m.group(1)
            instructions.append(("mask", (mask,)))
    return instructions


def part1():
    instructions = load_program()
    print("part1", solve_part1(instructions))


def solve_part1(instructions):
    mem = {}
    mask_mask, mask_value = None, None
    for opcode, operands in instructions:
        if opcode == "mem":
            address, value = operands
            value = (value & mask_mask) | mask_value
            mem[address] = value
        elif opcode == "mask":
            (mask,) = operands
            mask_value = int(mask.replace("X", "0"), 2)
            mask_mask = int(mask.replace("1", "0").replace("X", "1"), 2)

    return sum(mem.values())


def part2():
    instructions = load_program()
    print("part2", solve_part2(instructions))


def solve_part2(instructions):
    mem = {}
    one_bits = None
    float_bits = None
    for opcode, operands in instructions:
        if opcode == "mem":
            address, value = operands
            # apply crazy address operator:
            for address in gen_addresses(address, one_bits, float_bits):
                mem[address] = value
        elif opcode == "mask":
            (mask,) = operands
            one_bits = [i for i, b in enumerate(reversed(mask)) if b == "1"]
            float_bits = [i for i, b in enumerate(reversed(mask)) if b == "X"]

    return sum(mem.values())


def gen_addresses(base, one_bits, float_bits):
    for bit in one_bits:
        base |= 1 << bit

    masks = []
    for bit in float_bits:
        mask = 1 << bit
        base &= ~mask
        masks.append([0, mask])

    for masks in itertools.product(*masks):
        a = base
        for m in masks:
            a |= m
        yield a


def main():
    part1()
    part2()


def test_example1():
    lines = [
        "mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
        "mem[8] = 11",
        "mem[7] = 101",
        "mem[8] = 0",
    ]
    instructions = load_lines(lines)
    res = solve_part1(instructions)
    assert res == 165


def test_example2():
    lines = [
        "mask = 000000000000000000000000000000X1001X",
        "mem[42] = 100",
        "mask = 00000000000000000000000000000000X0XX",
        "mem[26] = 1",
    ]

    instruction = load_lines(lines)
    res = solve_part2(instruction)
    assert res == 208


if __name__ == "__main__":
    main()
