from constants import SLING_POINT, FLOOR_LEVEL, SPRITE_HEIGHT

DEFAULT_LEVEL = {
    "name": "",
    "description": "",
    "ducks": 0,
    "objects": []
}

DEFAULT_GAME = {
    "level_progress": 0,
    "random_levels_completed": 0,
    "random_high_score": 0
}

DEFAULT_DUCK = {
    "x": SLING_POINT,
    "y": FLOOR_LEVEL + SPRITE_HEIGHT,
    "x_velocity": 0,
    "y_velocity": 0,
    "angle": 10,
    "force": 5,
    "is_flying": False,
}
