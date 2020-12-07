

def load_answers():
    with open('input.txt', 'r') as f:
        groups = []
        group = []
        for line in f:
            line = line.strip()
            if line:
                group.append(set(line))
            else:
                groups.append(group)
                group = []

        if group:
            groups.append(group)
    return groups


groups = load_answers()

# Part 1:
any_answers = [set.union(*group) for group in groups]
print(sum(len(u) for u in any_answers))

# Part 2:
all_answers = [set.intersection(*group) for group in groups]
print(sum(len(u) for u in all_answers))
