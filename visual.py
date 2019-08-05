from gorgame import game

#CONSTANTS
global my_game
display = game.basics.Coords([1100, 600])
top_bar = game.basics.Coords([display.x, 100])
right_bar = game.basics.Coords([200, display.y + top_bar.y])
size = (display.x + right_bar.x, display.y + top_bar.y)


def main():
    setup()
    while True:
        my_game.loop()

def setup():
    global my_game
    my_game = game.Game(size)
    my_game.screen.window.add_component([0, 0], top_bar, "red", 1, "top bar", window = True)
    my_game.screen.window.add_component([0, top_bar.y], display, "grey", 1, "dispay", spaceview = True)
    my_game.screen.window.add_component([display.x, 0], right_bar, "blue", 1, "right bar", window = True)

main()
