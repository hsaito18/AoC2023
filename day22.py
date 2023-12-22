import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day22.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

from copy import deepcopy
from collections import deque

blocks_row = {}
for line in lines:
    c1, c2 = line.split("~")
    x1, y1, z1 = c1.split(",")
    x2, y2, z2 = c2.split(",")
    x1, y1, z1 = int(x1), int(y1), int(z1)
    x2, y2, z2 = int(x2), int(y2), int(z2)
    lowest = min(z1, z2)
    if lowest not in blocks_row:
        blocks_row[lowest] = []
    blocks_row[lowest].append(((x1, y1, z1), (x2, y2, z2)))

rows = [key for key in sorted(blocks_row.keys())]
blocks = []


def generate_block_coords(c1, c2):
    cs = []
    x1, y1, z1 = c1
    x2, y2, z2 = c2
    if x1 != x2:
        minx = min(x1, x2)
        maxx = max(x1, x2)
        for x in range(minx, maxx + 1):
            cs.append((x, y1, z1))
    elif y1 != y2:
        miny = min(y1, y2)
        maxy = max(y1, y2)
        for y in range(miny, maxy + 1):
            cs.append((x1, y, z1))
    elif z1 != z2:
        minz = min(z1, z2)
        maxz = max(z1, z2)
        for z in range(minz, maxz + 1):
            cs.append((x1, y1, z))
    else:
        cs.append((x1, y1, z1))
    return cs


num = 0
coord_to_num = {}
all_coords = set()
for z in rows:
    for block in blocks_row[z]:
        reliants = set()
        c1, c2 = block
        x1, y1, z1 = c1
        x2, y2, z2 = c2
        if z2 < z1:
            x2, y2, z2 = c1
            x1, y1, z1 = c2
        lowest = min(z1, z2)
        vertical = z1 != z2
        landed = False
        for nz in range(lowest - 1, 0, -1):
            nc1 = x1, y1, nz
            if vertical:
                nc2 = x2, y2, nz + z2 - z1
            else:
                nc2 = x2, y2, nz
            cs = generate_block_coords(nc1, nc2)
            for c in cs:
                if c not in all_coords:
                    continue
                landed = True
                reliants.add(coord_to_num[c])
            if landed:
                nc1 = x1, y1, nz + 1
                if vertical:
                    nc2 = x2, y2, nz + 1 + z2 - z1
                else:
                    nc2 = x2, y2, nz + 1
                cs_landed = generate_block_coords(nc1, nc2)
                for c in cs_landed:
                    coord_to_num[c] = num
                    all_coords.add(c)
                break
        if not landed:
            nc1 = x1, y1, 1
            if vertical:
                nc2 = x2, y2, 1 + z2 - z1
            else:
                nc2 = x2, y2, 1
            cs_landed = generate_block_coords(nc1, nc2)
            for c in cs_landed:
                coord_to_num[c] = num
                all_coords.add(c)
        blocks.append(
            {
                "num": num,
                "reliants": list(reliants),
                "responsibles": [],
                "coords": cs_landed,
            }
        )
        num += 1

criticals = set()
for block in blocks:
    if len(block["reliants"]) == 1:
        criticals.add(block["reliants"][0])

for i in range(num - 1, -1, -1):
    block = blocks[i]
    for r in block["reliants"]:
        blocks[r]["responsibles"].append(i)


def get_fallen_blocks(block_num, blocks):
    blocks_copy = deepcopy(blocks)
    que = deque()
    que.append(block_num)
    fallen = set()
    count = 0
    while que:
        curr_num = que.popleft()
        if curr_num in fallen:
            continue
        fallen.add(curr_num)
        count += 1
        curr_block = blocks_copy[curr_num]
        for r in curr_block["responsibles"]:
            blocks_copy[r]["reliants"].remove(curr_num)
            if len(blocks_copy[r]["reliants"]) == 0:
                que.append(r)
    return count


tot = 0
for block in blocks:
    tot += (get_fallen_blocks(block["num"], blocks)) - 1

print(f"Part 1 ans: {len(blocks) - len(criticals)}")
print(f"Part 2 ans: {tot}")
