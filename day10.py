import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day10.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

# pipe_pos - curr_pos are keys
PIPES = {
    "|": {(1, 0): (1, 0), (-1, 0): (-1, 0)},
    "-": {(0, 1): (0, 1), (0, -1): (0, -1)},
    "L": {(1, 0): (0, 1), (0, -1): (-1, 0)},
    "J": {(1, 0): (0, -1), (0, 1): (-1, 0)},
    "7": {(-1, 0): (0, -1), (0, 1): (1, 0)},
    "F": {(-1, 0): (0, 1), (0, -1): (1, 0)},
}

SOUTHS = set(("|", "7", "F"))
NORTHS = set(("|", "L", "J"))
EASTS = set(("-", "L", "F"))
WESTS = set(("-", "7", "J"))


STARTING_PIPE = "|"
S_REPLACEMENT = "F"


def add_tuple(t1, t2):
    return tuple([sum(x) for x in zip(t1, t2)])


def sub_tuple(t1, t2):
    return tuple([x[0] - x[1] for x in zip(t1, t2)])


def check_next_to(r, c, set):
    if (r - 1, c) in set:
        return True
    if (r + 1, c) in set:
        return True
    if (r, c - 1) in set:
        return True
    if (r, c + 1) in set:
        return True
    return False


start_pos = (0, 0)
for r, line in enumerate(lines):
    if line.find("S") != -1:
        start_pos = (r, line.find("S"))
        break

# next_move = PIPES["F"][(0, -1)]
next_move = PIPES[STARTING_PIPE][(1, 0)]
# last_pipe_coord = add_tuple(start_pos, (0, -1))
last_pipe_coord = add_tuple(start_pos, (1, 0))
steps = 2
loop_coords = set((start_pos, last_pipe_coord))
while True:
    next_pipe_coord = add_tuple(last_pipe_coord, next_move)
    loop_coords.add(next_pipe_coord)
    next_pipe = lines[next_pipe_coord[0]][next_pipe_coord[1]]
    if next_pipe == "S":
        break
    delta_coords = sub_tuple(next_pipe_coord, last_pipe_coord)
    next_move = PIPES[next_pipe][delta_coords]
    last_pipe_coord = next_pipe_coord
    curr_pipe = next_pipe
    steps += 1

expanded = []
for line in lines:
    new_line = []
    for c in line:
        new_line.append(c)
        new_line.append("0")
    expanded.append(new_line)
    expanded.append(["0"] * len(line) * 2)

for r, line in enumerate(expanded):
    print(len(line))
    for c, char in enumerate(line):
        if char != "0":
            continue
        if r != 0 and r != len(expanded) - 1:
            up = expanded[r - 1][c]
            if up == "S":
                up = S_REPLACEMENT
            down = expanded[r + 1][c]
            if down == "S":
                down = S_REPLACEMENT
            if down in NORTHS and up in SOUTHS:
                expanded[r][c] = "|"
                continue
        if c != 0 and c != len(line) - 1:
            left = expanded[r][c - 1]
            if left == "S":
                left = S_REPLACEMENT
            right = expanded[r][c + 1]
            if right == "S":
                right = S_REPLACEMENT
            if right in WESTS and left in EASTS:
                expanded[r][c] = "-"

start_pos = (0, 0)
for r, line in enumerate(expanded):
    for c, char in enumerate(line):
        if char == "S":
            start_pos = (r, c)
            break

# next_move = PIPES["F"][(0, -1)]
next_move = PIPES["|"][(1, 0)]
# last_pipe_coord = add_tuple(start_pos, (0, -1))
last_pipe_coord = add_tuple(start_pos, (1, 0))
loop_coords_2 = set((start_pos, last_pipe_coord))
steps2 = 2
print(expanded[8])
while True:
    next_pipe_coord = add_tuple(last_pipe_coord, next_move)
    loop_coords_2.add(next_pipe_coord)
    next_pipe = expanded[next_pipe_coord[0]][next_pipe_coord[1]]
    # print(next_pipe, next_pipe_coord)
    if next_pipe == "S":
        break
    delta_coords = sub_tuple(next_pipe_coord, last_pipe_coord)
    next_move = PIPES[next_pipe][delta_coords]
    last_pipe_coord = next_pipe_coord
    curr_pipe = next_pipe
    steps2 += 1


out_coords = set()
for i in range(100):
    for r, line in enumerate(expanded):
        for c, char in enumerate(line):
            if (r, c) in loop_coords_2:
                continue
            if r == 0 or r == len(expanded) - 1 or c == 0 or c == len(expanded) - 1:
                out_coords.add((r, c))
                continue
            if check_next_to(r, c, out_coords):
                out_coords.add((r, c))
total_coords = len(expanded) * len(expanded[0])
in_coords = set()
for r, line in enumerate(expanded):
    for c, char in enumerate(line):
        if (
            (r, c) not in out_coords
            and (r, c) not in loop_coords_2
            and r % 2 == 0
            and c % 2 == 0
        ):
            in_coords.add((int(r / 2), int(c / 2)))
print(f"Part 1 ans: {steps/2}")
print(total_coords, len(out_coords), len(loop_coords_2))
print(total_coords - len(out_coords) - len(loop_coords_2))
# 834 is the non leaking num. Too high.
# 800 too high...
print(in_coords)
