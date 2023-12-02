import os

path = os.getcwd()
with open(os.path.join(path, "inputs\\day1.txt")) as f:
    lines = f.readlines()

sum = 0
for line in lines:
    first_digit = 0
    last_digit = 0
    for c in line:
        if c.isnumeric():
            first_digit = c
            break
    for c in reversed(line):
        if c.isnumeric():
            last_digit = c
            break
    num = int(first_digit + last_digit)
    sum += num
print(f"Part 1 ans: {sum}")

sum = 0
for line in lines:
    first_digit = ""
    last_digit = ""
    for i, c in enumerate(line):
        if c.isnumeric():
            first_digit = c
            break
        if i >= len(line) - 2:
            continue
        next_three = line[i : i + 3]
        if next_three == "one":
            first_digit = "1"
            break
        if next_three == "two":
            first_digit = "2"
            break
        if next_three == "six":
            first_digit = "6"
            break
        if i >= len(line) - 3:
            continue
        next_four = line[i : i + 4]
        if next_four == "four":
            first_digit = "4"
            break
        if next_four == "five":
            first_digit = "5"
            break
        if next_four == "nine":
            first_digit = "9"
            break
        if i >= len(line) - 4:
            continue
        next_five = line[i : i + 5]
        if next_five == "three":
            first_digit = "3"
            break
        if next_five == "seven":
            first_digit = "7"
            break
        if next_five == "eight":
            first_digit = "8"
            break

    reverse = "".join(reversed(line))
    for i, c in enumerate(reverse):
        if c.isnumeric():
            last_digit = c
            break
        if i >= len(reverse) - 2:
            continue
        next_three = reverse[i : i + 3]
        if next_three == "eno":
            last_digit = "1"
            break
        if next_three == "owt":
            last_digit = "2"
            break
        if next_three == "xis":
            last_digit = "6"
            break
        if i >= len(reverse) - 3:
            continue
        next_four = reverse[i : i + 4]
        if next_four == "ruof":
            last_digit = "4"
            break
        if next_four == "evif":
            last_digit = "5"
            break
        if next_four == "enin":
            last_digit = "9"
            break
        if i >= len(reverse) - 4:
            continue
        next_five = reverse[i : i + 5]
        if next_five == "eerht":
            last_digit = "3"
            break
        if next_five == "neves":
            last_digit = "7"
            break
        if next_five == "thgie":
            last_digit = "8"
            break
    num = int(first_digit + last_digit)
    sum += num

print(f"Part 2 ans: {sum}")
