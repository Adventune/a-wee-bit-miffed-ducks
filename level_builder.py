from constants import (
    ui,
)
from game_lib import (
    clear_window,
    draw_background,
    begin_graphics_draw,
    prepare_sprite,
    mouse,
    draw_graphics,
    prepare_text,
    key,
    set_draw_handler,
    set_mouse_handler,
    set_mouse_move_handler,
    set_keyboard_handler,
    set_drag_handler,
    start,
    load_sprites,
    create_window,
)

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

    # Add sprite options (crate, stone, donkey, hard_crate) to batch with a number below
    margin = 30
    top_margin = 50
    for index, spriteName in enumerate(["crate", "stone", "donkey", "hard_crate"]):
        prepare_sprite(
            spriteName,
            x=ui.WINDOW_WIDTH / 2
            - ui.SPRITE_WIDTH / 2
            - (ui.SPRITE_WIDTH + margin)
            * (1.5 - index),  # This magic value seems to center everything best
            y=ui.WINDOW_HEIGHT - ui.SPRITE_HEIGHT - top_margin,
            scale=ui.WINDOW_RESIZE_SCALE,
        )
        prepare_text(
            str(index + 1),
            x=ui.WINDOW_WIDTH / 2
            - ui.SPRITE_WIDTH / 2
            - (ui.SPRITE_WIDTH + margin) * (1.2 - index),  # Same here
            y=ui.WINDOW_HEIGHT - ui.SPRITE_HEIGHT - top_margin - ui.SPRITE_HEIGHT - 10,
            anchor_x="center",
        )
        # Prepare single dot to the middle of the screen
        # Uncomment if adding sprites to get the screen center
        # prepare_text(".", x=ui.WINDOW_WIDTH / 2, y=ui.WINDOW_HEIGHT - 120)

    # Add instructions to batch
    prepare_text(
        "Click to place a sprite. Right click to remove a sprite. Ctrl + S to save",
        x=ui.WINDOW_WIDTH / 2,
        y=ui.WINDOW_HEIGHT - 10,
        anchor_y="top",
        size=15,
    )

    # Add floor sprites to batch
    for i in range(0, ui.WINDOW_WIDTH, ui.SPRITE_WIDTH):
        prepare_sprite("stone", x=i, y=0, scale=ui.WINDOW_RESIZE_SCALE)

    # Add sprites from objects list to batch
    for obj in objects:
        match obj["type"]:
            case "soft":
                prepare_sprite(
                    "crate",
                    x=obj["x"] * ui.WINDOW_RESIZE_SCALE,
                    y=obj["y"] * ui.WINDOW_RESIZE_SCALE,
                    scale=ui.WINDOW_RESIZE_SCALE,
                )
            case "unbreakable":
                prepare_sprite(
                    "stone",
                    x=obj["x"] * ui.WINDOW_RESIZE_SCALE,
                    y=obj["y"] * ui.WINDOW_RESIZE_SCALE,
                    scale=ui.WINDOW_RESIZE_SCALE,
                )
            case "donkey":
                prepare_sprite(
                    "donkey",
                    x=obj["x"] * ui.WINDOW_RESIZE_SCALE,
                    y=obj["y"] * ui.WINDOW_RESIZE_SCALE,
                    scale=ui.WINDOW_RESIZE_SCALE,
                )
            case "hard":
                prepare_sprite(
                    "hard_crate",
                    x=obj["x"] * ui.WINDOW_RESIZE_SCALE,
                    y=obj["y"] * ui.WINDOW_RESIZE_SCALE,
                    scale=ui.WINDOW_RESIZE_SCALE,
                )

    # Add current sprite to batch at mouse pos
    x = (
        40
        * round((mouse_pos[0] / ui.WINDOW_RESIZE_SCALE) / 40)
        * ui.WINDOW_RESIZE_SCALE
    )
    y = (
        40
        * round((mouse_pos[1] / ui.WINDOW_RESIZE_SCALE) / 40)
        * ui.WINDOW_RESIZE_SCALE
    )

    match current_sprite:
        case 0:
            prepare_sprite("crate", x=x, y=y, scale=ui.WINDOW_RESIZE_SCALE)
        case 1:
            prepare_sprite("stone", x=x, y=y, scale=ui.WINDOW_RESIZE_SCALE)
        case 2:
            prepare_sprite("donkey", x=x, y=y, scale=ui.WINDOW_RESIZE_SCALE)
        case 3:
            prepare_sprite(
                "hard_crate",
                x=x,
                y=y,
                scale=ui.WINDOW_RESIZE_SCALE,
            )

    draw_graphics()  # Draw everything


def modify_objects(button):
    """
    Modifies the objects list according to the given button.
    """
    # Place sprite into objects list with x, y, sprite name,
    # if location contains a sprite, remove it from the list
    global objects, last_action

    x = 40 * round(mouse_pos[0] / ui.WINDOW_RESIZE_SCALE / 40)
    y = 40 * round(mouse_pos[1] / ui.WINDOW_RESIZE_SCALE / 40)

    # Remove sprite from objects list if it is in the same position as the last action
    if button == mouse.LEFT or button == mouse.RIGHT:
        if (
            x == last_action["pos_x"]
            and y == last_action["pos_y"]
            and button == last_action["type"]
        ):
            return

        last_action["pos_x"] = x
        last_action["pos_y"] = y
        last_action["type"] = button

        objects = list(
            filter(
                lambda obj: obj["x"] != x or obj["y"] != y,
                objects,
            )
        )

    # Add sprite to objects list if action is left click
    if button == mouse.LEFT:
        match current_sprite:
            case 0:
                objects.append({"x": x, "y": y, "type": "soft"})
            case 1:
                objects.append({"x": x, "y": y, "type": "unbreakable"})
            case 2:
                objects.append({"x": x, "y": y, "type": "donkey"})
            case 3:
                objects.append({"x": x, "y": y, "type": "hard"})

        print(objects)
        print(ui.WINDOW_RESIZE_SCALE)


def mouse_press(x, y, button, modifiers):
    """
    Handles mouse press events.
    """
    modify_objects(button)


def mouse_drag(x, y, dx, dy, button, modifiers):
    """
    Handles mouse drag events.
    """
    updateMousePos(x, y)
    modify_objects(button)


def mouse_motion(x, y, dx, dy):
    """
    Handles mouse motion events.
    """
    # Set mouse pos rounded down to nearest sprite
    updateMousePos(x, y)


def updateMousePos(x, y):
    global mouse_pos
    mouse_pos = (
        max(
            ui.OBSTACLE_START_X,
            min(ui.WINDOW_WIDTH, x // ui.SPRITE_WIDTH * ui.SPRITE_WIDTH),
        ),
        max(
            ui.FLOOR_LEVEL,
            min(ui.WINDOW_HEIGHT, y // ui.SPRITE_HEIGHT * ui.SPRITE_HEIGHT),
        ),
    )


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
        json.dump(
            {
                "name": level_name,
                "description": level_description,
                "ducks": ducks,
                "objects": objects,
            },
            f,
        )

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
    elif sym == key._4:
        current_sprite = 3
    elif sym == key.S and modifiers & key.MOD_CTRL:
        level_name, level_description, ducks = prompt_level_info()
        save_level(level_name, level_description, ducks)


def main():
    """
    The main function of level builder.
    """
    load_sprites("sprites", "sprites/level_images")
    create_window(width=ui.WINDOW_WIDTH, height=ui.WINDOW_HEIGHT)

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
