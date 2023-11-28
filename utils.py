from math import radians, sin, cos
from constants import ui


def is_within_bounds(x_to_test, y_to_test, x_1, y_1, x_2, y_2):
    """
    Checks if the given x and y coordinates are within the given bounds.
    """
    return x_1 <= x_to_test <= x_2 and y_1 <= y_to_test <= y_2


def degrees_and_ray_to_x_y(degrees, ray):
    rad_angle = radians(degrees)
    x = ray * cos(rad_angle)
    y = ray * sin(rad_angle)
    return x, y


def sprites_overlap(x_1, y_1, x_2, y_2):
    """
    Checks if two tile sprites overlap
    """

    return (
        is_within_bounds(
            x_1, y_1, x_2, y_2, x_2 + ui.SPRITE_WIDTH, y_2 + ui.SPRITE_HEIGHT
        )
        or is_within_bounds(
            x_1 + ui.SPRITE_WIDTH,
            y_1,
            x_2,
            y_2,
            x_2 + ui.SPRITE_WIDTH,
            y_2 + ui.SPRITE_HEIGHT,
        )
        or is_within_bounds(
            x_1,
            y_1 + ui.SPRITE_HEIGHT,
            x_2,
            y_2,
            x_2 + ui.SPRITE_WIDTH,
            y_2 + ui.SPRITE_HEIGHT,
        )
        or is_within_bounds(
            x_1 + ui.SPRITE_WIDTH,
            y_1 + ui.SPRITE_HEIGHT,
            x_2,
            y_2,
            x_2 + ui.SPRITE_WIDTH,
            y_2 + ui.SPRITE_HEIGHT,
        )
    )


def is_on_screen(x, y):
    """
    Checks if the given x and y coordinates are on the screen.
    """
    return is_within_bounds(x, y, 0, 0, ui.WINDOW_WIDTH, ui.WINDOW_HEIGHT)


def get_hypotenuse(x_leg, y_leg):
    """
    Returns the hypotenuse of the given x and y cathetus.
    """
    return (x_leg**2 + y_leg**2) ** 0.5
