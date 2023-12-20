import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day15.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()


def hash_algo(s):
    val = 0
    for c in s:
        val += ord(c)
        val *= 17
        val = val % 256
    return val


steps = lines[0].split(",")
p1 = 0
for step in steps:
    p1 += hash_algo(step)

p2 = 0
boxes = [{"labels": [], "focal": []} for _ in range(256)]
for step in steps:
    if ("-") in step:
        label = step[:-1]
        box = hash_algo(label)
        if label not in boxes[box]["labels"]:
            continue
        idx = boxes[box]["labels"].index(label)
        boxes[box]["labels"].pop(idx)
        boxes[box]["focal"].pop(idx)
        continue
    label, focal_length = step.split("=")
    box = hash_algo(label)
    if label in boxes[box]["labels"]:
        idx = boxes[box]["labels"].index(label)
        boxes[box]["focal"][idx] = focal_length
        continue
    boxes[box]["labels"].append(label)
    boxes[box]["focal"].append(focal_length)

total_focusing_power = 0
for i, box in enumerate(boxes):
    for j, focal in enumerate(box["focal"]):
        total_focusing_power += (1 + i) * (1 + j) * int(focal)

print(f"Part 1 ans: {p1}")
print(f"Part 2 ans: {total_focusing_power}")
