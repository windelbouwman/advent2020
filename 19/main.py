from pprint import pprint
import re
import lark


def load_input():
    with open("input.txt", "r") as f:
        return load_from_lines(f)


def load_from_lines(lines):
    lines = iter(lines)

    rules = []
    for line in lines:
        line = line.strip()
        if line:
            nr, rule = line.split(": ")
            nr = int(nr)
            if rule[0] == '"' and rule[2] == '"':
                rule = rule[1]
            else:
                rule = tuple(tuple(map(int, r.split(" "))) for r in rule.split(" | "))
            rules.append((nr, rule))
        else:
            break

    messages = []
    for line in lines:
        line = line.strip()
        if line:
            messages.append(line)

    return rules, messages


def part1():
    rules, messages = load_input()
    res = solve_part1(rules, messages)
    print("part 1", res)


def solve_part1(rules, messages):
    # try to create a giant regex

    rule_map = {nr: impl for nr, impl in rules}
    rule_re = {}

    def get_regex(nr):
        if nr in rule_re:
            return rule_re[nr]
        else:
            impl = rule_map[nr]
            if isinstance(impl, str):
                r = impl
            else:
                alt_res = []
                for alt in impl:
                    re = "(" + "".join(get_regex(o) for o in alt) + ")"
                    alt_res.append(re)
                r = "(" + "|".join(alt_res) + ")"
            rule_re[nr] = r
            return r

    r = "^" + get_regex(0) + "$"

    prog = re.compile(r)

    n = 0
    for message in messages:
        if prog.match(message):
            n += 1
    return n


def test_part1():
    example = """0: 4 1 5
    1: 2 3 | 3 2
    2: 4 4 | 5 5
    3: 4 5 | 5 4
    4: "a"
    5: "b"

    ababbb
    bababa
    abbbab
    aaabbb
    aaaabbb
    """
    rules, messages = load_from_lines(example.splitlines())
    res = solve_part1(rules, messages)
    assert res == 2


def part2():
    rules, messages = load_input()
    res = solve_part2(rules, messages)
    print("part 2", res)


def rulify(opts):
    return " ".join(f"rule{o}" for o in opts)


def solve_part2(rules, messages):
    # construct grammar:
    grammar_lines = []
    for nr, impls in rules:
        # Patches by part 2:
        if nr == 8:
            impls = ((42,), (42, 8))
        elif nr == 11:
            impls = ((42, 31), (42, 11, 31))

        if isinstance(impls, str):
            line = f"rule{nr}: /{impls}/"
        else:
            rhs = " | ".join(rulify(impl) for impl in impls)
            line = f"rule{nr}: {rhs}"
        grammar_lines.append(line)

    grammar = "\n".join(grammar_lines)
    parser = lark.Lark(grammar, start="rule0")
    # print(parser)

    n = 0
    for message in messages:
        # print(message)
        try:
            parser.parse(message)
        except lark.exceptions.LarkError:
            # print('NACK')
            pass
        else:
            # print('OK')
            n += 1
    return n


def test_part2():
    example = """42: 9 14 | 10 1
    9: 14 27 | 1 26
    10: 23 14 | 28 1
    1: "a"
    11: 42 31
    5: 1 14 | 15 1
    19: 14 1 | 14 14
    12: 24 14 | 19 1
    16: 15 1 | 14 14
    31: 14 17 | 1 13
    6: 14 14 | 1 14
    2: 1 24 | 14 4
    0: 8 11
    13: 14 3 | 1 12
    15: 1 | 14
    17: 14 2 | 1 7
    23: 25 1 | 22 14
    28: 16 1
    4: 1 1
    20: 14 14 | 1 15
    3: 5 14 | 16 1
    27: 1 6 | 14 18
    14: "b"
    21: 14 1 | 1 14
    25: 1 1 | 1 14
    22: 14 14
    8: 42
    26: 14 22 | 1 20
    18: 15 15
    7: 14 5 | 1 21
    24: 14 1

    abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
    bbabbbbaabaabba
    babbbbaabbbbbabbbbbbaabaaabaaa
    aaabbbbbbaaaabaababaabababbabaaabbababababaaa
    bbbbbbbaaaabbbbaaabbabaaa
    bbbababbbbaaaaaaaabbababaaababaabab
    ababaaaaaabaaab
    ababaaaaabbbaba
    baabbaaaabbaaaababbaababb
    abbbbabbbbaaaababbbbbbaaaababb
    aaaaabbaabaaaaababaa
    aaaabbaaaabbaaa
    aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
    babaaabbbaaabaababbaabababaaab
    aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
    """
    rules, messages = load_from_lines(example.splitlines())
    res = solve_part2(rules, messages)
    assert res == 12


if __name__ == "__main__":
    part1()
    part2()
