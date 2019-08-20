from gorgame import game
import os

#CONSTANTS
global my_game
display = game.basics.Coords([1100, 600])
top_bar = game.basics.Coords([display.x, 100])
middle_bar = game.basics.Coords([200, display.y + top_bar.y])
button = game.basics.Coords([middle_bar.x, 100])
size = (display.x * 2 + middle_bar.x, display.y + top_bar.y)
display_order = ["DM", "party", None, "party"]
#display_order = ["party", "DM", "party", None]
current_map = None
agent_on_queue = None
wall_on_queue = None
creature_radius = 2.5
vision_radius = 300
wall_thickness = 1
wall_colour = "brown"


def main():
    setup()
    while True:
        my_game.loop()
        my_loop()

def my_loop():
    check_new_map_button()
    check_new_map_inputs()
    check_save_map_button()
    check_load_map_button()
    check_load_map_inputs()
    check_add_agent_button()
    check_add_agent_inputs()
    check_agent_on_queue()
    check_add_wall_button()
    check_wall_on_queue()

def setup():
    global my_game
    my_game = game.Game(size)
    my_game.screen.window.add_component([0, 0], top_bar, display_order[0] + " bar", background = "red", window = True)
    my_game.screen.window.add_component([0, top_bar.y], display, display_order[0] + " grid", background = "grey", gridview = True)
    my_game.screen.window.add_component([0, top_bar.y], display, display_order[0] + " space", height = 2, spaceview = True, faction = display_order[2])
    my_game.screen.window.add_component([display.x, 0], middle_bar, "middle bar", background = "blue", window = True)
    my_game.screen.window.add_component([display.x + middle_bar.x, 0], top_bar, display_order[1] + " bar", background = "red", window = True)
    my_game.screen.window.add_component([display.x + middle_bar.x, top_bar.y], display, display_order[1] + " grid", background = "grey", gridview = True)
    my_game.screen.window.add_component([display.x + middle_bar.x, top_bar.y], display, display_order[1] + " space", height = 2, spaceview = True, faction = display_order[3])

    my_game.screen.window.get("middle bar").add_component([0, 0], button, "new map button", background = "green", button = True, text = "New map")
    my_game.screen.window.get("middle bar").add_component([0, button.y], button, "save map button", background = "green", button = True, text = "Save map")
    my_game.screen.window.get("middle bar").add_component([0, button.y * 2], button, "load map button", background = "green", button = True, text = "Load map")

    my_game.screen.window.get("DM bar").add_component([0, 0], button, "add agent button", background = "green", button = True, text = "Add agent")
    my_game.screen.window.get("DM bar").add_component([button.x, 0], button, "add wall button", background = "green", button = True, text = "Add wall")

def check_new_map_button():
    if my_game.screen.window.get("middle bar").get("new map button").pressed:
        make_new_map_inputs()

def check_save_map_button():
    if my_game.screen.window.get("middle bar").get("save map button").pressed:
        save_map()

def check_load_map_button():
    if my_game.screen.window.get("middle bar").get("load map button").pressed:
        make_load_map_inputs()

def check_add_agent_button():
    if my_game.screen.window.get("DM bar").get("add agent button").pressed:
        make_add_agent_inputs()

def check_add_wall_button():
    if my_game.screen.window.get("DM bar").get("add wall button").pressed:
        add_wall_to_queue()

def save_map():
    if not current_map:
        return
    x = len(my_game.maps[current_map + " map"].tiles)
    y = len(my_game.maps[current_map + " map"].tiles[0])
    tile = int(my_game.spaces[current_map + " space"].size.x / x)
    file = open("maps/" + current_map + ".txt", "w+")
    file.write(str(x) + "\n")
    file.write(str(y) + "\n")
    file.write(str(tile) + "\n")
    file.write(str(len(my_game.spaces[current_map + " space"].agents)) + "\n")
    file.write(str(len(my_game.spaces[current_map + " space"].walls)) + "\n")
    for agent in my_game.spaces[current_map + " space"].agents:
        x = str(agent.loc.x)
        y = str(agent.loc.y)
        faction = agent.faction
        colour = agent.colour
        file.write(":".join([x, y, faction, colour]) + "\n")
    for wall in my_game.spaces[current_map + " space"].walls:
        x1 = str(wall.start.x)
        y1 = str(wall.start.y)
        x2 = str(wall.end.x)
        y2 = str(wall.end.y)
        file.write(":".join([x1, y1, x2, y2]) + "\n")
    file.close()
    clear_map()

def load_map(name):
    file_path = "maps/" + name + ".txt"
    if os.path.exists(file_path):
        clear_map()
        file = open("maps/" + name + ".txt", "r")
        x = int(file.readline())
        y = int(file.readline())
        tile = int(file.readline())
        agents = int(file.readline())
        walls = int(file.readline())
        make_map(x, y, tile, name)
        for i in range(agents):
            agent_data = file.readline().strip("\n").split(":")
            add_agent(float(agent_data[0]), float(agent_data[1]), agent_data[2], agent_data[3])
        for i in range(walls):
            wall_data = file.readline().strip("\n").split(":")
            add_wall([float(wall_data[0]), float(wall_data[1])], [float(wall_data[2]), float(wall_data[3])])
    else:
        print("does not exist")

def add_agent_to_queue(faction, colour):
    global agent_on_queue
    agent_on_queue = {
        "faction": faction,
        "colour": colour
    }

def add_wall_to_queue():
    global wall_on_queue
    wall_on_queue = {
        "wall": True,
        "point1": None,
        "point2": None
    }

def check_agent_on_queue():
    global agent_on_queue
    if not agent_on_queue:
        return
    if not my_game.screen.window.get("DM space").clicked:
        return
    x = my_game.screen.window.get("DM space").clicked.x
    y = my_game.screen.window.get("DM space").clicked.y
    faction = agent_on_queue["faction"]
    colour = agent_on_queue["colour"]
    agent_on_queue = None
    add_agent(x, y, faction, colour)

def check_wall_on_queue():
    global wall_on_queue
    if not wall_on_queue:
        return
    if not my_game.screen.window.get("DM space").clicked:
        return
    x = my_game.screen.window.get("DM space").clicked.x
    y = my_game.screen.window.get("DM space").clicked.y
    if not wall_on_queue["point1"]:
        wall_on_queue["point1"] = game.basics.Coords([x, y])
    elif not wall_on_queue["point2"]:
        wall_on_queue["point2"] = game.basics.Coords([x, y])
        point1 = wall_on_queue["point1"]
        point2 = wall_on_queue["point2"]
        wall_on_queue = None
        add_wall(point1, point2)

def add_agent(x, y, faction, colour):
    my_game.spaces[current_map + " space"].add_agent([x, y], creature_radius, colour, faction = faction, vision_radius = vision_radius)
    my_game.screen.window.get("DM space").update_locs()
    my_game.screen.window.get("party space").update_locs()

def add_wall(point1, point2):
    my_game.spaces[current_map + " space"].add_wall(point1, point2, wall_thickness, wall_colour)
    my_game.screen.window.get("DM space").update_locs()
    my_game.screen.window.get("party space").update_locs()

def clear_map():
    global current_map
    current_map = None
    my_game.maps = {}
    my_game.spaces = {}
    my_game.screen.window.get("DM grid").remove_grid()
    my_game.screen.window.get("DM space").remove_space()
    my_game.screen.window.get("party grid").remove_grid()
    my_game.screen.window.get("party space").remove_space()

def make_map(x, y, tile, name):
    global current_map
    x_space_per_pixel = x * tile / display.x
    y_space_per_pixel = y * tile / display.y
    space_per_pixel = max(x_space_per_pixel, y_space_per_pixel)
    my_game.add_map([x,y], name + " map")
    my_game.add_space([x*tile, y*tile], name + " space")
    my_game.maps[name + " map"].fill_chessboard_pattern()
    my_game.screen.window.get("DM grid").add_grid(my_game.maps[name + " map"].tiles)
    my_game.screen.window.get("DM space").add_space(my_game.spaces[name + " space"], space_per_pixel)
    my_game.screen.window.get("party grid").add_grid(my_game.maps[name + " map"].tiles)
    my_game.screen.window.get("party space").add_space(my_game.spaces[name + " space"], space_per_pixel)
    current_map = name

def make_new_map_inputs():
    my_game.screen.window.get("middle bar").add_component([0, 0], [button.x, button.y / 4], "map x size", background = "white", input = True, active_colour = "light grey", text = "x size")
    my_game.screen.window.get("middle bar").add_component([0, button.y / 4], [button.x, button.y / 4], "map y size", background = "white", input = True, active_colour = "light grey", text = "y size")
    my_game.screen.window.get("middle bar").add_component([0, button.y * 2 / 4], [button.x, button.y / 4], "map tile size", background = "white", input = True, active_colour = "light grey", text = "tile size")
    my_game.screen.window.get("middle bar").add_component([0, button.y * 3 / 4], [button.x, button.y / 4], "map name", background = "white", input = True, active_colour = "light grey", text = "name")

def remove_new_map_inputs():
    my_game.screen.window.get("middle bar").remove("map x size")
    my_game.screen.window.get("middle bar").remove("map y size")
    my_game.screen.window.get("middle bar").remove("map tile size")
    my_game.screen.window.get("middle bar").remove("map name")

def check_new_map_inputs():
    if not my_game.output:
        return
    x, y, tile, name = None, None, None, None
    for key, value in my_game.output.items():
        if key == "map x size":
            x = int(value)
        if key == "map y size":
            y = int(value)
        if key == "map tile size":
            tile = int(value)
        if key == "map name":
            name = value
    if x and y and tile and name:
        make_map(x, y, tile, name)
    remove_new_map_inputs()

def make_load_map_inputs():
    my_game.screen.window.get("middle bar").add_component([0, button.y * 2], button, "load map name", background = "white", input = True, active_colour = "light grey", text = "name")

def remove_load_map_inputs():
    my_game.screen.window.get("middle bar").remove("load map name")

def check_load_map_inputs():
    if not my_game.output:
        return
    name = None
    for key, value in my_game.output.items():
        if key == "load map name":
            name = value
    if name:
        load_map(name)
    remove_load_map_inputs()

def make_add_agent_inputs():
    my_game.screen.window.get("DM bar").add_component([0, 0], [button.x, button.y / 2], "add agent faction", background = "white", input = True, active_colour = "light grey", text = "faction")
    my_game.screen.window.get("DM bar").add_component([0, button.y / 2], [button.x, button.y / 2], "add agent colour", background = "white", input = True, active_colour = "light grey", text = "colour")

def remove_add_agent_inputs():
    my_game.screen.window.get("DM bar").remove("add agent faction")
    my_game.screen.window.get("DM bar").remove("add agent colour")

def check_add_agent_inputs():
    if not my_game.output:
        return
    faction, colour = None, None
    for key, value in my_game.output.items():
        if key == "add agent faction":
            faction = value
        if key == "add agent colour":
            colour = value
    if faction and colour:
        add_agent_to_queue(faction, colour)
    remove_add_agent_inputs()

main()
