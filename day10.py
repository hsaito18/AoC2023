import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day10.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

# pipe_pos - curr_pos are keys
PIPES = {"|": {(1,0): (1,0), (-1,0): (-1,0)}, 
         "-": {(0,1): (0,1), (0,-1): (0,-1)},
         "L": {(1,0): (0,1), (0,-1): (-1,0)},
         "J": {(1,0): (0,-1), (0,1): (-1, 0)},
         "7": {(-1,0): (0,-1), (0,1): (1, 0)},
         "F": {(-1,0): (0, 1), (0,-1): (1,0)}
         }

def add_tuple(t1, t2):
    return tuple([sum(x) for x in zip(t1,t2)])

def sub_tuple(t1, t2):
    return tuple([x[0] - x[1] for x in zip(t1,t2)])

start_pos = (0,0)
for r,line in enumerate(lines):
    if (line.find("S") != -1):
        start_pos = (r, line.find("S"))
        break

next_move = PIPES["F"][(0,-1)]
# next_move = PIPES["|"][(1,0)]
last_pipe_coord = add_tuple(start_pos, (0,-1))
# last_pipe_coord = add_tuple(start_pos, (1,0))
steps = 2
curr_pipe = "F"
while True:
    next_pipe_coord = add_tuple(last_pipe_coord, next_move)
    next_pipe = lines[next_pipe_coord[0]][next_pipe_coord[1]]
    if (next_pipe == "S"): break
    delta_coords = sub_tuple(next_pipe_coord, last_pipe_coord)
    next_move = PIPES[next_pipe][delta_coords]
    last_pipe_coord = next_pipe_coord
    curr_pipe = next_pipe
    steps += 1
  
print(f"Part 1 ans: {steps/2}")