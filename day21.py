import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day21.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()


from collections import deque

for r, line in enumerate(lines):
    for c, char in enumerate(line):
        if char == "S":
            pos = (r, c)

STEPS_LIMIT = 64
STEPS_LIMIT_2 = 65


def get_valid_adj(r, c):
    valids = []
    for nr in [r - 1, r + 1]:
        if nr < 0 or nr >= len(lines):
            continue
        if lines[nr][c] == "#":
            continue
        valids.append((nr, c))
    for nc in [c - 1, c + 1]:
        if nc < 0 or nc >= len(lines[0]):
            continue
        if lines[r][nc] == "#":
            continue
        valids.append((r, nc))
    return valids


def get_char(r, c):
    lines_r = len(lines)
    lines_c = len(lines[0])
    adj_r = r % lines_r
    adj_c = c % lines_c
    return lines[adj_r][adj_c]


def get_valid_inf_adj(r, c):
    valids = []
    for nr in [r - 1, r + 1]:
        if get_char(nr, c) == "#":
            continue
        valids.append((nr, c))
    for nc in [c - 1, c + 1]:
        if get_char(r, nc) == "#":
            continue
        valids.append((r, nc))
    return valids


even_visited = set()
odd_visited = set()
searchers = []
searchers.append(pos)
for i in range(STEPS_LIMIT + 1):
    print(f"{i}/64, also {len(searchers)}")
    steps = i
    next_searchers = []
    ns_set = set()
    even = steps % 2 == 0
    curr_set = even_visited if even else odd_visited
    next_set = odd_visited if even else even_visited
    for search in searchers:
        curr_set.add(search)
        valids = get_valid_adj(search[0], search[1])
        for v in valids:
            if v in next_set:
                continue
            if v in ns_set:
                continue
            next_searchers.append(v)
            ns_set.add(v)
    searchers = next_searchers

# print((even_visited))
print(len(even_visited))


even_visited_2 = set()
odd_visited_2 = set()
searchers_2 = []
searchers_2.append(pos)
for i in range(STEPS_LIMIT_2 + 1):
    # print(f"{i}/{STEPS_LIMIT_2}, also {len(searchers_2)}")
    steps = i
    next_searchers_2 = []
    ns_set = set()
    even = steps % 2 == 0
    curr_set = even_visited_2 if even else odd_visited_2
    next_set = odd_visited_2 if even else even_visited_2
    for search in searchers_2:
        curr_set.add(search)
        valids = get_valid_inf_adj(search[0], search[1])
        for v in valids:
            if v in next_set:
                continue
            if v in ns_set:
                continue
            next_searchers_2.append(v)
            ns_set.add(v)
    searchers_2 = next_searchers_2

# print((even_visited_2))
print(len(even_visited_2))
import numpy as np

a0 = 3701
a1 = 33108
a2 = 91853
vandermonde = np.matrix([[0, 0, 1], [1, 1, 1], [4, 2, 1]])
b = np.array([a0, a1, a2])
x = np.linalg.solve(vandermonde, b).astype(np.int64)
n = 202300
print("part 2:", x[0] * n * n + x[1] * n + x[2])
