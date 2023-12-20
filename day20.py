import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day20.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

from collections import deque

modules = {}
for line in lines:
    line = line.replace(" ", "")
    name, dist = line.split("->")
    if name[0] == "%":
        modules[name[1:]] = {
            "name": name[1:],
            "dist": dist.split(","),
            "type": "flip",
            "state": 0,
        }
    elif name[0] == "&":
        modules[name[1:]] = {
            "name": name[1:],
            "dist": dist.split(","),
            "type": "conj",
            "state": {},
        }
    else:
        modules["broadcaster"] = {"dist": dist.split(","), "type": "broad"}

for key in modules:
    module = modules[key]
    for dist in module["dist"]:
        if dist not in modules:
            continue
        if modules[dist]["type"] == "conj":
            modules[dist]["state"][key] = 0

queue = deque()


def flip_handle(signal, module):
    if signal == 1:
        return
    if module["state"] == 0:
        module["state"] = 1
        for dist in module["dist"]:
            queue.append((dist, 1, module["name"]))
    else:
        module["state"] = 0
        for dist in module["dist"]:
            queue.append((dist, 0, module["name"]))


def conj_handle(signal, module, sender):
    memory = module["state"]
    memory[sender] = signal
    for key in memory:
        if memory[key] == 0:
            for dist in module["dist"]:
                queue.append((dist, 1, module["name"]))
            return
    for dist in module["dist"]:
        queue.append((dist, 0, module["name"]))


def push_button(i):
    l_count = 1
    h_count = 0
    for module in modules["broadcaster"]["dist"]:
        queue.append((module, 0, "broadcaster"))
    while queue:
        for m in modules["zp"]["state"]:
            if modules["zp"]["state"][m] == 1:
                print(modules["zp"]["state"], i)

        module_name, signal, sender = queue.popleft()
        # print(module_name, signal, sender)
        if signal:
            h_count += 1
        else:
            l_count += 1
        if module_name not in modules:
            continue
        module = modules[module_name]
        if module["type"] == "flip":
            flip_handle(signal, module)
        elif module["type"] == "conj":
            conj_handle(signal, module, sender)
    # print(l_count, h_count)
    return (l_count, h_count)


total_l = 0
total_r = 0
for i in range(1000):  # 10000 for part 2
    l, r = push_button(i)
    total_l += l
    total_r += r

# sb: 3797, 3796
# nd: 3917, 3916
# ds: 3733, 3732
# hf:  3877, 3876
from math import lcm

print(f"Part 1 ans: {total_l * total_r}")
print(f"Part 2 ans: {lcm(3797, 3917, 3733, 3877)}")
