import constants
from clickable_area import ClickableArea
from scene import Scene
from game_lib import (clear_window, draw_background, begin_graphics_draw, prepare_text,
                      draw_graphics, set_scene, close, mouse)

PLAY_BUTTON_X = constants.WINDOW_WIDTH / 2
PLAY_BUTTON_Y = 240

QUIT_BUTTON_X = constants.WINDOW_WIDTH / 2
QUIT_BUTTON_Y = 145

clickable_areas: list[ClickableArea] = []


def menu_draw():
    """
    Draws the menu screen.
    """
    clear_window()
    draw_background()
    begin_graphics_draw()

    global clickable_areas
    clickable_areas = [prepare_text("Play", PLAY_BUTTON_X, PLAY_BUTTON_Y,
                                    onclick=lambda: set_scene("levels").init(), anchor_x="center"),
                       prepare_text("Quit", QUIT_BUTTON_X, QUIT_BUTTON_Y,
                                    onclick=lambda: close(), anchor_x="center")]

    prepare_text("A Wee Bit Miffed Ducks", constants.WINDOW_WIDTH / 2, 450)

    draw_graphics()


def menu_mouse_handle(x, y, button, modifiers):
    """
    Handles mouse events for the menu screen.
    """
    if button == mouse.LEFT:
        for clickable_area in clickable_areas:
            if clickable_area.is_within_bounds(x, y):
                clickable_area.onclick()


MENU_SCENE = Scene(draw_handler=menu_draw, mouse_handler=menu_mouse_handle)
