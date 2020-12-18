import re


def load_expressions():
    expressions = []
    with open("input.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                expressions.append(line)
    return expressions


def part1():
    expressions = load_expressions()
    print("part 1", sum(eval_expr1(e) for e in expressions))


def tokenize(line):
    spec = [
        ("SKIP", r"[ ]+"),
        ("NUM", r"\d+"),
        ("OP", r"[\*\+\)\(]"),
        ("ERR", r"."),
    ]
    prog = "|".join(f"(?P<{n}>{p})" for n, p in spec)

    for mo in re.finditer(prog, line):
        kind = mo.lastgroup
        value = mo.group()
        if kind == "SKIP":
            continue
        elif kind == "OP":
            yield value
        elif kind == "NUM":
            yield int(value)
        else:
            raise ValueError(f"Invalid char [{value}]")


ops = {
    "+": lambda a, b: a + b,
    "*": lambda a, b: a * b,
}


def eval_expr1(expression):
    """Try to use shunting yard algorithm.
    https://en.wikipedia.org/wiki/Shunting-yard_algorithm
    """

    output = []
    stack = []
    tokens = list(tokenize(expression))

    for token in tokens:
        if token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                op = stack.pop(-1)
                output.append(op)
            op = stack.pop(-1)
            assert op == "("
        elif token in ["+", "*"]:
            if stack and stack[-1] in ["+", "*"]:
                op = stack.pop(-1)
                output.append(op)

            stack.append(token)
        elif isinstance(token, int):
            output.append(token)
        else:
            raise NotImplementedError(token)

        # print(token, output, stack)

    while stack and stack[-1] in ["+", "*"]:
        op = stack.pop(-1)
        output.append(op)

    assert not stack

    return eval_ops(output)


def eval_ops(opcodes):
    """ Evaluate a byte codes. """
    output = []
    for op in opcodes:
        if op in ["+", "*"]:
            b = output.pop(-1)
            a = output.pop(-1)
            value = ops[op](a, b)
            output.append(value)
        else:
            output.append(op)

    assert len(output) == 1
    return output[0]


def test_part1_1():
    assert 26 == eval_expr1("2 * 3 + (4 * 5)")


def test_part1_2():
    assert 437 == eval_expr1("5 + (8 * 3 + 9 + 3 * 4 * 3)")


def test_part1_3():
    assert 12240 == eval_expr1("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")


def test_part1_4():
    assert 13632 == eval_expr1("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")


def part2():
    expressions = load_expressions()
    print("part 2", sum(eval_expr2(e) for e in expressions))


def eval_expr2(expression):
    """Try to use shunting yard algorithm.
    https://en.wikipedia.org/wiki/Shunting-yard_algorithm
    """

    output = []
    stack = []
    tokens = list(tokenize(expression))

    precedence = {
        "*": 10,
        "+": 20,
    }

    for token in tokens:
        if token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                op = stack.pop(-1)
                output.append(op)
            op = stack.pop(-1)
            assert op == "("
        elif token in ["+", "*"]:
            while (
                stack
                and stack[-1] in ["+", "*"]
                and precedence[token] < precedence[stack[-1]]
            ):
                op = stack.pop(-1)
                output.append(op)

            stack.append(token)
        elif isinstance(token, int):
            output.append(token)
        else:
            raise NotImplementedError(token)

        # print(token, output, stack)

    while stack and stack[-1] in ["+", "*"]:
        op = stack.pop(-1)
        output.append(op)

    assert not stack

    return eval_ops(output)


def test_part2_1():
    assert 46 == eval_expr2("2 * 3 + (4 * 5)")


def test_part2_2():
    assert 1445 == eval_expr2("5 + (8 * 3 + 9 + 3 * 4 * 3)")


def test_part2_3():
    assert 669060 == eval_expr2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")


def test_part2_4():
    assert 23340 == eval_expr2("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")


if __name__ == "__main__":
    part1()
    part2()
