import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day13.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()


def get_col(column, pattern):
    out = []
    for row in pattern:
        out.append(row[column])
    return out

patterns = []
curr_pattern = []
for line in lines:
    if len(line) == 0:
        patterns.append(curr_pattern)
        curr_pattern = []
    else:
        curr_pattern.append(line)
patterns.append(curr_pattern)

num_horiz = 0
num_vert = 0

num_horiz_2 = 0
num_vert_2 = 0

for pattern in patterns:
    for r,row in enumerate(pattern):
        if (r == len(pattern) - 1): continue
        mirror = True
        r_top = r
        r_bot = r+1
        while (r_top >= 0 and r_bot < len(pattern)):
            top_line = pattern[r_top]
            bot_line = pattern[r_bot]
            r_top -= 1
            r_bot += 1
            if (top_line != bot_line):
                mirror = False
                break
        if (mirror): num_horiz += 1+r
    for c in range(len(pattern[0])):
        if (c == len(pattern[0]) - 1): continue
        mirror_vert = True
        c_left = c
        c_right = c+1
        while (c_left >= 0 and c_right < len(pattern[0])):
            left_line = get_col(c_left, pattern)
            right_line = get_col(c_right, pattern)
            c_left -= 1
            c_right += 1
            if (left_line != right_line):
                mirror_vert = False
                break
        if (mirror_vert): num_vert += 1+c
    
    # Part 2:
    r_diffs = []
    for r,row in enumerate(pattern):
        if (r == len(pattern) - 1): continue
        r_top = r
        r_bot = r+1
        line_diff = 0
        while (r_top >= 0 and r_bot < len(pattern)):
            top_line = pattern[r_top]
            bot_line = pattern[r_bot]
            r_top -= 1
            r_bot += 1
            line_diff += sum(1 for i, j in zip(top_line, bot_line) if i != j)
        r_diffs.append(line_diff)
    for i,d in enumerate(r_diffs):
        if d == 1:
            num_horiz_2 += 1+i
    c_diffs = []
    for c in range(len(pattern[0])):
        if (c == len(pattern[0]) - 1): continue
        c_left = c
        c_right = c+1
        line_diff = 0
        while (c_left >= 0 and c_right < len(pattern[0])):
            left_line = get_col(c_left, pattern)
            right_line = get_col(c_right, pattern)
            c_left -= 1
            c_right += 1
            line_diff += sum(1 for i, j in zip(left_line, right_line) if i != j)
        c_diffs.append(line_diff)
    for i,d in enumerate(c_diffs):
        if d == 1:
            num_vert_2 += 1+i

print(f"Part 1 ans: {num_vert + num_horiz*100}")
print(f"Part 2 ans: {num_vert_2 + num_horiz_2*100}")