from gorgame import game

#CONSTANTS
global my_game
display = game.basics.Coords([1100, 600])
top_bar = game.basics.Coords([display.x, 100])
middle_bar = game.basics.Coords([200, display.y + top_bar.y])
button = game.basics.Coords([middle_bar.x, 50])
size = (display.x * 2 + middle_bar.x, display.y + top_bar.y)
display_order = ["DM", "party"]


def main():
    setup()
    while True:
        my_game.loop()

def setup():
    global my_game
    my_game = game.Game(size)
    my_game.screen.window.add_component([0, 0], top_bar, 1, display_order[0] + " bar", background = "red", window = True)
    my_game.screen.window.add_component([0, top_bar.y], display, 1, display_order[0] + " display", background = "grey", spaceview = True)
    my_game.screen.window.add_component([display.x, 0], middle_bar, 1, "middle bar", background = "blue", window = True)
    my_game.screen.window.add_component([display.x + middle_bar.x, 0], top_bar, 1, display_order[1] + " bar", background = "red", window = True)
    my_game.screen.window.add_component([display.x + middle_bar.x, top_bar.y], display, 1, display_order[1] + " display", background = "grey", spaceview = True)

    my_game.screen.window.get("middle bar").add_component([0, 0], button, 1, "new map button", background = "green", button = True)
    my_game.screen.window.get("middle bar").get("new map button").add_text("New map", "black")

main()
