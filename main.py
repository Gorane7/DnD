import random
import matplotlib.pyplot as plt
from gorgame import game

global cli_running
end_keywords = ["exit", "end", "terminate", "over", "stop"]

def run_cli():
    global cli_running
    cli_running = True
    while cli_running:
        cmd = input("Enter command: ").split(" ")
        process_cmd(cmd)

def process_cmd(cmd):
    if len(cmd) == 1:
        if check_exit(cmd):
            exit()
            return
    if check_roll(cmd):
        print(roll(cmd))
        return
    if check_analyze(cmd):
        analyze(cmd)
        return

def check_exit(cmd):
    if cmd[0].lower() in end_keywords:
        return True

def exit():
    global cli_running
    cli_running = False

def roll(cmd):
    roll_type = check_roll_type(cmd)
    if roll_type == "high":
        return special_roll(cmd[1:], "high")
    elif roll_type == "low":
        return special_roll(cmd[1:], "low")
    elif roll_type == "normal":
        return simple_roll(cmd[1:])

def check_roll(cmd):
    if cmd[0] == "roll":
        is_valid = True
        for word in cmd[1:]:
            word_valid = False
            temp_word = word.split("d")

            if len(temp_word) == 2:
                if temp_word[0].isdigit() and temp_word[1].isdigit():
                    word_valid = True

            if word.split("high")[0].isdigit() and word.split("high")[0] + "high" == word:
                word_valid = True
            if word.split("low")[0].isdigit() and word.split("low")[0] + "low" == word:
                word_valid = True

            if not word_valid:
                is_valid = False
        if not is_valid:
            print("Wrong syntax for rolling, correct example would be 'roll 4d6 3d20 2high'")
            return False
        return True
    return False

def check_roll_type(cmd):
    if "high" in cmd[-1] or "low" in cmd[-1]:
        if "high" in cmd[-1]:
            type = "high"
        if "low" in cmd[-1]:
            type = "low"

        total = 0
        for word in cmd[1:-1]:
            total += int(word.split("d")[0])
        chosen = int(cmd[-1].split(type)[0])
        if chosen > total:
            print("The amount chosen with '" + type + "' can't be larger than the amount of dice rolled.")
            return False
        return type
    return "normal"

def analyze(cmd):
    values = {}
    for i in range(int(cmd[1])):
        value = sum(roll(cmd[2:]))
        if str(value) in values:
            values[str(value)] += 1
        else:
            values[str(value)] = 0

    temp_values = []
    total = 0
    for value, amount in values.items():
        total += int(value) * amount
        temp_values.append([int(value), amount])
    temp_values = sorted(temp_values, key = lambda x: x[0])
    avg = total / int(cmd[1])

    ordered_values = [[], []]
    for value_pair in temp_values:
        ordered_values[0].append(value_pair[0])
        ordered_values[1].append(value_pair[1])

    print(avg)
    plt.bar(ordered_values[0], ordered_values[1])
    plt.show()

def check_analyze(cmd):
    if cmd[0] == "analyze" and cmd[1].isdigit():
        if check_roll(cmd[2:]):
            return True
    return False

def simple_roll(dice):
    numbers = []
    types = []
    rolls = []
    for die in dice:
        temp = die.split("d")
        numbers.append(int(temp[0]))
        types.append(int(temp[1]))
    for number, type in zip(numbers, types):
        for i in range(number):
            rolls.append(random.randint(1, type))
    return rolls

def special_roll(dice, type):
    chosen = int(dice[-1].split(type)[0])
    rolls = simple_roll(dice[:-1])
    if type == "high":
        rolls = sorted(rolls, reverse = True)
    else:
        rolls = sorted(rolls)
    rolls = rolls[:chosen]
    random.shuffle(rolls)
    return rolls

run_cli()
