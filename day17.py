import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day17.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

from functools import cache
from math import copysign

states = {(0,0,(0,0)): 0}
visited = set()
unvisited = set()
goal = len(lines[0])-1
DIRECTIONS = [(1,0), (0,1), (-1,0), (0,-1)]

def get_opp_dir(d):
    return (d[0]*-1, d[1]*-1)

def get_dir(n1,n2):
    r = n1-n2
    if r != 0:
        r = int(copysign(1,r))
    return r

def heuristic(node):
    # return (goal-node[0] + goal-node[1])*5
    return 0

def min_heat(node):
    return goal-node[0] + goal-node[1]
# (row, column, dir_row, dir_col, how many straights has it gone already)
def get_min_heat_loss(r,c, dir):
    if (r,c) == (goal,goal): return states[(r,c,dir)]
    # print(f'exploring: {r}, {c}, {dir_r}, {dir_c}, {straights}')
    # print(r,c,dir_r,dir_c,straights,steps)
    curr_heat = states[(r,c,dir)]
    # if (steps > 9000): return float('inf')
    for direction in (DIRECTIONS):
        if dir == direction or direction == get_opp_dir(dir): continue
        cum_heat = 0
        for dist in range(1,max_dist+1):
            nr = r + direction[0]*dist
            nc = c + direction[1]*dist
            if (nr < 0 or nr >= len(lines) or nc < 0 or nc >= len(lines[0])): break
            cum_heat += int(lines[nr][nc])
            if (dist < min_dist): continue
            next_heat = curr_heat + cum_heat
            # print(states.get((nr,nc,direction),float('inf')))
            if (next_heat > states.get((nr,nc,direction),float('inf'))): continue
            states[(nr,nc,direction)] = next_heat
            # print((nr,nc,direction), next_heat)
            if (nr,nc,direction) not in visited:
                unvisited.add((nr,nc,direction))
    visited.add((r,c,dir))
    if ((r,c,dir) in unvisited): unvisited.remove((r,c,dir))
    min_heat = float('inf')
    next_node = -1
    # print(len(unvisited))
    for node in unvisited:
        node_heat = states[node]
        if (node_heat < min_heat):
            min_heat = node_heat
            next_node = node
    return next_node

max_dist = 3
min_dist = 0
explore_next = get_min_heat_loss(0,0,(0,0))
while not isinstance(explore_next, int):
    explore_next  = get_min_heat_loss(explore_next[0], explore_next[1], explore_next[2])
    
print(f'Part 1 ans: {explore_next}')

min_dist = 4
max_dist = 10
states = {(0,0,(0,0)): 0}
visited = set()
unvisited = set()
explore_next = get_min_heat_loss(0,0,(0,0))
while not isinstance(explore_next, int):
    explore_next  = get_min_heat_loss(explore_next[0], explore_next[1], explore_next[2])
    

print(f'Part 2 ans: {explore_next}')
