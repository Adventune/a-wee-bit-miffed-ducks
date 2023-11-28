import json
from math import degrees, atan
from random import randint
from copy import deepcopy
from constants import (
    ui,
    MIN_TAKEOFF_VELOCITY,
    FORCE_DIVIDER,
    GRAVITY,
    MIN_BREAK_VELOCITY,
    MIN_HARD_BREAK_VELOCITY,
    MIN_X_VELOCITY,
    MIN_Y_VELOCITY,
    DRAG,
    BOUNCE_ACCELERATION_X,
    BOUNCE_ACCELERATION_Y,
    HIT_DRAG,
    TOTAL_LEVEL_COUNT,
    LEVEL_ONGOING,
    LEVEL_COMPLETED,
    LEVEL_FAILED,
)
from scene import Scene
from game_lib import (
    clear_window,
    draw_background,
    begin_graphics_draw,
    prepare_sprite,
    key,
    draw_graphics,
    prepare_text,
    set_scene,
    FOREGROUND,
    MIDDLEGROUND,
    HELP_TEXT,
    SHADE,
    mouse,
)
from utils import degrees_and_ray_to_x_y, overlaps, get_hypotenuse
from defaults import DEFAULT_LEVEL, DEFAULT_GAME
from duck import Duck

current_duck = Duck()
level = deepcopy(DEFAULT_LEVEL)
level_copy = deepcopy(level)
game = deepcopy(DEFAULT_GAME)

thrown_ducks = []
text_objects = []

help_visible = False
drag = False
drag_start = (0, 0)
drag_current = (0, 0)

level_state = LEVEL_ONGOING
current_high_score = 0
current_level = 0


def set_level(data):
    global level, level_copy, text_objects
    level = data
    level_copy = deepcopy(data)
    text_objects = [
        obstacle for obstacle in level["objects"] if obstacle["type"] == "text"
    ]


def random_level_objects():
    global level
    level["objects"] = []
    prev_donkey_height = 0
    for i in range(20):
        objects_in_column = randint(3, 10)

        # contains_donkey = 1/5 chance of containing a donkey
        contains_donkey = randint(1, 5) == 1

        stone_height = min(prev_donkey_height, randint(0, objects_in_column - 2))

        # First stone_count objects in column are stones
        for j in range(stone_height):
            level["objects"].append(
                {
                    "type": "unbreakable",
                    "x": ui.OBSTACLE_START_X + i * ui.SPRITE_WIDTH,
                    "y": ui.FLOOR_LEVEL + j * ui.SPRITE_HEIGHT,
                    "y_velocity": 0,
                    "has_been_hit": False,
                }
            )

        # Rest of the objects are crates or one of them is a donkey
        for j in range(stone_height, objects_in_column):
            obstacle_type = (
                "soft"
                if not contains_donkey or j != objects_in_column - 1
                else "donkey"
            )

            if obstacle_type == "donkey":
                prev_donkey_height = j

            level["objects"].append(
                {
                    "type": obstacle_type,
                    "x": ui.OBSTACLE_START_X + i * ui.SPRITE_WIDTH,
                    "y": ui.FLOOR_LEVEL + j * ui.SPRITE_HEIGHT,
                    "y_velocity": 0,
                    "has_been_hit": False,
                }
            )


def launch():
    if level_state:
        return

    current_duck.launch()


def game_draw():
    clear_window()
    draw_background()
    begin_graphics_draw()

    if level_state == LEVEL_ONGOING:
        duck_x, duck_y = (current_duck.x, current_duck.y)
        prepare_sprite("duck", duck_x, duck_y, scale=ui.WINDOW_RESIZE_SCALE)

    prepare_flight_path_sprites()

    if drag:
        prepare_drag_start_and_end_sprites()

    prepare_floor_sprites()
    prepare_obstacle_sprites()

    for thrown_duck in thrown_ducks:
        x = thrown_duck.x / thrown_duck.scale_on_save * ui.WINDOW_RESIZE_SCALE
        y = thrown_duck.y / thrown_duck.scale_on_save * ui.WINDOW_RESIZE_SCALE
        prepare_sprite("duck", x, y, group=MIDDLEGROUND, scale=ui.WINDOW_RESIZE_SCALE)

    prepare_info_text()

    if level_state == LEVEL_ONGOING:
        prepare_level_text_objects()
    if help_visible:
        prepare_help_text()

    if level_state == LEVEL_COMPLETED:
        prepare_level_completed_text()
    if level_state == LEVEL_FAILED:
        prepare_level_failed_text()

    draw_graphics()


def game_keypress_handler(sym, mods):
    global thrown_ducks, level_state, current_level, current_high_score

    match sym:
        case key.R:
            if level_state == LEVEL_FAILED:
                current_high_score = 0
            game_init(current_level, current_high_score)
        case key.H:
            global help_visible
            help_visible = not help_visible
        case key.RIGHT:
            current_duck.angle -= 10
            if current_duck.angle < 10:
                current_duck.angle = 350
        case key.LEFT:
            current_duck.angle += 10
            if current_duck.angle > 350:
                current_duck.angle = 10
        case key.UP:
            if current_duck.force < 50:
                current_duck.force += 5
        case key.DOWN:
            if current_duck.force >= 5:
                current_duck.force -= 5
            else:
                current_duck.force = 0
        case key.ESCAPE:
            set_scene("levels").init()
        case key.ENTER | key.SPACE:
            if level_state == LEVEL_ONGOING:
                launch()
            elif level_state == LEVEL_COMPLETED:
                if current_level == -1:
                    current_high_score += 1
                    level_completed(random_level=True, score=current_high_score)
                    game_init(-1, current_high_score)
                elif current_level + 1 == TOTAL_LEVEL_COUNT:
                    level_completed()
                    set_scene("completed")
                else:
                    level_completed()
                    game_init(current_level + 1)
            elif level_state == LEVEL_FAILED:
                current_high_score = 0
                game_init(current_level, 0)


def game_mouse_down_handler(x, y, button, modifiers):
    if level_state or help_visible:
        return

    if button == mouse.LEFT:
        global drag_start, drag
        drag_start = (x, y)
        drag = True


def game_mouse_release_handler(x, y, button, modifiers):
    if level_state or help_visible:
        return

    if button == mouse.LEFT:
        global drag, drag_start, drag_current
        drag = False
        drag_start = (0, 0)
        drag_current = (0, 0)
        launch()


def game_drag_handler(x, y, dx, dy, buttons, modifiers):
    if level_state or help_visible:
        return

    # Create vector from drag start to current mouse position
    real_dx = drag_start[0] - x + 0.001  # Add 0.001 to avoid division by zero
    real_dy = drag_start[1] - y

    # Calculate angle from vector
    angle = round(degrees(atan(max(0, real_dy) / real_dx)))
    force = round(
        get_hypotenuse(real_dx, real_dy) / FORCE_DIVIDER * ui.WINDOW_RESIZE_SCALE
    )

    # Clamp force between 5 and 50
    force = max(5, min(50, force))
    # Clamp angle between 20 and 80
    angle = max(5, min(80, abs(angle)))

    # Set angle and force
    current_duck.angle = angle
    current_duck.force = force
    global drag_current
    drag_current = (x, y)


def game_update(dt):
    global level_state, current_duck, thrown_ducks, level, current_level, current_high_score

    scaled_x_vel = current_duck.x_velocity * ui.WINDOW_RESIZE_SCALE
    scaled_y_vel = current_duck.y_velocity * ui.WINDOW_RESIZE_SCALE
    scaled_gravity = GRAVITY * ui.WINDOW_RESIZE_SCALE
    scaled_break_velocity = MIN_BREAK_VELOCITY * ui.WINDOW_RESIZE_SCALE
    scaled_hard_break_velocity = MIN_HARD_BREAK_VELOCITY * ui.WINDOW_RESIZE_SCALE
    scaled_min_y_vel = MIN_Y_VELOCITY * ui.WINDOW_RESIZE_SCALE
    scaled_min_x_vel = MIN_X_VELOCITY * ui.WINDOW_RESIZE_SCALE

    donkeys_remaining = len(
        [obstacle for obstacle in level["objects"] if obstacle["type"] == "donkey"]
    )

    if level["ducks"] == len(thrown_ducks) or donkeys_remaining == 0:
        if level_state == LEVEL_ONGOING:
            level_state = LEVEL_FAILED if donkeys_remaining > 0 else LEVEL_COMPLETED

    else:
        flight_ended = False
        if current_duck.is_flying:
            # A duck is currently in the air
            # Save ducks position before updating it
            prev_position_x = current_duck.x
            prev_position_y = current_duck.y

            # Update ducks position
            current_duck.x += scaled_x_vel
            current_duck.y += scaled_y_vel
            current_duck.y_velocity -= scaled_gravity

            nearby_objects = get_nearby_objects(current_duck.x, current_duck.y)
            for obstacle in nearby_objects:
                obstacle_x, obstacle_y = (
                    obstacle["x"] * ui.WINDOW_RESIZE_SCALE,
                    obstacle["y"] * ui.WINDOW_RESIZE_SCALE,
                )

                duck_x, duck_y = current_duck.x, current_duck.y

                # Go through every obstacle near the duck and check if it overlaps with the duck
                if overlaps(duck_x, duck_y, obstacle_x, obstacle_y):
                    velocity_hypotenuse = get_hypotenuse(
                        current_duck.x_velocity, current_duck.y_velocity
                    )
                    # Object is destroyable if:
                    # 1. It is a soft obstacle
                    # 2. It is a donkey
                    # 3. It is a hard obstacle and has been hit before
                    # 4. Object is hard and duck is moving fast enough
                    if (
                        obstacle["type"] == "soft"
                        or obstacle["type"] == "donkey"
                        or (
                            obstacle["type"] == "hard"
                            and (
                                obstacle.get("has_been_hit", False)
                                or velocity_hypotenuse > scaled_hard_break_velocity
                            )
                        )
                    ):
                        # Here we handle all destroyable objects and destroy them
                        # if they are hit with enough force

                        # If duck collides with an soft obstacle, remove obstacle
                        # and lower ducks velocity
                        if velocity_hypotenuse > scaled_break_velocity:
                            drag_addition = 0
                            if obstacle["type"] == "hard":
                                drag_addition = 0.2
                            level["objects"].remove(obstacle)
                            current_duck.x_velocity *= HIT_DRAG - drag_addition
                            current_duck.y_velocity *= HIT_DRAG - drag_addition

                    # Object is not destroyable if:
                    # 1. It is an unbreakable obstacle
                    # 2. It is a hard obstacle and has not been hit before
                    # 3. It is destroyable but the duck is not moving fast enough
                    if (
                        obstacle["type"] == "unbreakable"
                        or (
                            obstacle["type"] == "hard"
                            and not obstacle.get("has_been_hit", False)
                            and velocity_hypotenuse < scaled_hard_break_velocity
                        )
                        or velocity_hypotenuse < scaled_break_velocity
                    ):
                        # Set that the obstacle has been hit
                        # It doesn't matter if it is destroyable or not
                        if not obstacle.get("has_been_hit", False):
                            obstacle["has_been_hit"] = True

                        # Duck has previously been above or below the obstacle
                        # It must have entered from above or below so bounce it on the y axis
                        duck_came_from_above = (
                            prev_position_y > obstacle["y"] + ui.SPRITE_HEIGHT
                        )
                        duck_came_from_below = (
                            prev_position_y + ui.SPRITE_HEIGHT < obstacle["y"]
                        )
                        if duck_came_from_above or duck_came_from_below:
                            # If the duck is moving slow enough and it came from above
                            # stop it and add it to the list of thrown ducks
                            if (
                                (
                                    abs(current_duck.y_velocity) < scaled_min_y_vel
                                    or abs(current_duck.x_velocity) < scaled_min_x_vel
                                )
                            ) and duck_came_from_above:
                                current_duck.y_velocity = 0
                                current_duck.is_flying = False
                                current_duck.y = obstacle["y"] + ui.SPRITE_HEIGHT

                                flight_ended = True
                            else:
                                current_duck.y = prev_position_y
                                current_duck.y_velocity *= BOUNCE_ACCELERATION_Y
                                current_duck.x_velocity *= DRAG

                        # Duck has previously been to the left or right of the obstacle
                        # It must have entered from the side so bounce it on the y axis
                        else:
                            current_duck.x = prev_position_x
                            current_duck.x_velocity *= BOUNCE_ACCELERATION_X
                            current_duck.y_velocity *= DRAG

            # Duck is not colliding with any obstacles
            # Check if it flew off the screen or hit the floor
            if current_duck.x < 0 or current_duck.x > ui.WINDOW_WIDTH:
                # Stop the duck and add it to the list of thrown ducks
                current_duck.is_flying = False
                current_duck.x_velocity = 0
                current_duck.y_velocity = 0

                flight_ended = True
            elif current_duck.y < ui.FLOOR_LEVEL:
                current_duck.y = ui.FLOOR_LEVEL
                # Bounce back until the velocity is small enough
                if abs(current_duck.y_velocity) > scaled_min_y_vel:
                    current_duck.y_velocity *= BOUNCE_ACCELERATION_Y
                    current_duck.x_velocity *= DRAG

                else:
                    current_duck.y_velocity = 0
                    current_duck.is_flying = False
                    current_duck.y = ui.FLOOR_LEVEL

                    flight_ended = True
        else:
            # Duck is not flying
            # Reset ducks position
            current_duck.x = ui.SLING_POINT
            current_duck.y = ui.FLOOR_LEVEL + ui.SPRITE_HEIGHT

        if flight_ended:
            new_thrown_duck = deepcopy(current_duck)
            new_thrown_duck.scale_on_save = ui.WINDOW_RESIZE_SCALE
            thrown_ducks.append(new_thrown_duck)
            current_duck = Duck()


def game_init(level_number, high_score=0):
    print(f"Initializing level {level_number} ")
    global level_state, thrown_ducks, level, current_duck, current_level, current_high_score, game
    global text_objects

    # Initialize game values from game file
    with open("game.json", "r") as game_data:
        game = json.load(game_data)

    # Init level values to default
    current_level = level_number
    current_duck = Duck()
    level_state = LEVEL_ONGOING
    thrown_ducks = []
    text_objects = []

    if current_level == -1:
        random_level_objects()
        current_high_score = high_score
        level["name"] = "Random Level"
        level["description"] = "A randomly generated level"
        # Level ducks is at least as many as there are obstacles of type donkey
        donkeys = len(
            [obstacle for obstacle in level["objects"] if obstacle["type"] == "donkey"]
        )
        level["ducks"] = randint(max(donkeys, 3), donkeys + 3)

        global level_copy
        level_copy = deepcopy(level)

    else:
        with open(f"levels/level_{current_level}.json", "r") as levels_file:
            set_level(json.load(levels_file))


def level_completed(random_level=False, score=0):
    with open("game.json", "w") as game_data:
        new_game = deepcopy(game)
        if random_level:
            new_game["random_levels_completed"] += 1

            if score > game["random_high_score"]:
                new_game["random_high_score"] = score

        else:
            new_game["level_progress"] = max(current_level + 1, game["level_progress"])

        json.dump(new_game, game_data)


GAME_SCENE = Scene(
    draw_handler=game_draw,
    interval_handler=game_update,
    keyboard_handler=game_keypress_handler,
    mouse_handler=game_mouse_down_handler,
    release_handler=game_mouse_release_handler,
    drag_handler=game_drag_handler,
    init=game_init,
)


# ==================== HELPERS ==================== #
def prepare_flight_path_sprites():
    current_x_velocity, current_y_velocity = degrees_and_ray_to_x_y(
        current_duck.angle, current_duck.force
    )
    current_takeoff_velocity = get_hypotenuse(current_x_velocity, current_y_velocity)

    if (
        not current_duck.is_flying
        and not level_state
        and current_takeoff_velocity > MIN_TAKEOFF_VELOCITY
    ):
        x_v, y_v = degrees_and_ray_to_x_y(current_duck.angle, current_duck.force)
        i = 0

        duck_x, duck_y = (
            current_duck.x * ui.WINDOW_RESIZE_SCALE,
            current_duck.y * ui.WINDOW_RESIZE_SCALE,
        )
        while True:
            i += 1
            duck_x += x_v
            duck_y += y_v
            y_v -= GRAVITY

            if i % 2 == 0:
                prepare_sprite(
                    "flight_path",
                    duck_x,
                    duck_y,
                    group=FOREGROUND,
                    scale=ui.WINDOW_RESIZE_SCALE,
                )

            if duck_y < ui.FLOOR_LEVEL:
                break


def prepare_drag_start_and_end_sprites():
    prepare_sprite(
        "flight_path", drag_start[0], drag_start[1], scale=ui.WINDOW_RESIZE_SCALE
    )
    prepare_sprite(
        "flight_path",
        drag_current[0],
        drag_current[1],
        scale=ui.WINDOW_RESIZE_SCALE,
    )


def prepare_help_text():
    prepare_sprite("shade", x=0, y=0, group=SHADE, scale=10)

    prepare_text("Controls:", ui.WINDOW_WIDTH / 2, 630, size=20, group=HELP_TEXT)
    prepare_text(
        "Drag the mouse on the screen to launch",
        ui.WINDOW_WIDTH / 2,
        600,
        size=20,
        group=HELP_TEXT,
    )
    prepare_text(
        "OR!!! Left/Right: Change angle",
        ui.WINDOW_WIDTH / 2,
        570,
        size=20,
        group=HELP_TEXT,
    )
    prepare_text(
        "Up/Down: Change force", ui.WINDOW_WIDTH / 2, 540, size=20, group=HELP_TEXT
    )
    prepare_text(
        "Space/Enter: Launch duck",
        ui.WINDOW_WIDTH / 2,
        510,
        size=20,
        group=HELP_TEXT,
    )
    prepare_text(
        "R: Reset the level (Not available in random mode)",
        ui.WINDOW_WIDTH / 2,
        480,
        size=20,
        group=HELP_TEXT,
    )


def prepare_obstacle_sprites():
    for obstacle in level["objects"]:
        x, y = (
            obstacle["x"] * ui.WINDOW_RESIZE_SCALE,
            obstacle["y"] * ui.WINDOW_RESIZE_SCALE,
        )
        match obstacle["type"]:
            case "soft":
                prepare_sprite(
                    "crate", x, y, group=MIDDLEGROUND, scale=ui.WINDOW_RESIZE_SCALE
                )
            case "hard":
                if not obstacle.get("has_been_hit", False):
                    prepare_sprite(
                        "hard_crate",
                        x,
                        y,
                        group=MIDDLEGROUND,
                        scale=ui.WINDOW_RESIZE_SCALE,
                    )
                else:
                    prepare_sprite(
                        "hard_crate_cracked",
                        x,
                        y,
                        group=MIDDLEGROUND,
                        scale=ui.WINDOW_RESIZE_SCALE,
                    )
            case "unbreakable":
                prepare_sprite(
                    "stone", x, y, group=MIDDLEGROUND, scale=ui.WINDOW_RESIZE_SCALE
                )
            case "donkey":
                prepare_sprite(
                    "donkey", x, y, group=MIDDLEGROUND, scale=ui.WINDOW_RESIZE_SCALE
                )


def prepare_info_text():
    prepare_text(
        "H: Help",
        ui.WINDOW_WIDTH - 120,
        ui.WINDOW_HEIGHT - 60,
        size=20,
        anchor_x="right",
    )
    prepare_text("Esc: Menu", 120, ui.WINDOW_HEIGHT - 60, size=20, anchor_x="left")

    # Draw remaining ducks
    prepare_text(
        "Ducks remaining: {}".format(level["ducks"] - len(thrown_ducks)),
        ui.WINDOW_WIDTH / 2,
        ui.WINDOW_HEIGHT - 150,
        size=20,
    )
    # Draw level name
    prepare_text(level["name"], ui.WINDOW_WIDTH / 2, ui.WINDOW_HEIGHT - 60, size=20)
    # Draw level description
    prepare_text(
        level["description"], ui.WINDOW_WIDTH / 2, ui.WINDOW_HEIGHT - 90, size=20
    )

    if current_level == -1:
        prepare_text(
            "High score: {}".format(game["random_high_score"]),
            ui.WINDOW_WIDTH / 2,
            700,
            size=20,
        )
        prepare_text(f"Score: {current_high_score}", ui.WINDOW_WIDTH / 2, 670, size=20)


def prepare_floor_sprites():
    for i in range(0, ui.WINDOW_WIDTH, ui.SPRITE_WIDTH):
        prepare_sprite(
            "stone",
            i,
            ui.FLOOR_LEVEL - ui.SPRITE_HEIGHT,
            group=FOREGROUND,
            scale=ui.WINDOW_RESIZE_SCALE,
        )

    for i in range(-1, 2):
        prepare_sprite(
            "stone",
            ui.SLING_POINT + i * ui.SPRITE_WIDTH,
            ui.FLOOR_LEVEL,
            scale=ui.WINDOW_RESIZE_SCALE,
        )


def prepare_level_text_objects():
    # Loop through every text object in the level
    for object in text_objects:
        # Draw the text object
        duck_x, duck_y = (
            object["x"] * ui.WINDOW_RESIZE_SCALE,
            object["y"] * ui.WINDOW_RESIZE_SCALE,
        )
        prepare_text(
            object["text"],
            duck_x,
            duck_y,
            anchor_x="left",
            size=18,
            color=(255, 255, 255, 255)
            if not object.get("black", False)
            else (0, 0, 0, 255),
        )


def prepare_level_completed_text():
    duck_x = ui.WINDOW_WIDTH / 2
    y_center = ui.WINDOW_HEIGHT / 2
    y_1, y_2, y_3 = y_center + 50, y_center, y_center - 50
    prepare_text("Level completed!", duck_x, y_1, size=40)
    prepare_text("Press R to restart", duck_x, y_2, size=30)
    prepare_text("Press Enter to continue and save", duck_x, y_3, size=30)


def prepare_level_failed_text():
    duck_x = ui.WINDOW_WIDTH / 2
    y_center = ui.WINDOW_HEIGHT / 2
    y_1, y_2 = y_center + 50, y_center - 50
    prepare_text("Level failed!", duck_x, y_1, size=40)
    prepare_text("Press Enter or R to restart", duck_x, y_2, size=30)


def get_nearby_objects(x, y):
    check_range = 2 * ui.SPRITE_WIDTH
    return [
        obstacle
        for obstacle in level["objects"]
        if abs(obstacle["x"] * ui.WINDOW_RESIZE_SCALE - x) < check_range
        or abs(obstacle["y"] * ui.WINDOW_RESIZE_SCALE - y) < check_range
    ]
