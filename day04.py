import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day04.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()


def get_num_winners(nums: str) -> int:
    nums = nums.strip()
    nums = ",".join(nums.split())
    winning_nums_text, your_nums_text = nums.split("|")
    winning_nums = winning_nums_text.split(",")[:-1]
    your_nums = your_nums_text.split(",")[1:]
    count = 0
    for yn in your_nums:
        if yn in winning_nums:
            count += 1
    return count


score = 0
cards = 0
MAX_CARD = len(lines)
points_arr = [1] * MAX_CARD

for line in lines:
    card_num_text, nums = line.split(":")
    count = get_num_winners(nums)
    if count > 0:
        score += 2 ** (count - 1)

for line in reversed(lines):
    card_num_text, nums = line.split(":")
    card_num = int(card_num_text.split(" ")[-1])
    count = get_num_winners(nums)
    pts = 1
    for i in range(count):
        next_card_num = card_num + i + 1
        if next_card_num > MAX_CARD:
            break
        pts += points_arr[next_card_num - 1]
    cards += pts
    points_arr[card_num - 1] = pts

print(f"Part 1 ans: {score}")
print(f"Part 2 ans: {cards}")
