import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day07.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

import functools

CARD_RANKING = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

CARD_RANKING_2 = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 1,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


def get_type_hand(hand: str) -> int:
    cts = {}
    for c in hand:
        cts[c] = hand.count(c)
    if len(cts) == 1:
        return 6
    max_count = max(cts.values())
    if len(cts) == 2:
        if max_count == 4:
            return 5
        else:
            return 4
    if len(cts) == 3:
        if max_count == 3:
            return 3
        else:
            return 2
    if len(cts) == 4:
        return 1
    return 0


def get_type_hand_joker(hand: str) -> int:
    jokers = hand.count("J")
    hand = hand.replace("J", "")
    if len(hand) == 0:
        return 6
    cts = {}
    for c in hand:
        cts[c] = hand.count(c)
    if len(cts) == 1:
        return 6
    min_count = min(cts.values())
    max_count = max(cts.values())
    if len(cts) == 2:
        if min_count == 1:
            return 5
        else:
            return 4
    if len(cts) == 3:
        if jokers > 0:
            return 3
        elif max_count == 3:
            return 3
        else:
            return 2
    if len(cts) == 4:
        return 1
    return 0


def compare_card(c1: str, c2: str) -> int:
    if CARD_RANKING[c1] > CARD_RANKING[c2]:
        return 1
    elif CARD_RANKING[c2] > CARD_RANKING[c1]:
        return -1
    else:
        return 0


def compare_card_2(c1: str, c2: str) -> int:
    if CARD_RANKING_2[c1] > CARD_RANKING_2[c2]:
        return 1
    elif CARD_RANKING_2[c2] > CARD_RANKING_2[c1]:
        return -1
    else:
        return 0


def compare_hands(hand1: str, hand2: str) -> int:
    type1 = get_type_hand(hand1)
    type2 = get_type_hand(hand2)
    if type1 > type2:
        return 1
    elif type2 > type1:
        return -1
    else:
        for i in range(5):
            r = compare_card(hand1[i], hand2[i])
            if r != 0:
                return r
    return 0


def compare(line1, line2):
    return compare_hands(line1["hand"], line2["hand"])


def compare_hands_joker(hand1: str, hand2: str) -> int:
    type1 = get_type_hand_joker(hand1)
    type2 = get_type_hand_joker(hand2)
    if type1 > type2:
        return 1
    elif type2 > type1:
        return -1
    else:
        for i in range(5):
            r = compare_card_2(hand1[i], hand2[i])
            if r != 0:
                return r
    return 0


def compare_joker(line1, line2):
    return compare_hands_joker(line1["hand"], line2["hand"])


hands = []

for line in lines:
    hand, bid = line.split(" ")
    hands.append({"hand": hand, "bid": bid})

aa = sorted(hands, key=functools.cmp_to_key(compare))
bb = sorted(hands, key=functools.cmp_to_key(compare_joker))

score = 0
for i, hand in enumerate(aa):
    rank = i + 1
    bid = int(hand["bid"])
    score += rank * bid

score2 = 0
for i, hand in enumerate(bb):
    rank = i + 1
    bid = int(hand["bid"])
    score2 += rank * bid

print(f"Part 1 ans: {score}")
print(f"Part 2 ans: {score2}")
