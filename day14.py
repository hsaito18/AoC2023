import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day14.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

from operator import itemgetter


def get_load(rocks):
    total_load = 0
    for rock in rocks:
        total_load += len(lines) - rock[0]
    return total_load


def get_north_end(r, c, rocks, walls):
    for nr in range(r - 1, -1, -1):
        if (nr, c) in rocks or walls[nr][c]:
            return nr + 1
    return 0


def get_east_end(r, c, rocks, walls, size):
    for nc in range(c + 1, size):
        if (r, nc) in rocks or walls[r][nc]:
            return nc - 1
    return size - 1


def get_south_end(r, c, rocks, walls, size):
    for nr in range(r + 1, size):
        if (nr, c) in rocks or walls[nr][c]:
            return nr - 1
    return size - 1


def get_west_end(r, c, rocks, walls):
    for nc in range(c - 1, -1, -1):
        if (r, nc) in rocks or walls[r][nc]:
            return nc + 1
    return 0


def roll_east(rocks, walls, size, history):
    sorted_rocks = sorted(rocks, key=itemgetter(1), reverse=True)
    new_rocks = sorted_rocks.copy()
    for i, rock in enumerate(sorted_rocks):
        nc = get_east_end(rock[0], rock[1], new_rocks, walls, size)
        new_rocks[i] = (rock[0], nc)
        history[i].append((rock[0], nc))
    return new_rocks


def roll_south(rocks, walls, size, history):
    sorted_rocks = sorted(rocks, key=itemgetter(0), reverse=True)
    new_rocks = sorted_rocks.copy()
    for i, rock in enumerate(sorted_rocks):
        nr = get_south_end(rock[0], rock[1], new_rocks, walls, size)
        new_rocks[i] = (nr, rock[1])
        history[i].append((nr, rock[1]))
    return new_rocks


def roll_north(rocks, walls, history):
    sorted_rocks = sorted(rocks, key=itemgetter(0))
    new_rocks = sorted_rocks.copy()
    for i, rock in enumerate(sorted_rocks):
        nr = get_north_end(rock[0], rock[1], new_rocks, walls)
        new_rocks[i] = (nr, rock[1])
        history[rock[2]].append((nr, rock[1]))
    return new_rocks


def roll_west(rocks, walls, history):
    sorted_rocks = sorted(rocks, key=itemgetter(1))
    new_rocks = sorted_rocks.copy()
    for i, rock in enumerate(sorted_rocks):
        nc = get_west_end(rock[0], rock[1], new_rocks, walls)
        new_rocks[i] = (rock[0], nc)
        history[i].append((rock[0], nc))
    return new_rocks


def roll_cycle(rocks, walls, size, history):
    new_hist = [[] for x in range(len(history))]
    new_rocks = roll_north(rocks, walls, new_hist)
    new_rocks = roll_west(new_rocks, walls, new_hist)
    new_rocks = roll_south(new_rocks, walls, size, new_hist)
    new_rocks = roll_east(new_rocks, walls, size, new_hist)
    for hist, new in zip(history, new_hist):
        hist.append(new)
    return new_rocks


def check_if_stuck(rock_history, margin):
    return False
    if len(rock_history) < margin:
        return False
    init_coord = rock_history[-margin]
    for coords in rock_history[-(margin - 1) :]:
        if coords != init_coord:
            return False
    return True


def roll_n_cycles(n, rocks, walls, size):
    new_rocks = rocks.copy()
    rock_history = [[] for i in range(len(new_rocks))]
    total_load = 0
    for i in range(n):
        print(f"{i}/{n} cycles...  load: {get_load(new_rocks)}")
        new_rocks = roll_cycle(new_rocks, walls, size, rock_history)
    print(f"{n}/{n} cycles...     LOAD: {total_load}")
    return new_rocks


rocks = []
rock_locations = []
walls = [[False for j in range(len(lines))] for i in range(len(lines))]

count = 0
for r, line in enumerate(lines):
    for c, char in enumerate(line):
        if char == "#":
            walls[r][c] = True
        if char == "O":
            rocks.append((r, c, count))
            rock_locations.append((r, c))
            count += 1

out = roll_n_cycles(10000, rocks, walls, len(lines))

total_load = 0
for rock in rocks:
    total_load += len(lines) - rock[0]

print(f"Part 1 ans: {total_load}")
print(f"Part 2 ans: {95254}")  # hee hee xd
