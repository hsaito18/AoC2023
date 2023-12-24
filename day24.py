import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day24.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()


def path_intersection(h1, h2):
    if h1["vx"] == h2["vx"] and h1["vy"] == h2["vy"]:
        return None
    h1_m = h1["vy"] / h1["vx"]
    h2_m = h2["vy"] / h2["vx"]
    if h1_m == h2_m:
        return None
    h1_b = h1["y"] - h1_m * h1["x"]
    h2_b = h2["y"] - h2_m * h2["x"]
    x_intersection = (h2_b - h1_b) / (h1_m - h2_m)
    y_intersection = h1_m * x_intersection + h1_b
    x1_intersection_time = (x_intersection - h1["x"]) / h1["vx"]
    y1_intersection_time = (y_intersection - h1["y"]) / h1["vy"]
    x2_intersection_time = (x_intersection - h2["x"]) / h2["vx"]
    y2_intersection_time = (y_intersection - h2["y"]) / h2["vy"]
    if (
        x1_intersection_time < 0
        or y1_intersection_time < 0
        or x2_intersection_time < 0
        or y2_intersection_time < 0
    ):
        return None
    return (x_intersection, y_intersection)


hails = []
for line in lines:
    pos, vel = line.split("@")
    x, y, z = pos.split(",")
    vx, vy, vz = vel.split(",")
    x, y, z = int(x), int(y), int(z)
    vx, vy, vz = int(vx), int(vy), int(vz)
    hails.append({"x": x, "y": y, "z": z, "vx": vx, "vy": vy, "vz": vz})

count = 0
XY_MIN = 200000000000000
XY_MAX = 400000000000000
for i, hail in enumerate(hails):
    for j in range(i + 1, len(hails)):
        hail2 = hails[j]
        intersect = path_intersection(hail, hail2)
        if intersect is None:
            continue
        if (
            intersect[0] >= XY_MIN
            and intersect[0] <= XY_MAX
            and intersect[1] >= XY_MIN
            and intersect[1] <= XY_MAX
        ):
            count += 1

import z3

# Unknowns:
x = z3.Real("x")
y = z3.Real("y")
z = z3.Real("z")

vx = z3.Real("vx")
vy = z3.Real("vy")
vz = z3.Real("vz")

t1 = z3.Real("t1")
t2 = z3.Real("t2")
t3 = z3.Real("t3")

# Knowns:
h1 = hails[0]
h2 = hails[1]
h3 = hails[2]

x1 = h1["x"]
y1 = h1["y"]
z1 = h1["z"]
vx1 = h1["vx"]
vy1 = h1["vy"]
vz1 = h1["vz"]

x2 = h2["x"]
y2 = h2["y"]
z2 = h2["z"]
vx2 = h2["vx"]
vy2 = h2["vy"]
vz2 = h2["vz"]

x3 = h3["x"]
y3 = h3["y"]
z3_xd = h3["z"]
vx3 = h3["vx"]
vy3 = h3["vy"]
vz3 = h3["vz"]

s = z3.Solver()

s.add(vx1 * t1 + x1 == vx * t1 + x)
s.add(vy1 * t1 + y1 == vy * t1 + y)
s.add(vz1 * t1 + z1 == vz * t1 + z)

s.add(vx2 * t2 + x2 == vx * t2 + x)
s.add(vy2 * t2 + y2 == vy * t2 + y)
s.add(vz2 * t2 + z2 == vz * t2 + z)

s.add(vx3 * t3 + x3 == vx * t3 + x)
s.add(vy3 * t3 + y3 == vy * t3 + y)
s.add(vz3 * t3 + z3_xd == vz * t3 + z)

s.check()
m = s.model()

x_ans = m[x].as_long()
y_ans = m[y].as_long()
z_ans = m[z].as_long()

p2 = x_ans + y_ans + z_ans

print(f"Part 1 ans: {count}")
print(f"Part 2 ans: {p2}")
