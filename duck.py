from constants import (
    ui,
    DRAG,
    GRAVITY,
    MIN_TAKEOFF_VELOCITY,
    BOUNCE_ACCELERATION_Y,
    BOUNCE_ACCELERATION_X,
)
from utils import degrees_and_ray_to_x_y, get_hypotenuse


class Duck:
    scale_on_save = 1

    def __init__(self):
        self.x = ui.SLING_POINT
        self.y = ui.FLOOR_LEVEL + ui.SPRITE_HEIGHT
        self.x_velocity = 0
        self.y_velocity = 0
        self.angle = 10
        self.force = 5
        self.is_flying = False

    def launch(self, scale=1):
        current_x_velocity, current_y_velocity = degrees_and_ray_to_x_y(
            self.angle, self.force
        )
        current_takeoff_velocity = get_hypotenuse(
            current_x_velocity, current_y_velocity
        )
        if current_takeoff_velocity < MIN_TAKEOFF_VELOCITY:
            return

        if not self.is_flying:
            self.is_flying = True
            x, y = degrees_and_ray_to_x_y(self.angle, self.force)
            self.x_velocity = x * scale
            self.y_velocity = y * scale

    def stop(self):
        self.is_flying = False
        self.x_velocity = 0
        self.y_velocity = 0

    def move(self, scale=1):
        scaled_gravity = GRAVITY * scale

        self.x += min(self.x_velocity, ui.SPRITE_WIDTH)
        self.y += min(self.y_velocity, ui.SPRITE_HEIGHT)
        self.y_velocity -= scaled_gravity

        return self.x, self.y

    def bounce_y(self, prev_position_y):
        self.y = prev_position_y
        self.y_velocity *= BOUNCE_ACCELERATION_Y
        self.x_velocity *= DRAG

    def bounce_x(self, prev_position_x):
        self.x = prev_position_x
        self.x_velocity *= BOUNCE_ACCELERATION_X
        self.y_velocity *= DRAG
