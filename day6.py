import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day6.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

import re

times_line = re.sub(" +", " ", lines[0])
times_line = times_line.split(" ")

distance_line = re.sub(" +", " ", lines[1])
distances = distance_line.split(" ")


def get_dist(ct: int, time: int) -> int:
    return ct * (time - ct)


p1 = 1

for i in range(1, len(distances)):
    goal = int(distances[i])
    time = int(times_line[i])
    winning_nums = 0
    for ct in range(1, time):
        dist = ct * (time - ct)
        if dist > goal:
            winning_nums += 1
        elif winning_nums > 0:
            break
    p1 *= winning_nums

time_p2 = int(lines[0].replace(" ", "")[5:])
dist_p2 = int(lines[1].replace(" ", "")[9:])

p2 = 0
for ct in range(1, time_p2):
    dist = ct * (time_p2 - ct)
    if dist > dist_p2:
        p2 += 1
    elif p2 > 0:
        break

print(f"Part 1 ans: {p1}")
print(f"Part 2 ans: {p2}")
