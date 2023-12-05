import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day5.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

def get_mapped_inputs(lines):
    inputs = []
    min_in = float('inf')
    for line in lines:
        out_start,in_start,range_num = line.split(" ")
        out_start = int(out_start)
        in_start = int(in_start)
        range_num = int(range_num)
        inputs.append({'start': in_start, 'end': in_start+range_num, 'offset': out_start-in_start, 'min_out': out_start, 'max_out': out_start+range_num})
        if (in_start < min_in): min_in = in_start
    if (min_in > 0): inputs.append({'start':0,'end':min_in,'offset':0,'min_out':0,'max_out': min_in})
    return inputs

def get_output(input,map):
    for map_obj in map:
        if (input < map_obj['start']): continue
        if (input >= map_obj['end']): continue
        return map_obj['offset'] + input
    return input

def get_preimage(out_start, out_end, map):
    preimage = []
    for map_obj in map:
        if (out_start >= map_obj['max_out']): continue
        if (out_end < map_obj['min_out']): continue
        min_pre = max(out_start, map_obj['min_out'])
        max_pre = min(out_end, map_obj['max_out'])
        offset = map_obj['offset']
        preimage.append({'start': min_pre-offset, 'end': max_pre-offset, 'in_start': map_obj['start']})
        
    # check if input has any overlap
    extras = [{'start': out_start, 'end': out_end, 'in_start': -1}]
    for map_obj in map:
        for ex in extras:
            new_out_start = -1
            new_out_end = -1
            if (ex['start'] >= map_obj['end']): continue
            if (ex['end'] < map_obj['start']): continue
            if (ex['start'] >= map_obj['start']):
                new_out_start = map_obj['end']
            else:
                new_out_end = map_obj['start']
            if (ex['end'] <= map_obj['end']):
                new_out_end = map_obj['start']
            else:
                new_out_start = map_obj['end']
            if (new_out_start == -1 and new_out_end != -1):
                ex['end'] = new_out_end
            elif (new_out_end == -1 and new_out_start != -1):
                ex['start'] = new_out_start
            elif (ex['start'] >= map_obj['start']): extras.remove(ex)
            else:
                ex['end'] = new_out_end
                extras.append({'start': new_out_start, 'end': ex['end'], 'in_start': -2})
    preimage += extras 
    return preimage

def get_location(seed):
    val = seed
    for i in range(7):
        val = get_output(int(val), maps[i])
    return val

def get_single_overlap(o1,o2):
    if (o1['start'] >= o2['end']): return None
    if (o1['end'] < o2['start']): return None
    return {'start': max(o1['start'], o2['start']), 'end': min(o1['end'], o2['end'])}

def get_overlaps(preimage, valids):
    out_pm = []
    for pm in preimage:
        for v in valids:
            over = get_single_overlap(pm, v)
            if (over is not None):
                out_pm.append(over)
    return out_pm

seeds = lines[0].split(" ")[1:]

label_rows = []
for i,line in enumerate(lines):
    if len(line) == 0: continue
    if line[0].isalpha():
        label_rows.append(i)

seed_to_soil_range = (label_rows[1]+1, label_rows[2]-1)
soil_to_fert_range = (label_rows[2]+1, label_rows[3]-1)
fert_to_water_range = (label_rows[3]+1, label_rows[4]-1)
water_to_light_range = (label_rows[4]+1, label_rows[5]-1)
light_to_temp_range = (label_rows[5]+1, label_rows[6]-1)
temp_to_humid_range = (label_rows[6]+1, label_rows[7]-1)
humid_to_loc_range = (label_rows[7]+1, len(lines))

seed_to_soil_map = get_mapped_inputs(lines[seed_to_soil_range[0]:seed_to_soil_range[1]])
soil_to_fert_map = get_mapped_inputs(lines[soil_to_fert_range[0]:soil_to_fert_range[1]])
fert_to_water_map = get_mapped_inputs(lines[fert_to_water_range[0]:fert_to_water_range[1]])
water_to_light_map = get_mapped_inputs(lines[water_to_light_range[0]:water_to_light_range[1]])
light_to_temp_map = get_mapped_inputs(lines[light_to_temp_range[0]:light_to_temp_range[1]])
temp_to_humid_map = get_mapped_inputs(lines[temp_to_humid_range[0]:temp_to_humid_range[1]])
humid_to_loc_map = get_mapped_inputs(lines[humid_to_loc_range[0]:humid_to_loc_range[1]])

maps = []
maps.append(seed_to_soil_map)
maps.append(soil_to_fert_map)
maps.append(fert_to_water_map)
maps.append(water_to_light_map)
maps.append(light_to_temp_map)
maps.append(temp_to_humid_map)
maps.append(humid_to_loc_map)

lowest_loc = float('inf')
lowest_seed_path = []
for seed in seeds:
    val = seed
    path = [seed]
    for i in range(7):
        val = get_output(int(val), maps[i])
        path.append(val)
    if (int(val) < lowest_loc):
        lowest_loc = val
        lowest_seed = seed
        lowest_seed_path = path

seeds2 = []
for i,seed in enumerate(seeds):
    if (i % 2 != 0): continue
    start_seed = int(seed)
    num_seeds = int(seeds[i+1])
    seeds2.append({'start': start_seed, 'end': start_seed + num_seeds})

MAX_LOCATION = 37965625 # Kept decreasing this number until total_seeds got small enough to brute force. 
humid_preimage = get_preimage(0, MAX_LOCATION, humid_to_loc_map) 
temp_preimage = []
for pre in humid_preimage:
    temp_preimage += get_preimage(pre['start'], pre['end'], temp_to_humid_map)
light_preimage = []
for pre in temp_preimage:
    light_preimage += get_preimage(pre['start'], pre['end'], light_to_temp_map)
water_preimage = []
for pre in light_preimage:
    water_preimage += get_preimage(pre['start'], pre['end'], water_to_light_map)
fert_preimage = []
for pre in water_preimage:
    fert_preimage += get_preimage(pre['start'], pre['end'], fert_to_water_map)
soil_preimage = []
for pre in fert_preimage:
    soil_preimage += get_preimage(pre['start'], pre['end'], soil_to_fert_map)
seed_preimage = []
for pre in soil_preimage:
    seed_preimage += get_preimage(pre['start'], pre['end'], seed_to_soil_map)
possibles = get_overlaps(seed_preimage, seeds2)
total_seeds = 0
for possible in possibles:
    total_seeds += possible['end'] - possible['start']
seeds4 = []
for pre in possibles:
    for i in range(pre['start'], pre['end']):
        seeds4.append(i)
lowest_loc_2 = float('inf')
for a,seed in enumerate(seeds4):
    val = seed
    for i in range(7):
        val = get_output(int(val), maps[i])
    if (int(val) < lowest_loc_2):
        lowest_loc_2 = val

print(f'Part 1 ans: {lowest_loc}')
print(f'Part 2 ans: {lowest_loc_2}')
