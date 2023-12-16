import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day16.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

def move_light(t, t2, searched_tiles):
    nr = t[0]+t2[0]
    nc = t[1]+t2[1]
    if ((nr,nc,t2) in searched_tiles): return -1
    if nr < 0 or nr >= len(lines): return -1
    if nc < 0 or nc >= len(lines[0]): return -1
    return (t[0]+t2[0], t[1]+t2[1])



FORWARD_MIRROR_MAP = {(1,0): (0,-1), (-1,0): (0,1), (0,1): (-1,0), (0,-1): (1,0)}
BACKWARD_MIRROR_MAP = {(1,0): (0,1), (-1,0): (0,-1), (0,1): (1,0), (0,-1): (-1,0)}
MIRROR_MAP = {"/": FORWARD_MIRROR_MAP, "\\": BACKWARD_MIRROR_MAP}

def get_final_energized(init_pos, init_dir):
    lights = [(init_pos[0],init_pos[1], init_dir)]
    energized_tiles = set()
    energized_tiles.add(init_pos)
    searched_tiles = set()
    for j in range(1000):
      new_lights = lights.copy()
      for i,light in enumerate(lights):
        r,c,d = light
        curr_space = lines[r][c]
        if (curr_space == "-"):
            if (d == (0,1) or d == (0,-1)): curr_space = "."
            else:
                left_coord = move_light((r,c), (0,-1), searched_tiles)
                if (left_coord == -1): new_lights[i] = -1
                else:  
                  new_lights[i] = (left_coord[0], left_coord[1], (0,-1))
                  energized_tiles.add(left_coord)
                  searched_tiles.add((left_coord[0], left_coord[1], (0,-1)))
                right_coord = move_light((r,c), (0,1), searched_tiles)
                if (right_coord != -1):
                  new_lights.append((right_coord[0], right_coord[1], (0,1)))
                  energized_tiles.add(right_coord)
                  searched_tiles.add((right_coord[0], right_coord[1], (0,1)))
                continue
        if (curr_space == "|"):
            if (d == (1,0) or d == (-1,0)): curr_space = "."
            else:
                up_coord = move_light((r,c), (-1,0), searched_tiles)
                if (up_coord == -1): new_lights[i] = -1
                else:
                  new_lights[i] = (up_coord[0], up_coord[1], (-1,0))
                  energized_tiles.add(up_coord)
                  searched_tiles.add((up_coord[0], up_coord[1], (-1,0)))
                down_coord = move_light((r,c), (1,0), searched_tiles)
                if (down_coord != -1):
                  new_lights.append((down_coord[0], down_coord[1], (1,0)))
                  energized_tiles.add(down_coord)
                  searched_tiles.add((down_coord[0], down_coord[1], (1,0)))
                continue  
        if curr_space == ".":
            new_coord = move_light((r,c), d, searched_tiles)
            if new_coord == -1:
              new_lights[i] = -1
              continue
            new_lights[i] = (new_coord[0], new_coord[1], d)
            energized_tiles.add(new_coord)
            searched_tiles.add((new_coord[0], new_coord[1], d))
            continue
        if curr_space == "/" or curr_space == "\\":
            new_direction = MIRROR_MAP[curr_space][d]
            new_coord = move_light((r,c), new_direction, searched_tiles)
            if new_coord == -1:
              new_lights[i] = -1
              continue
            new_lights[i] = (new_coord[0], new_coord[1], new_direction)
            energized_tiles.add(new_coord)
            searched_tiles.add((new_coord[0], new_coord[1],new_direction))
            continue
      lights = list(filter((-1).__ne__, new_lights))
    return len(energized_tiles)

max_energized = 0
for r in range(len(lines)):
  energized_left = get_final_energized((r,0), (0,1))
  energized_right = get_final_energized((r, len(lines[0])-1), (0,-1))
  if (max(energized_right, energized_left) > max_energized):
    max_energized = max(energized_right, energized_left)

for c in range(len(lines[0])):
  energized_top = get_final_energized((0,c), (1,0))
  energized_bot = get_final_energized((len(lines)-1, c), (-1,0))
  if (max(energized_bot, energized_top) > max_energized):
    max_energized = max(energized_bot, energized_top)

print(f"Part 1 ans: {get_final_energized((0,0), (0,1))}")
print(f"Part 2 ans: {max_energized}")
