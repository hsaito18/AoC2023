import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day8.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

from math import lcm

nodes = {}
directions = lines[0]
nodes_lines = lines[2:]
for line in nodes_lines:
    nodes[line[0:3]] = {"L": line[7:10], "R": line[12:15]}

steps = 0
i = 0
curr_node = "AAA"
while curr_node != "ZZZ":
    curr_node = nodes[curr_node][directions[i]]
    steps += 1
    i += 1
    if i == len(directions):
        i = 0

curr_nodes = []
for node in nodes:
    if node[2] == "A":
        curr_nodes.append(node)

steps2 = 0
i = 0

# Let's examine curr_nodes[0]
node = curr_nodes[5]
start_node = curr_nodes[0]
success_hits = []
for l in range(100000):
    node = nodes[node][directions[i]]
    steps2 += 1
    i += 1
    if i == len(directions):
        i = 0
    if node[2] == "Z":
        success_hits.append(steps2)

diffs = [success_hits[0]]
for i in range(1, len(success_hits) - 1):
    diffs.append(success_hits[i] - success_hits[i - 1])

# print(diffs)
# 0: 17873
# 1: 19631
# 2: 17287
# 3: 12599
# 4: 21389
# 5: 20803
steps2 = lcm(17873, 19631, 17287, 12599, 21389, 20803)

print(f"Part 1 ans: {steps}")
print(f"Part 2 ans: {steps2}")
