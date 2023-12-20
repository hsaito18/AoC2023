import os

# Load input file:
path = os.getcwd()
with open(os.path.join(path, "inputs", "day19.txt")) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

workflows = {}
parts = []
wf = True
parent_workflow = {}


def get_opp_rule(rule):
    if ">" in rule:
        prop, rest = rule.split(">")
        num_text, out = rest.split(":")
        opp_num = int(num_text) + 1
        return f"{prop}<{opp_num}:{out}"
    if "<" in rule:
        prop, rest = rule.split("<")
        num_text, out = rest.split(":")
        opp_num = int(num_text) - 1
        return f"{prop}>{opp_num}:{out}"
    return ""


for line in lines:
    if line == "":
        wf = False
        continue
    if wf:
        name, rest = line.split("{")
        rules = rest[:-1].split(",")
        workflows[name] = {"rules": rules}
        for i, rule in enumerate(rules):
            if ":" in rule:
                child_wf = rule.split(":")[1]
                prev_rules = rules[:i]
                curr_rules = []
                for prev in prev_rules:
                    curr = get_opp_rule(prev)
                    curr_rules.append(curr)
                curr_rules.append(rule)
                parent_workflow[child_wf] = {"name": name, "rules": curr_rules}
            elif rule != "A" and rule != "R":
                child_wf = rule
                prev_rules = rules[:i]
                curr_rules = []
                for prev in prev_rules:
                    curr = get_opp_rule(prev)
                    curr_rules.append(curr)
                parent_workflow[child_wf] = {"name": name, "rules": curr_rules}
    else:
        x, m, a, s = line.split(",")
        parts.append(
            {"x": int(x[3:]), "m": int(m[2:]), "a": int(a[2:]), "s": int(s[2:-1])}
        )
total = 0
for part in parts:
    work_name = "in"
    while work_name != "A" and work_name != "R":
        workflow = workflows[work_name]
        for rule in workflow["rules"]:
            if "<" in rule:
                prop, rest = rule.split("<")
                num_text, out = rest.split(":")
                if part[prop] < int(num_text):
                    work_name = out
                    break
                continue
            if ">" in rule:
                prop, rest = rule.split(">")
                num_text, out = rest.split(":")
                if part[prop] > int(num_text):
                    work_name = out
                    break
                continue
            work_name = rule
            break
    if work_name == "A":
        total += part["x"] + part["m"] + part["a"] + part["s"]


def add_rules(rules, curr_path):
    for rule in rules:
        if "<" in rule:
            prop, rest = rule.split("<")
            num = int(rest.split(":")[0])
            if curr_path[prop][1] > num:
                curr_path[prop] = (curr_path[prop][0], num)
                continue
        if ">" in rule:
            prop, rest = rule.split(">")
            num = int(rest.split(":")[0]) + 1
            if curr_path[prop][0] < num:
                curr_path[prop] = (num, curr_path[prop][1])
                continue


def generate_path(rules, i, workflow):
    path = {"x": (1, 4001), "m": (1, 4001), "a": (1, 4001), "s": (1, 4001)}
    if i == len(rules) - 1:
        next_rules = rules[:-1]
        opp_rules = []
        for next in next_rules:
            opp_rules.append(get_opp_rule(next))
        add_rules(opp_rules, path)
        parent_wf = parent_workflow[workflow]
        parent_name = parent_wf["name"]
        while True:
            add_rules(parent_wf["rules"], path)
            if parent_name == "in":
                return path
            parent_wf = parent_workflow[parent_name]
            parent_name = parent_wf["name"]

    else:
        curr_rule = rules[i]
        next_rules = rules[:i]
        opp_rules = []
        opp_rules.append(curr_rule)
        for next in next_rules:
            opp_rules.append(get_opp_rule(next))
        add_rules(opp_rules, path)
        parent_wf = parent_workflow[workflow]
        parent_name = parent_wf["name"]
        while True:
            add_rules(parent_wf["rules"], path)
            if parent_name == "in":
                return path
            parent_wf = parent_workflow[parent_name]
            parent_name = parent_wf["name"]


a = {}
pathways = []
for workflow in workflows:
    rules = workflows[workflow]["rules"]
    for i, rule in enumerate(rules):
        if rule == "A" or "A" in rule:
            path = generate_path(rules, i, workflow)
            pathways.append(path)

combinations = 0
for p in pathways:
    x_range = p["x"][1] - p["x"][0]
    a_range = p["a"][1] - p["a"][0]
    m_range = p["m"][1] - p["m"][0]
    s_range = p["s"][1] - p["s"][0]
    combinations += x_range * a_range * m_range * s_range

print(f"Part 1 ans: {total}")
print(f"Part 2 ans: {combinations}")
