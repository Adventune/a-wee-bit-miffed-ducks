from constants import ui, MIN_TAKEOFF_VELOCITY
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
