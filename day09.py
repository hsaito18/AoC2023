import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day09.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()


def check_if_zeroes(arr):
    for n in arr:
        if n != 0:
            return False
    return True


def cofactor_expansion_of_a_matrix(arr):
    out = 0
    for i, n in enumerate(arr):
        if i % 2 == 0:
            out -= n
        else:
            out += n
    return out


p1 = 0
p2 = 0
for line in lines:
    nums = line.split(" ")
    done = False
    final_nums = [int(nums[-1])]
    first_first_num = int(nums[0])
    first_nums = []
    prev_diffs = nums
    while not done:
        diffs = []
        for i, n in enumerate(prev_diffs):
            if i == 0:
                continue
            diffs.append(int(n) - int(prev_diffs[i - 1]))
        if check_if_zeroes(diffs):
            done = True
        final_nums.append(diffs[-1])
        first_nums.append(diffs[0])
        prev_diffs = diffs
    p1 += sum(final_nums)
    p2 += first_first_num + cofactor_expansion_of_a_matrix(first_nums)

print(f"Part 1 ans: {p1}")
print(f"Part 2 ans: {p2}")
