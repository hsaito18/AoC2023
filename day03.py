import os

path = os.getcwd()
with open(os.path.join(path, "inputs", "day03.txt")) as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    lines[i] = line.strip()

SYMBOLS = "!@#$%^&*()_-+={}[]/\|:;"


def get_full_number(row, col):
    left_done = True if col == 0 else False
    left_col = col
    while not left_done:
        left_col = left_col - 1
        if not lines[row][left_col].isnumeric():
            left_done = True
            left_col += 1
        if left_col == 0:
            left_done = True
    right_done = True if col == dim - 1 else False
    right_col = col
    while not right_done:
        right_col = right_col + 1
        if not lines[row][right_col].isnumeric():
            right_done = True
            right_col -= 1
        if right_col == dim - 1:
            right_done = True
    return int(lines[row][left_col : right_col + 1]), left_col, right_col


def check_symbol(row, col):
    s = 0
    for r in range(row - 1, row + 2):
        if r < 0 or r >= dim:
            continue
        for c in range(col - 1, col + 2):
            if c < 0 or c >= dim:
                continue
            if r == row and c == col:
                continue
            if not lines[r][c].isnumeric():
                continue
            if counted_numbers[r][c]:
                continue
            (num, left, right) = get_full_number(r, c)
            # hasn't been counted yet.
            for num_col in range(left, right + 1):
                counted_numbers[r][num_col] = True
            s += num
    return s


def check_star(row, col):
    star_counted_numbers = []
    for _ in range(3):
        star_counted_numbers.append([False] * 3)
    # -1 -1 => 0 0
    gr1 = 0
    gr2 = 0
    for r in range(row - 1, row + 2):
        if r < 0 or r >= dim:
            continue
        for c in range(col - 1, col + 2):
            if c < 0 or c >= dim:
                continue
            if r == row and c == col:
                continue
            if not lines[r][c].isnumeric():
                continue
            if star_counted_numbers[r - row + 1][c - col + 1]:
                continue
            (num, left, right) = get_full_number(r, c)
            for num_col in range(left - col + 1, right - col + 2):
                if num_col < 0 or num_col >= 3:
                    continue
                star_counted_numbers[r - row + 1][num_col] = True
            if gr2 != 0:
                return 0
            if gr1 != 0:
                gr2 = num
            else:
                gr1 = num
    return gr1 * gr2


counted_numbers = []
dim = len(lines[0])
for i in range(dim):
    counted_numbers.append([False] * dim)

sum = 0
gear_sum = 0

for row, line in enumerate(lines):
    for col, c in enumerate(line):
        if c in SYMBOLS:
            sum += check_symbol(row, col)
            if c == "*":
                gear_sum += check_star(row, col)

print(f"Part 1 ans: {sum}")
print(f"Part 2 ans: {gear_sum}")
