import os

path = os.getcwd()
with open(os.path.join(path, "inputs", "day02.txt")) as f:
    lines = f.readlines()


def check_game_validity(sets, limits):
    for set in sets:
        colors = set.split(",")
        for color_text in colors:
            [num, color] = color_text.strip().split(" ")
            if int(num) > limits[color]:
                return False
    return True


def calculate_game_mins(sets):
    maxs = {"red": 0, "green": 0, "blue": 0}
    for set in sets:
        colors = set.split(",")
        for color_text in colors:
            [num, color] = color_text.strip().split(" ")
            if int(num) > maxs[color]:
                maxs[color] = int(num)
    return (maxs["red"], maxs["green"], maxs["blue"])


def calculate_game_power(sets):
    [r, g, b] = calculate_game_mins(sets)
    return r * g * b


limits = {"red": 12, "green": 13, "blue": 14}

id_sum = 0
power_sum = 0
for line in lines:
    [game_id, rest] = line.split(":")
    id = int(game_id.split(" ")[1])
    sets = rest.split(";")
    if check_game_validity(sets, limits):
        id_sum += id
    power_sum += calculate_game_power(sets)

print(f"Part 1 ans: {id_sum}")
print(f"Part 2 ans: {power_sum}")
