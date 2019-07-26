global exit
end_keywords = ["exit", "end", "terminate", "over", "stop"]

def run_cli():
    global exit
    exit = False
    while not exit:
        cmd = input("Enter command: ")
        process_cmd(cmd)

def process_cmd(cmd):
    if check_exit(cmd):
        return
    if check_roll(cmd):
        return

def check_exit(cmd):
    global exit
    if cmd.lower() in end_keywords:
        exit = True
        return True

def check_roll(cmd):
    if cmd[:4] == "roll":
        print("6")
        return True

run_cli()
