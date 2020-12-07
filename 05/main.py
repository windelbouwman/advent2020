
def load_tickets():
    with open('input.txt', 'r') as f:
        tickets = []
        for line in f:
            line = line.strip()
            if line:
                row = int(line[0:7].replace('B', '1').replace('F', '0'), 2)
                col = int(line[7:10].replace('R', '1').replace('L', '0'), 2)
                id = row * 8 + col
                tickets.append((id, row, col))
    return tickets

tickets = load_tickets()
used_ids = [t[0] for t in tickets]
print('Highest ID', max(used_ids))

all_seats = set(range(1024))
used_seats = set(used_ids)
free_seats = all_seats - used_seats
print('My seat:', list(filter(lambda s: (((s + 1) in used_seats) and (s - 1) in used_seats), free_seats)))

