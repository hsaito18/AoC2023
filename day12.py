import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day12.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

import functools

def check_arrangement(arr, groups):
    actual = []
    counting = arr[0] == "#"
    curr_count = 0
    for c in arr:
        if c == "?": return False
        if c == "#":
            curr_count += 1
            if not counting: counting = True
            continue
        if c == "." and counting:
            actual.append(curr_count)
            counting = False
            curr_count = 0
    if counting:
        actual.append(curr_count)
    return groups == actual

def check_possible(arr,groups):
    actual = []
    counting = arr[0] == "#"
    curr_count = 0
    confirmed_first = True
    for c in arr:
        if c == "?": confirmed_first = False
        if c == "#":
            curr_count += 1
            if not counting: counting = True
            continue
        if counting:
            actual.append(curr_count)
            counting = False
            if confirmed_first and curr_count != groups[0]: return False
            curr_count = 0
            confirmed_first = False
    if counting:
        actual.append(curr_count)
    if (len(actual) == 0): return True
    if (max(groups) < max(actual)): return False
    return True

def preoptimize(start, groups):
  next = start
  for i,c in enumerate(start):
    if (c != "?"): continue
    test_1 = next[:i] + "#" + next[i+1:]
    test_2 = next[:i] + "." + next[i+1:]
    if (not check_possible(test_1, groups)):
      next = test_2
    elif (not check_possible(test_2, groups)):
      next = test_1
  start = next
  total_damaged = sum(groups)
  num_damaged_start = start.count("#")
  delta_damaged = total_damaged - num_damaged_start
  if (delta_damaged == 0): return (start, groups)
  curr_line = start
  for i,c in enumerate(start):
    if c != "?": continue
    curr_line = start[:i] + "#" + start[i+1:]
    l_done = i == 0
    l_i = i-1
    r_done = i == len(start)-1 
    r_i = i+1
    curr_size = 0
    while not l_done:
      l_c = curr_line[l_i]
      if (l_c) != "#": break
      curr_size += 1
      if (l_i == 0): break
      l_i -= 1
    while not r_done:
      r_c = curr_line[r_i]
      if (r_c) != "#": break
      curr_size += 1
      if (r_i == len(start) - 1): break
      r_i += 1
    if (curr_size > max(groups)):
      start = start[:i] + "." + start[i+1:]
  islands = start.split(".")
  big = []
  for i,isl in enumerate(islands):
     if len(isl) >= max(groups): big.append(i)
     if len(isl) < min(groups): 
        islands[i] = "." * len(isl)
  if len(big) == 1 and len(islands[big[0]]) == max(groups):
     islands[big[0]] = "#" * max(groups)
  start = ".".join(islands)
  return start,groups

@functools.cache
def recursive_search(start, groups_text):
  if groups_text:
    groups = [ int(x) for x in groups_text.split(",") ]
  else:
    groups = []
  if (len(groups) == 0): 
    if ("#" in start): return 0
    return 1
  first_grouping = groups[0]
  next = []
  for i,c in enumerate(start):
    if i != 0 and start[i-1] == "#": break
    if c == ".": continue
    if i+first_grouping > len(start): break
    if "." in start[i:i+first_grouping]: continue
    if i+first_grouping < len(start) and start[i+first_grouping] == "#": continue
    next.append((start[i+first_grouping+1:], ",".join(str(x) for x in groups[1:]),i))
  out = 0
  for poss in next:
    out += recursive_search(poss[0], poss[1])
  return out

def fold_line(line, folds, groups):
    return (line+"?")*(folds-1) + line + " " + (groups+",")*(folds-1)+groups
  
total_possiblities = 0
start,groups_text = lines[0].split(" ")
possibilities_arr = []
quintupled_lines = []

for line in lines:
  start,groups_text = line.split(" ")
  groups = [ int(x) for x in groups_text.split(",") ]
  possibilities = recursive_search(start, groups_text)
  total_possiblities += possibilities
  possibilities_arr.append(possibilities)
  quintupled_lines.append(fold_line(start,5, groups_text))

quintuple_poss_arr = []
for i,line in enumerate(quintupled_lines):
  print(f"Analyzing {i}/1000...")
  start,groups_text = line.split(" ")
  groups = [ int(x) for x in groups_text.split(",") ]
  possibilities = recursive_search(start,groups_text)
  quintuple_poss_arr.append(possibilities)


print(f'Part 1 ans: {total_possiblities}')
print(f'Part 2 ans: {sum(quintuple_poss_arr)}')
