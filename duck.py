from constants import (
    ui,
    MIN_TAKEOFF_VELOCITY,
    GRAVITY,
    BOUNCE_ACCELERATION_Y,
    DRAG,
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

    def launch(self):
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
            self.x_velocity = x
            self.y_velocity = y

    def stop(self):
        self.is_flying = False
        self.x_velocity = 0
        self.y_velocity = 0

    def move(self, scale=1):
        scaled_x_vel = self.x_velocity * scale
        scaled_y_vel = self.y_velocity * scale
        scaled_gravity = GRAVITY * scale

        self.x += scaled_x_vel
        self.y += scaled_y_vel
        self.y_velocity -= scaled_gravity

        print(self.x, self.y, self.x_velocity, self.y_velocity)

        return self.x, self.y

    def bounce_y(self, prev_position_y):
        self.y = prev_position_y
        self.y_velocity *= BOUNCE_ACCELERATION_Y
        self.x_velocity *= DRAG

    def bounce_x(self, prev_position_x):
        self.x = prev_position_x
        self.x_velocity *= BOUNCE_ACCELERATION_X
        self.y_velocity *= DRAG
