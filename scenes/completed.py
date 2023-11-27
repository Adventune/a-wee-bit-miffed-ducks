from game_lib import (
    clear_window,
    draw_background,
    begin_graphics_draw,
    prepare_text,
    draw_graphics,
    set_scene,
    key,
)
from constants import ui
from scene import Scene


def completed_draw():
    clear_window()
    draw_background()
    begin_graphics_draw()

    # Congratulate on winning the game
    prepare_text(
        "Congratulations! You have completed the game!",
        ui.WINDOW_WIDTH / 2,
        ui.WINDOW_HEIGHT - 100,
    )

    prepare_text(
        "Only the fiercest of ducks can do that.",
        ui.WINDOW_WIDTH / 2,
        ui.WINDOW_HEIGHT - 150,
    )
    prepare_text("You are one of them.", ui.WINDOW_WIDTH / 2, ui.WINDOW_HEIGHT - 200)
    prepare_text("You are a fierce duck.", ui.WINDOW_WIDTH / 2, ui.WINDOW_HEIGHT - 250)
    prepare_text(
        "Or just a duck with a lot of time on your hands.",
        ui.WINDOW_WIDTH / 2,
        ui.WINDOW_HEIGHT - 300,
    )
    prepare_text(
        "Or maybe I didn't have enough time to make more levels.",
        ui.WINDOW_WIDTH / 2,
        ui.WINDOW_HEIGHT - 350,
    )
    prepare_text(
        "Either way, you are a duck and not a pesky donkey.",
        ui.WINDOW_WIDTH / 2,
        ui.WINDOW_HEIGHT - 450,
    )
    prepare_text("Congratulations!", ui.WINDOW_WIDTH / 2, ui.WINDOW_HEIGHT - 500)
    prepare_text(
        "Press 'Enter' to return to the menu.",
        ui.WINDOW_WIDTH / 2,
        ui.WINDOW_HEIGHT - 750,
    )

    draw_graphics()


def completed_key_handle(sym, modifiers):
    if sym == key.ENTER:
        set_scene("menu")


COMPLETED_SCENE = Scene(
    draw_handler=completed_draw, keyboard_handler=completed_key_handle
)
