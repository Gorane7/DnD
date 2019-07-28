import random
import matplotlib.pyplot as plt

global exit
end_keywords = ["exit", "end", "terminate", "over", "stop"]

def run_cli():
    global exit
    exit = False
    while not exit:
        cmd = input("Enter command: ").split(" ")
        process_cmd(cmd)

def process_cmd(cmd):
    if len(cmd) == 1:
        if check_exit(cmd):
            return
    if check_roll(cmd):
        return
    if check_analyze(cmd):
        return

def check_exit(cmd):
    global exit
    if cmd[0].lower() in end_keywords:
        exit = True
        return True

def check_roll(cmd, known = False):
    if cmd[0] == "roll":
        if "low" in cmd[-1]:
            if cmd[-1][:-3].isdigit():
                if known:
                    return roll(cmd[1:-1], adv = "low", adv_amount = int(cmd[-1][:-3]))
                else:
                    print(roll(cmd[1:-1], adv = "low", adv_amount = int(cmd[-1][:-3])))
            else:
                print("Wrong syntax for rolling, correct example would be 'roll 4d6 3d20 2high'")
        elif "high" in cmd[-1]:
            if cmd[-1][:-4].isdigit():
                if known:
                    return roll(cmd[1:-1], adv = "high", adv_amount = int(cmd[-1][:-4]))
                else:
                    print(roll(cmd[1:-1], adv = "high", adv_amount = int(cmd[-1][:-4])))
            else:
                print("Wrong syntax for rolling, correct example would be 'roll 4d6 3d20 2high'")
        else:
            if known:
                return roll(cmd[1:])
            else:
                print(roll(cmd[1:]))
        return True

def check_analyze(cmd):
    if cmd[0] == "analyze" and cmd[1].isdigit():
        values = {}
        for i in range(int(cmd[1])):
            value = check_roll(cmd[2:], known = True)
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
        return True

def roll(dice, adv = None, adv_amount = None):
    numbers = []
    types = []
    rolls = []
    for die in dice:
        if "d" not in die:
            return "Wrong syntax for rolling, correct example would be 'roll 4d6 3d20 2high'"
        if len(die.split("d")) != 2:
            return "Wrong syntax for rolling, correct example would be 'roll 4d6 3d20 2high'"
        temp = die.split("d")
        if not temp[0].isdigit() or not temp[1].isdigit():
            return "Wrong syntax for rolling, correct example would be 'roll 4d6 3d20 2high'"
        numbers.append(int(temp[0]))
        types.append(int(temp[1]))
    for number, type in zip(numbers, types):
        for i in range(number):
            rolls.append(random.randint(1, type))
    rolls.sort()
    if adv_amount:
        if adv_amount > len(rolls):
            return "Argument for high/low can't be larger than the total amount of dice"
        if adv == "low":
            rolls = rolls[:adv_amount]
        if adv == "high":
            rolls = rolls[-adv_amount:]
    return sum(rolls)

run_cli()
