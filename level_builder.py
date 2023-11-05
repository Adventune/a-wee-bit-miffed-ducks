from constants import (OBSTACLE_START_X, WINDOW_WIDTH, WINDOW_HEIGHT, FLOOR_LEVEL, SPRITE_WIDTH,
                       SPRITE_HEIGHT)
from game_lib import (clear_window, draw_background, begin_graphics_draw, prepare_sprite,
                      mouse, draw_graphics, prepare_text, key, set_draw_handler,
                      set_mouse_handler, set_mouse_move_handler, set_keyboard_handler,
                      set_drag_handler, start, load_sprites, create_window)

BUILD_LIMITS_X = [OBSTACLE_START_X, WINDOW_WIDTH]
BUILD_LIMITS_Y = [FLOOR_LEVEL, WINDOW_HEIGHT]

current_sprite = 0
mouse_pos = (0, 0)

objects = []

last_action = {"pos_x": 0, "pos_y": 0, "type": None}


def draw():
    """
    Handles drawing the level builder.
    """

    # Draw background
    clear_window()
    draw_background()

    begin_graphics_draw()  # Begin drawing

    # Add sprite options (crate, stone, donkey) to batch with a number below
    margin = 30
    top_margin = 50
    prepare_sprite("crate", x=WINDOW_WIDTH / 2 - SPRITE_WIDTH / 2 - (SPRITE_WIDTH + margin),
                   y=WINDOW_HEIGHT - SPRITE_HEIGHT - top_margin)
    prepare_sprite("stone", x=WINDOW_WIDTH / 2 - SPRITE_WIDTH / 2,
                   y=WINDOW_HEIGHT - SPRITE_HEIGHT - top_margin)
    prepare_sprite("donkey", x=WINDOW_WIDTH / 2 - SPRITE_WIDTH / 2 + SPRITE_WIDTH + margin,
                   y=WINDOW_HEIGHT - SPRITE_HEIGHT - top_margin)

    prepare_text("1",
                 x=WINDOW_WIDTH / 2 - SPRITE_WIDTH / 2 - (SPRITE_WIDTH + margin) + SPRITE_WIDTH / 2,
                 y=WINDOW_HEIGHT - SPRITE_HEIGHT - top_margin - SPRITE_HEIGHT / 2 - 10,
                 anchor_y="top")
    prepare_text("2",
                 x=WINDOW_WIDTH / 2 - SPRITE_WIDTH / 2 + SPRITE_WIDTH / 2,
                 y=WINDOW_HEIGHT - SPRITE_HEIGHT - top_margin - SPRITE_HEIGHT / 2 - 10,
                 anchor_y="top")
    prepare_text("3",
                 x=WINDOW_WIDTH / 2 - SPRITE_WIDTH / 2 + SPRITE_WIDTH + margin + SPRITE_WIDTH / 2,
                 y=WINDOW_HEIGHT - SPRITE_HEIGHT - top_margin - SPRITE_HEIGHT / 2 - 10,
                 anchor_y="top")

    # Add instructions to batch
    prepare_text("Click to place a sprite. Right click to remove a sprite. Ctrl + S to save",
                 x=WINDOW_WIDTH / 2,
                 y=WINDOW_HEIGHT - 10, anchor_y="top", size=15)

    # Add floor sprites to batch
    for i in range(0, WINDOW_WIDTH, SPRITE_WIDTH):
        prepare_sprite("stone", x=i, y=0)

    # Add sprites from objects list to batch
    for obj in objects:
        match obj["type"]:
            case "soft":
                prepare_sprite("crate", x=obj["x"], y=obj["y"])
            case "unbreakable":
                prepare_sprite("stone", x=obj["x"], y=obj["y"])
            case "donkey":
                prepare_sprite("donkey", x=obj["x"], y=obj["y"])

    # Add current sprite to batch at mouse pos
    match current_sprite:
        case 0:
            prepare_sprite("crate", x=mouse_pos[0], y=mouse_pos[1])
        case 1:
            prepare_sprite("stone", x=mouse_pos[0], y=mouse_pos[1])
        case 2:
            prepare_sprite("donkey", x=mouse_pos[0], y=mouse_pos[1])

    draw_graphics()  # Draw everything


def modify_objects(button):
    """
    Modifies the objects list according to the given button.
    """
    # Place sprite into objects list with x, y, sprite name,
    # if location contains a sprite, remove it from the list
    global objects, last_action

    # Remove sprite from objects list if it is in the same position as the last action
    if button == mouse.LEFT or button == mouse.RIGHT:
        if (mouse_pos[0] == last_action["pos_x"] and mouse_pos[1] == last_action["pos_y"]
                and button == last_action["type"]):
            return

        last_action["pos_x"] = mouse_pos[0]
        last_action["pos_y"] = mouse_pos[1]
        last_action["type"] = button

        objects = list(
            filter(lambda obj: obj["x"] != mouse_pos[0] or obj["y"] != mouse_pos[1], objects))

    # Add sprite to objects list if action is left click
    if button == mouse.LEFT:
        match current_sprite:
            case 0:
                objects.append({"x": mouse_pos[0], "y": mouse_pos[1], "type": "soft"})
            case 1:
                objects.append({"x": mouse_pos[0], "y": mouse_pos[1], "type": "unbreakable"})
            case 2:
                objects.append({"x": mouse_pos[0], "y": mouse_pos[1], "type": "donkey"})


def mouse_press(x, y, button, modifiers):
    """
    Handles mouse press events.
    """
    modify_objects(button)


def mouse_drag(x, y, dx, dy, button, modifiers):
    """
    Handles mouse drag events.
    """

    # Draw sprite at mouse pos
    global mouse_pos
    mouse_pos = (max(OBSTACLE_START_X, min(WINDOW_WIDTH, x // SPRITE_WIDTH * SPRITE_WIDTH)),
                 max(FLOOR_LEVEL, min(WINDOW_HEIGHT, y // SPRITE_HEIGHT *
                                      SPRITE_HEIGHT)))
    modify_objects(button)


def mouse_motion(x, y, dx, dy):
    """
    Handles mouse motion events.
    """
    # Set mouse pos rounded down to nearest sprite
    global mouse_pos
    mouse_pos = (max(OBSTACLE_START_X, min(WINDOW_WIDTH, x // SPRITE_WIDTH * SPRITE_WIDTH)),
                 max(FLOOR_LEVEL, min(WINDOW_HEIGHT, y // SPRITE_HEIGHT *
                                      SPRITE_HEIGHT)))


def prompt_level_info():
    """
    Prompts the user for level info.
    """
    level_name = input("Enter level name: ")
    level_description = input("Enter level description: ")
    ducks = 0
    while ducks < 1:
        try:
            ducks = int(input("Enter number of ducks: "))
        except ValueError:
            print("Please enter a number")
    return level_name, level_description, ducks


def save_level(level_name, level_description, ducks):
    """
    Saves the level.
    """
    import json
    import os

    # Save the level
    # Get the level number
    current_level_files = os.listdir("levels")
    level = 0
    for i in current_level_files:
        if i.endswith(".json"):
            level += 1

    # Create a new file with the level number
    with open(f"levels/level_{level}.json", "w") as f:
        json.dump({"name": level_name, "description": level_description, "ducks": ducks,
                   "objects": objects}, f)

        print(f"Saved level with index of {level}.")


def key_press(sym, modifiers):
    """
    Handles key press events.
    """
    if sym == key._1:
        global current_sprite
        current_sprite = 0
    elif sym == key._2:
        current_sprite = 1
    elif sym == key._3:
        current_sprite = 2
    elif sym == key.S and modifiers & key.MOD_CTRL:
        level_name, level_description, ducks = prompt_level_info()
        save_level(level_name, level_description, ducks)


def main():
    """
    The main function of level builder.
    """
    load_sprites("sprites", "sprites/level_images")
    create_window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

    set_draw_handler(draw)
    set_mouse_handler(mouse_press)
    set_mouse_move_handler(mouse_motion)
    set_keyboard_handler(key_press)
    set_drag_handler(mouse_drag)

    start()


if __name__ == "__main__":
    main()
else:
    print("Please run this file directly.")
