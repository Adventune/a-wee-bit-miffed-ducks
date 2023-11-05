import json
from clickable_area import ClickableArea
from scene import Scene
from game_lib import (clear_window, draw_background, begin_graphics_draw, prepare_sprite,
                      key, set_scene, prepare_text, MIDDLEGROUND, FOREGROUND, draw_graphics,
                      mouse)
from constants import (WINDOW_WIDTH, WINDOW_HEIGHT, FLOOR_LEVEL, LEVEL_IMAGE_SCALED_WIDTH,
                       LEVEL_IMAGE_SCALED_HEIGHT, TOTAL_LEVEL_COUNT, LEVEL_IMAGE_SCALE)

page = 0

game = {
    "level_progress": 0,
    "random_levels_completed": 0,
    "random_high_score": 0
}

BACK_BUTTON_X = 200

LEVEL_IMAGE_X_START = WINDOW_WIDTH / 2 - (LEVEL_IMAGE_SCALED_WIDTH / 2) - (
        LEVEL_IMAGE_SCALED_WIDTH + 100)
LEVEL_IMAGE_Y_START = WINDOW_HEIGHT / 2 - (LEVEL_IMAGE_SCALED_HEIGHT / 2) + 150 - 30

clickable_areas: list[ClickableArea] = []


def level_menu_draw():
    clear_window()
    draw_background()
    begin_graphics_draw()

    temp_clickable_areas = []

    # Draw level images in a 3x2 grid with 100px padding, image size is 1420x855 scaled by 0.1
    for i in range(2):
        for j in range(3):
            # i = 0 or 1 for row
            # j = 0, 1 or 2 for column

            level = j + i * 3 + page * 6
            x = LEVEL_IMAGE_X_START + j * (LEVEL_IMAGE_SCALED_WIDTH + 100)
            y = LEVEL_IMAGE_Y_START - i * (LEVEL_IMAGE_SCALED_HEIGHT + 100)

            if level >= TOTAL_LEVEL_COUNT:
                break

            if level <= game["level_progress"]:

                def lambda_generator(value):
                    """
                    Lambda generator for the onclick function of the level image.
                    param value: The level to load.

                    return: A lambda function that loads the given level.

                    Why? Because otherwise the lambda function would always load the last+1 level.
                    """
                    return lambda: set_scene("game").init(value, 0)

                try:
                    temp_clickable_areas.append(prepare_sprite(f"level_{level}_image",
                                                               x=x, y=y,
                                                               scale=LEVEL_IMAGE_SCALE,
                                                               onclick=lambda_generator(level)))
                except KeyError:
                    temp_clickable_areas.append(prepare_sprite("level_image_placeholder",
                                                               x=x, y=y,
                                                               scale=LEVEL_IMAGE_SCALE,
                                                               onclick=lambda_generator(level)))

                prepare_text(f"Level {str(level)}",
                             x=x,
                             y=y - 50,
                             anchor_x="left")
            else:
                try:
                    prepare_sprite(f"level_{level}_image",
                                   x=x, y=y, scale=LEVEL_IMAGE_SCALE, group=MIDDLEGROUND)
                except KeyError:
                    prepare_sprite("level_image_placeholder",
                                   x=x, y=y, scale=LEVEL_IMAGE_SCALE, group=MIDDLEGROUND)

                prepare_sprite("locked_overlay",
                               x=x, y=y, scale=LEVEL_IMAGE_SCALE, group=FOREGROUND)

    prepare_text("Level Menu", WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100)
    prepare_text("Press 'R' for a random level.", WINDOW_WIDTH / 2, WINDOW_HEIGHT - 150, size=15)

    # Draw back text
    temp_clickable_areas.append(
        prepare_text("Back", x=BACK_BUTTON_X, y=FLOOR_LEVEL, anchor_x="left",
                     anchor_y="bottom",
                     onclick=lambda: set_scene("menu")))

    clickable_areas.clear()
    clickable_areas.extend(temp_clickable_areas)

    if TOTAL_LEVEL_COUNT > 6:
        # Draw next page text
        prepare_text("Next Page", x=WINDOW_WIDTH - 200, y=FLOOR_LEVEL,
                     anchor_x="right", anchor_y="bottom")

    draw_graphics()


def level_menu_mouse_handle(click_x, click_y, button, modifiers):
    if button == mouse.LEFT:
        for clickable_area in clickable_areas:
            if clickable_area.is_within_bounds(click_x, click_y):
                clickable_area.onclick()


def level_menu_key_handle(sym, modifiers):
    if sym == key.R:
        set_scene("game").init(-1, 0)


def init():
    global page, game
    page = 0
    with open("game.json", "r") as game_data:
        game = json.load(game_data)


LEVELS_MENU_SCENE = Scene(draw_handler=level_menu_draw, release_handler=level_menu_mouse_handle,
                          keyboard_handler=level_menu_key_handle, init=init)
