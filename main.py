import json
from os.path import isfile


from constants import ui
from game_lib import load_sprites, create_window, set_scene, start
from defaults import DEFAULT_GAME


def create_game_file_if_not_exists():
    """
    Creates the game.json file with the default values.

    :return: None
    """
    if not isfile("game.json"):
        with open("game.json", "w") as file:
            json.dump(DEFAULT_GAME, file)


def main():
    """
    The main function of the game.

    Loads the sprites, creates the window, sets the scene to menu and starts the game.
    :return: None
    """
    load_sprites("sprites", "sprites/level_images")
    create_window(width=ui.WINDOW_WIDTH, height=ui.WINDOW_HEIGHT)

    create_game_file_if_not_exists()

    set_scene("menu")

    start()


if __name__ == "__main__":
    main()
else:
    print("This file is not meant to be imported.")
    exit(1)
