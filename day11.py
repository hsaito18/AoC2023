import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day11.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

def check_empty_col(col_num, grid):
    for r in grid:
        if r[col_num] == "#": return False
    return True

def check_empty_row(row_num, grid):
    return not("#" in grid[row_num])

def get_man_dist(coords1, coords2):
    return abs(coords1[0]-coords2[0]) + abs(coords1[1]-coords2[1])

def get_expanded_dist(c1, c2, expansion, empty_rows, empty_cols):
    crossings = 0
    r1 = c1[0]
    r2 = c2[0]
    min_r = min(r1,r2)
    max_r = max(r1,r2)
    crossing_rows = range(min_r+1, max_r)
    for r in empty_rows:
        if r in crossing_rows:
            crossings += 1
    col1 = c1[1]
    col2 = c2[1]
    min_c = min(col1,col2)
    max_c = max(col1,col2)
    crossing_cols = range(min_c+1, max_c)
    for c in empty_cols:
        if c in crossing_cols:
            crossings += 1
    return get_man_dist(c1,c2) + crossings * expansion    

empty_rows = set()
empty_cols = set()

for r,line in enumerate(lines):
    if (check_empty_row(r, lines)):
        empty_rows.add(r)

for c in range(len(lines[0])):
    if (check_empty_col(c, lines)):
        empty_cols.add(c)

galaxies = []
for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if (char == "#"): galaxies.append({"r": r, "c": c})

total_dist = 0
total_dist_2 = 0
for i,g in enumerate(galaxies):
    if (i == len(galaxies)-1): break
    for j,g2 in enumerate(galaxies[i+1:]):
        total_dist += get_expanded_dist((g["r"], g["c"]), (g2["r"], g2["c"]), 1, empty_rows, empty_cols)
        total_dist_2 += get_expanded_dist((g["r"], g["c"]), (g2["r"], g2["c"]), 999999, empty_rows, empty_cols)

print(f'Part 1 ans: {total_dist}')
print(f'Part 2 ans: {total_dist_2}')
