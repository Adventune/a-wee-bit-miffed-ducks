"""
game_lib (originally "sweeperlib") - simple graphics and event library for minesweeper

@author: Mika Oja, University of Oulu

This library offers a handful of functions that students can use to implement
a graphical interface for a minesweeper game without having to study how an
entire user interface or game library works. It's a wrapper for Pyglet and
offers a small subset of its features through a simple interface made of
functions. Students who have deeper interest in the subject are encouraged to
look at Pyglet itself:

https://pyglet.readthedocs.io

"
This library is modified from the original "sweeperlib" to be suited for my particular
implementation of the game.
"
"""
import os
from typing import Any

import pyglet
from pyglet.gl import glEnable, GL_TEXTURE_2D
from clickable_area import ClickableArea

key = pyglet.window.key
mouse = pyglet.window.mouse

BACKGROUND = pyglet.graphics.OrderedGroup(0)
MIDDLEGROUND = pyglet.graphics.OrderedGroup(1)
FOREGROUND = pyglet.graphics.OrderedGroup(2)
SHADE = pyglet.graphics.OrderedGroup(3)
HELP_TEXT = pyglet.graphics.OrderedGroup(4)

# Variables required for drawing graphics are saved to this dictionary so that
# they can be easily accessed in all functions. A similar solution is
# recommended for your minesweeper in order to have the information required by
# handler functions available to them.

graphics: dict[str, Any] = { # Typed as any to avoid warnings
    "window": None,
    "background": None,
    "bg_color": None,
    "batch": None,
    "graphics": [],
    "images": {}
}

handlers = {
    "timeouts": [],
}

glEnable(GL_TEXTURE_2D)

pyglet.resource.add_font("fonts/junglefever/JUNGLEFE.TTF")
pyglet.font.load("Jungle Fever")


def load_sprites(path, levels_path):
    """
    Loads the necessary graphics for the duck game. This include the duck
    itself (size 40x40) and a sling that can be used as an atmospheric prop
    (size 80x150).
    
    :param str path: path to the sprites folder
    :param str levels_path: path to the level image folder
    """

    pyglet.resource.path = [path, levels_path]

    dir_list = os.listdir(path)
    for file in dir_list:
        if file.endswith(".png"):
            graphics["images"][file.split(".")[0]] = pyglet.resource.image(f"{path}/{file}")

    dir_list = os.listdir(levels_path)
    for file in dir_list:
        if file.endswith(".png"):
            level = file.split(".")[0]
            sprite_name = f"level_{level}_image"
            graphics["images"][sprite_name] = (
                pyglet.resource.image(f"{levels_path}/{file}"))


def create_window(width=800, height=600, bg_color=(240, 240, 240, 255)):
    """
    Creates a game window for displaying graphics. This function needs to be
    called before any other functions in this module can be used. By default
    creates a 800x600 pixel window with light grey background. These can be
    changed by providing optional arguments to the function.
    
    :param int width: window width
    :param int height: window height
    :param tuple bg_color: background color, tuple containing four values
                           (0-255, RGBA)
    """

    if graphics["window"] is None:
        graphics["window"] = pyglet.window.Window(width, height, resizable=True)
        graphics["bg_color"] = bg_color
        graphics["background"] = pyglet.sprite.Sprite(pyglet.resource.image("sprites/bg.png"))
        graphics["window"].set_visible(False)
        graphics["window"].on_close = close
    else:
        resize_window(width, height)


def resize_window(width, height):
    """
    Changes the window size while the program is running.

    :param int width: new window width
    :param int height: new window height
    """

    graphics["window"].set_size(width, height)
    graphics["background"] = pyglet.sprite.Sprite(
        pyglet.image.SolidColorImagePattern(graphics["bg_color"]).create_image(width, height)
    )


def set_mouse_handler(handler):
    """
    Sets a function that is used to handle mouse clicks. The handler function
    will be called whenever a mouse button is pressed down inside the game
    window. The handler must be a function that has four parameters: x, y, 
    button, and modifier keys. X and y are the mouse click's coordinates inside
    the window; button indicates which button was pressed (its possible values
    are MOUSE_LEFT, MOUSE_MIDDLE, and MOUSE_RIGHT). Modifier keys have been
    explained in the module documentation, and should not be needed in a basic
    implementation.
    
    In other words you need a function similar to this in your code:

    def mouse_handler(x, y, button, modifiers):
        # things happen

    and register it:

    game_lib.set_mouse_handler(mouse_handler)

    This way your program can receive mouse clicks from Pyglet.

    :param function handler: handler function for mouse clicks
    """

    if graphics["window"]:
        graphics["window"].on_mouse_press = handler
    else:
        print("Window hasn't been created!")


def set_mouse_move_handler(handler):
    """
    Sets a function that is used to handle mouse movement.
    The handler function will be called whenever the mouse cursor is moved
    The handler must be a function that has four parameters: x, y, dx, dy.

    :param function handler: handler function for mouse movement
    """

    if graphics["window"]:
        graphics["window"].on_mouse_motion = handler
    else:
        print("Window hasn't been created!")


def set_drag_handler(handler):
    """
    Sets a function that is used to handle mouse dragging. It is called
    periodically when the mouse cursor is moved while one of its buttons is
    held down. The handler must be a function with a total of six parameters:
    x, y, dx, dy, button, and modifier keys. Of these, x and y are the cursor's
    current position where as dx and dy indicate the change moved from the last
    position. Button indicates which button was pressed (its possible values
    are MOUSE_LEFT, MOUSE_MIDDLE, and MOUSE_RIGHT). Modifier keys have been
    explained in the module documentation, and should not be needed in a basic
    implementation.
    
    In other words you need a function similar to this in your code:
    
    def drag_handler(x, y, dx, dy, button, modifiers):
        # things happen
        
    and register it:

    game_lib.set_drag_handler(drag_handler)

    This way your program can receive mouse drag events from Pyglet.

    :param function handler: handler function for mouse clicks
    """

    if graphics["window"]:
        graphics["window"].on_mouse_drag = handler
    else:
        print("Window hasn't been created!")


def set_release_handler(handler):
    """
    Sets a function that is used when a mouse button is released. Typically
    needed if a program needs to do something after dragging an object. Accepts
    a handler similar to the mouse click handler. Define a function similar to
    this:
    
    Asettaa funktion, jota käytetään kun hiiren nappi vapautetaan.
    Tyypillisesti tarpeellinen jos raahauksen päätteeksi halutaan tehdä jotain.
    Käsittelijäksi kelpaa samanlainen funktion kuin 
    aseta_hiiri_kasittelija-funktiolle. Eli määrittele sopiva funktio:
    
    def release_handler(x, y, button, modifiers):
        # things happen
        
    and register it:

    game_lib.set_release_handler(release_handler)

    This way your program can receive mouse release events from Pyglet.

    :param function handler: handler function for mouse release
    """

    if graphics["window"]:
        graphics["window"].on_mouse_release = handler
    else:
        print("Window hasn't been created!")


def set_keyboard_handler(handler):
    """
    Sets a function that is for handling keyboard input. You won't need this
    unless you want to use the keyboard for something. The handler function
    must have two parameters: symbol and modifier keys. The symbol is a
    constant that's been defined in the pyglet.window.key module (e.g. 
    pyglet.window.key.A is the A key). Use the following import to access these
    constants conveniently:
    
    from pyglet.window import key

    With this you can use the key name to access key codes, e.g. key.A for A.
    Modifier keys are explained in this module's documentation.

    In order to use the keyboard you need to define a function like this:

    def keyboard_handler(symbol, modifiers):
        # things happen

    and register it:

    game_lib.set_keyboard_handler(keyboard_handler)

    :param function handler: handler function for key presses
    """

    if graphics["window"]:
        graphics["window"].on_key_press = handler
    else:
        print("Window hasn't been created!")


def set_draw_handler(handler):
    """
    Sets a function that is used for drawing the game's graphics - somewhat
    important. The handler is a function that doesn't have any parameters, and
    it should daw the window's contents by using the following functions:
    
    clear_window (clears away everything draw last iteration)
    draw_background (draws the background color)
    begin_sprite_draw (called before drawing the game tiles)
    prepare_sprite (prepares a sprite to be drawn)
    draw_sprites (draws all prepared sprites at once)
    draw_text (writes some text - optional)
    
    :param function handler: handler function for drawing
    """

    if graphics["window"]:
        graphics["window"].on_draw = handler
    else:
        print("Window hasn't been created!")


def set_interval_handler(handler, interval=1 / 60):
    """
    Sets a function that will be called periodically using the given interval.
    Used for e.g. animations, on-screen timers etc. The interval is given as
    seconds and is treated as a target - it will always have some variance in
    milliseconds. The actual time elapsed between function calls is given to
    the handler to its sole parameter. The handler must match:
    
    def interval_handler(elapsed):
        # something happens
        
    and is registered with

    game_lib.set_interval_handler(interval_handler, 1/60)

    The interval's default value translates to 60 FPS.

    :param function handler: handler to call periodically
    :param float interval: interval between calls, default 1/60
    """

    pyglet.clock.schedule_interval(handler, interval)
    handlers["timeouts"].append(handler)


def start():
    """
    Starts the game. You need to create a window and set handlers before
    calling this.
    """

    graphics["window"].set_visible(True)
    pyglet.app.run()


def close():
    """
    Closes the window and exits the game loop. You can use this to return from
    the game window back to a text-based terminal menu. Note that in order to
    restart the game after this, you need to create the window and set the
    handlers again.
    """

    for handler in handlers["timeouts"]:
        pyglet.clock.unschedule(handler)
    pyglet.app.exit()
    graphics["window"].set_visible(False)


def clear_window():
    """
    Clears away everything from the window.
    """

    graphics["window"].clear()


def draw_background():
    """
    Draws the window's background graphics (color). Pretty decent idea to call
    this before anything else, otherwise the bg color will cover everything.
    """

    graphics["background"].draw()


def begin_graphics_draw():
    """
    Starts the drawing of graphics (sprites and text) by initializing a batch where all
    graphics to be drawn are collected. Graphics are not drawn one by one because
    that is not particularly efficient. Instead, they are smartly collected to
    a batch that is then drawn in one go. In order for this to work, this
    function must be called before drawing the graphics themselves.
    """

    graphics["batch"] = pyglet.graphics.Batch()


def prepare_text(text, x, y, color=(255, 255, 255, 255), font="junglefever", size=32,
                 anchor_x="center", anchor_y="bottom", group=FOREGROUND, onclick=lambda: None):
    """
    Draws text on the screen. Can be used if you want to write something to
    the game window (e.g. counters or instructions). Default font is serif,
    size 32, color black. These can be altered by providing the function its
    optional arguments. The x and y coordinates define the bottom left corner
    of the text.
    
    Text, if any, should be drawn last.
    
    :param str text: string to display
    :param int x: bottom left x coordinate for the text
    :param int y: bottom left y coordinate for the text
    :param tuple color: color value, a tuple of four integers (RGBA)
    :param str font: name of the font family
    :param int size: fontin size as points
    :param str anchor_x: horizontal anchor point, "left", "center", or "right"
    :param str anchor_y: vertical anchor point, "bottom", "center", or "top"
    :param pyglet.graphics.OrderedGroup group: group to which the text belongs
    :param function onclick: function to call when the text is clicked
    """

    text_box = pyglet.text.Label(text, font_name=font,
                                 font_size=size, color=color, x=x, y=y,
                                 anchor_x=anchor_x, anchor_y=anchor_y,
                                 group=group, batch=graphics["batch"])

    graphics["graphics"].append(text_box)

    return ClickableArea(x, y, x + text_box.content_width, y + text_box.content_height,
                         onclick=onclick, text_anchor_x=anchor_x, text_anchor_y=anchor_y)


def prepare_sprite(key, x, y, group=FOREGROUND, scale=1, onclick=lambda: None):
    """
    Adds a sprite to be drawn into the batch. Therefore the begin_sprite_draw
    must have been called once before this function is called. The first
    argument defines which sprite to draw. Possible values are the numbers
    0 to 8 as strings, "x" for mines, "f" for flags, and " " for unopened
    tiles.
    
    You have to calculate the position of each tile. One tile sprite is always
    40x40 pixels.

    :param str key: key, used to select the sprite
    :param int x: bottom left x coordinate
    :param int y: bottom left y coordinate
    :param pyglet.graphics.OrderedGroup group: group to which the sprite belongs
    :param float scale: scale factor for the sprite
    :param function onclick: function to call when the sprite is clicked
    """

    sprite = pyglet.sprite.Sprite(
        graphics["images"][str(key).lower()],
        x, y,
        batch=graphics["batch"], group=group
    )

    sprite.scale = scale
    graphics["graphics"].append(sprite)

    return ClickableArea(x, y, x + sprite.width, y + sprite.height, onclick=onclick)


def draw_graphics():
    """
    Draws all prepared sprites from the batch in one go. Call this function
    when you have prepared all sprites to be drawn.
    """

    graphics["batch"].draw()
    graphics["graphics"].clear()


def set_scene(scene_name):
    """
    Sets the scene to be drawn. The scene name must match one of the scenes

    :param str scene_name: name of the scene to be drawn
    """
    from scenes.menu import MENU_SCENE  # Import here to avoid circular imports
    from scenes.levels import LEVELS_MENU_SCENE
    from scenes.game import GAME_SCENE
    from scenes.completed import COMPLETED_SCENE

    scenes = {
        "menu": MENU_SCENE,
        "levels": LEVELS_MENU_SCENE,
        "game": GAME_SCENE,
        "completed": COMPLETED_SCENE
    }

    scene = scenes[scene_name]

    set_draw_handler(scene.draw_handler)
    set_mouse_handler(scene.mouse_handler)
    set_interval_handler(scene.interval_handler, scene.interval)
    set_drag_handler(scene.drag_handler)
    set_release_handler(scene.release_handler)
    set_keyboard_handler(scene.keyboard_handler)

    return scene
