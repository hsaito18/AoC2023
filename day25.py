import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day25.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

import networkx as nx

components = set()
G = nx.Graph()
for line in lines:
    curr_comp = line[:3]
    others = line[5:]
    others_list = others.split(" ")
    components.add(curr_comp)
    for comp in others_list:
        G.add_edge(curr_comp, comp, capacity=1)
        components.add(comp)


def get_ans(G, components):
    for c1 in components:
        for c2 in components:
            if c1 == c2:
                continue
            num_cuts, groups = nx.minimum_cut(G, c1, c2)
            if num_cuts == 3:
                return len(groups[0]) * len(groups[1])


ans = get_ans(G, components)

print(f"Part 1 ans: {ans}")
