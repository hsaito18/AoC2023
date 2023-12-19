import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day18.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

DIRECTION = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
DIRECTION_2 = {"0": (0, 1), "1": (1, 0), "2": (0, -1), "3": (-1, 0)}

dug_tiles = set()
point = (0, 0)
dug_tiles.add(point)

vertices = []

num_tiles_2 = 0
point_2 = (0, 0)


vertices_2 = []

for line in lines:
    dir_char, num_text, color = line.split(" ")
    direction = DIRECTION[dir_char]
    num = int(num_text)
    for i in range(num):
        r = point[0] + direction[0]
        c = point[1] + direction[1]
        point = (r, c)
        dug_tiles.add(point)
    vertices.append(point)

    dist_text = color[2:-2]
    dir_text = color[-2]
    direction = DIRECTION_2[dir_text]
    num_2 = int(dist_text, 16)
    point_2 = (point_2[0] + direction[0] * num_2, point_2[1] + direction[1] * num_2)
    num_tiles_2 += num_2
    vertices_2.append(point_2)
vertices.append(vertices[0])
vertices_2.append(vertices_2[0])

sum_down = 0
sum_up = 0
for i, v in enumerate(vertices):
    if i != len(vertices) - 1:
        sum_down += v[0] * vertices[i + 1][1]
    if i != 0:
        sum_up += v[0] * vertices[i - 1][1]
a = (sum_up - sum_down) / 2 + 0.5 * len(dug_tiles) + 1

sum_down_2 = 0
sum_up_2 = 0
for i, v in enumerate(vertices_2):
    if i != len(vertices_2) - 1:
        sum_down_2 += v[0] * vertices_2[i + 1][1]
    if i != 0:
        sum_up_2 += v[0] * vertices_2[i - 1][1]
b = (sum_up_2 - sum_down_2) / 2 + 0.5 * num_tiles_2 + 1

print(f"Part 1 ans: {int(a)}")
print(f"Part 2 ans: {int(b)}")
