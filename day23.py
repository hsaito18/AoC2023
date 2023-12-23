import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day23.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

GOAL = (len(lines) - 1, len(lines[0]) - 2)
# GOAL = (5, 3)


def get_possibilities(r, c):
    if lines[r][c] == ">":
        return [(r, c + 1)]
    if lines[r][c] == "<":
        return [(r, c - 1)]
    if lines[r][c] == "^":
        return [(r - 1, c)]
    if lines[r][c] == "v":
        return [(r + 1, c)]
    possibilities = []
    for nr in [r - 1, r + 1]:
        if nr < 0 or nr >= len(lines):
            continue
        if lines[nr][c] in ["#", ">", "<"]:
            continue
        if lines[nr][c] == "^" and nr == r + 1:
            continue
        if lines[nr][c] == "v" and nr == r - 1:
            continue
        possibilities.append((nr, c))
    for nc in [c - 1, c + 1]:
        if nc < 0 or nc >= len(lines[r]):
            continue
        if lines[r][nc] in ["#", "^", "v"]:
            continue
        if lines[r][nc] == "<" and nc == c + 1:
            continue
        if lines[r][nc] == ">" and nc == c - 1:
            continue
        possibilities.append((r, nc))
    return possibilities


def get_possibilities_2(r, c):
    possibilities = []
    for nr in [r - 1, r + 1]:
        if nr < 0 or nr >= len(lines):
            continue
        if lines[nr][c] in ["#"]:
            continue
        possibilities.append((nr, c))
    for nc in [c - 1, c + 1]:
        if nc < 0 or nc >= len(lines[r]):
            continue
        if lines[r][nc] in ["#"]:
            continue
        possibilities.append((r, nc))
    return possibilities


def get_longest_path(r, c, visited):
    print((r, c))
    if (r, c) == GOAL:
        return 0
    possibilities = get_possibilities(r, c)
    if len(possibilities) == 0:
        return 0
    longest = 0
    for possibility in possibilities:
        if possibility in visited:
            continue
        visited.add(possibility)
        longest = max(
            longest, 1 + get_longest_path(possibility[0], possibility[1], visited)
        )
    return longest


def get_all_coords(lines):
    coords = set()
    for r, row in enumerate(lines):
        for c, char in enumerate(row):
            if char != "#":
                coords.add((r, c))
    return coords


from collections import deque
from copy import deepcopy

start_point = (0, 1)
visited = set()
path = []
visited.add(start_point)
que = deque()
que.append((start_point, visited, path))
max_len = 0
while que:
    curr, visit, p = que.popleft()
    if curr == GOAL:
        print(len(visit))
        if len(visit) > max_len:
            max_len = len(visit)
            # print(p)
            # print(max_len)
            # test = (0, 1)
            # print(test in visit)
        continue

    possibilities = get_possibilities_2(curr[0], curr[1])
    filtered_possibilities = list(filter(lambda x: x not in visit, possibilities))
    for possibility in filtered_possibilities:
        vis = deepcopy(visit)
        pa = deepcopy(p)
        vis.add(possibility)
        # pa.append(possibility)
        que.append((possibility, vis, pa))

print(f"Part 1 ans: {max_len - 1}")  # 2018
nodes = [{"rc": (0, 1), "children": {}, "possibilities": [(1, 1)]}]
node_set = set()
node_set.add((0, 1))
coords_to_node = {(0, 1): 0}
for r, row in enumerate(lines):
    for c, char in enumerate(row):
        if char == "#":
            continue
        poss = get_possibilities_2(r, c)
        if len(poss) > 2:
            nodes.append({"rc": (r, c), "children": {}, "possibilities": poss})
            node_set.add((r, c))
            coords_to_node[(r, c)] = len(nodes) - 1

nodes.append({"rc": GOAL, "children": {}, "possibilities": []})
node_set.add(GOAL)
coords_to_node[GOAL] = len(nodes) - 1
GOAL_IDX = len(nodes) - 1
for node in nodes:
    for poss in node["possibilities"]:
        dist = 0
        last_visited = node["rc"]
        while True:
            if poss in node_set:
                node["children"][poss] = dist + 1
                break
            possibilities = get_possibilities_2(poss[0], poss[1])
            possibilities.remove(last_visited)
            if (len(possibilities)) == 0:
                break
            last_visited = poss
            poss = possibilities[0]
            dist += 1

start_point = (0, 1)

visited = set()
visited.add(start_point)

que = deque()
que.append((0, visited, 0))
max_len = 0
while que:
    curr_idx, visit, dist = que.popleft()
    # print(curr_idx, GOAL_IDX)
    node = nodes[curr_idx]
    if curr_idx == GOAL_IDX:
        # print(dist, max_len)
        if dist > max_len:
            max_len = dist
            # print(p)
            # print(max_len)
            # test = (0, 1)
            # print(test in visit)
        continue
    for possibility in node["children"]:
        poss_idx = coords_to_node[possibility]
        if poss_idx in visit:
            continue
        poss_dist = node["children"][possibility]
        vis = deepcopy(visit)
        vis.add(poss_idx)
        # pa.append(possibility)
        que.append((poss_idx, vis, dist + poss_dist))

print(max_len)  # 6406
