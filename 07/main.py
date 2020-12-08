import networkx as nx

from pprint import pprint
import re

def load_bags():
    prog = re.compile('^(\d+) (.*) bags?$')
    bags = []
    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            # print(line)
            if 'bags contain' in line:
                bag, content_line = line.split('bags contain')
                bag = bag.strip()

                contents = []

                content_line = content_line.strip()
                assert content_line.endswith('.')
                content_line = content_line[:-1]  # Strip off trailing dot

                if content_line != 'no other bags':
                    for item in content_line.split(','):
                        item = item.strip()
                        mo = prog.match(item)
                        # print(mo)
                        amount = int(mo.group(1))
                        name = mo.group(2)
                        # print(item, mo.group(1), mo.group(2))
                        contents.append((amount, name))
                bags.append((bag, contents))
    return bags


bags = load_bags()

# pprint(bags)

# Part 1:
g = nx.DiGraph()
for bag, contents in bags:
    for amount, item in contents:
        g.add_edge(bag, item, weight=amount)

a = nx.algorithms.dag.ancestors(g, 'shiny gold')
print('possible containers:', len(a))

# Part 2:
cost_map = {}

for n in nx.dfs_postorder_nodes(g, 'shiny gold'):
    cost = 1  # the bag itself!
    for sub in g.successors(n):
        weight = g.get_edge_data(n, sub)['weight']
        cost += weight * cost_map[sub]
    assert n not in cost_map
    cost_map[n] = cost

print('total amount of bags in own bag:', cost_map['shiny gold'] - 1)