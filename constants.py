import os

TOTAL_LEVEL_COUNT = 0
# Yeah it is "constants" but I don't want to change it
# Every time a new level is added
level_files = os.listdir("levels")
for file in level_files:
    if file.endswith(".json"):
        TOTAL_LEVEL_COUNT += 1


# ======================== UI ========================
# UI Constants aren't really constants either, but they are scaled by the window size


class UIConstants:
    WINDOW_RESIZE_SCALE = 1
    ASPECT_RATIO = 9 / 16
    WINDOW_WIDTH = 1400  # Can anything divisible by 40
    WINDOW_HEIGHT = round(WINDOW_WIDTH * ASPECT_RATIO)

    SPRITE_WIDTH = 40
    SPRITE_HEIGHT = SPRITE_WIDTH

    FLOOR_LEVEL = SPRITE_HEIGHT
    SLING_POINT = 120

    OBSTACLE_START_X = 600

    LEVEL_IMAGE_WIDTH = 1420
    LEVEL_IMAGE_HEIGHT = 855

    LEVEL_IMAGE_SCALE = 0.2

    LEVEL_IMAGE_SCALED_WIDTH = LEVEL_IMAGE_WIDTH * LEVEL_IMAGE_SCALE
    LEVEL_IMAGE_SCALED_HEIGHT = LEVEL_IMAGE_HEIGHT * LEVEL_IMAGE_SCALE

    def __init__(self):
        return

    def resize_handler(self, width, height):
        self.WINDOW_RESIZE_SCALE = width / 1400

        # Update all variables that are scaled with window resize
        self.WINDOW_WIDTH = round(width)
        self.WINDOW_HEIGHT = round(height)
        self.SPRITE_WIDTH = round(40 * self.WINDOW_RESIZE_SCALE)
        self.SLING_POINT = round(120 * self.WINDOW_RESIZE_SCALE)
        self.OBSTACLE_START_X = round(600 * self.WINDOW_RESIZE_SCALE)
        self.LEVEL_IMAGE_WIDTH = round(1420 * self.WINDOW_RESIZE_SCALE)
        self.LEVEL_IMAGE_HEIGHT = round(855 * self.WINDOW_RESIZE_SCALE)

        # Update values that are dependant on above values
        self.LEVEL_IMAGE_SCALED_WIDTH = self.LEVEL_IMAGE_WIDTH * self.LEVEL_IMAGE_SCALE
        self.LEVEL_IMAGE_SCALED_HEIGHT = (
            self.LEVEL_IMAGE_HEIGHT * self.LEVEL_IMAGE_SCALE
        )
        self.SPRITE_HEIGHT = self.SPRITE_WIDTH
        self.FLOOR_LEVEL = self.SPRITE_HEIGHT


ui = UIConstants()

# ======================== Game ========================

GRAVITY = 1
# Some magic values tested to work well

FORCE_DIVIDER = 10
BOUNCE_ACCELERATION_Y = -0.5
BOUNCE_ACCELERATION_X = -0.8
MIN_Y_VELOCITY = (3 + 1 / 3) * GRAVITY
MIN_X_VELOCITY = (3 + 1 / 3) * GRAVITY
DRAG = 0.5
HIT_DRAG = 0.8
MIN_BREAK_VELOCITY = (3 + 1 / 3) * GRAVITY
MIN_HARD_BREAK_VELOCITY = (20) * GRAVITY

MIN_TAKEOFF_VELOCITY = 10 * GRAVITY
