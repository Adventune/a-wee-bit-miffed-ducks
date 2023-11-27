class Scene:
    def __init__(
        self,
        draw_handler=None,
        interval_handler=None,
        drag_handler=None,
        mouse_handler=None,
        release_handler=None,
        keyboard_handler=None,
        init=None,
    ):
        if draw_handler is not None:
            self.draw_handler = draw_handler
        if interval_handler is not None:
            self.interval_handler = interval_handler
        if drag_handler is not None:
            self.drag_handler = drag_handler
        if mouse_handler is not None:
            self.mouse_handler = mouse_handler
        if release_handler is not None:
            self.release_handler = release_handler
        if keyboard_handler is not None:
            self.keyboard_handler = keyboard_handler
        if init is not None:
            self.init = init

    def init(self):
        pass

    def draw_handler(self):
        pass

    def interval_handler(self, delta):
        pass

    def drag_handler(self, x, y, dx, dy, button, modifiers):
        pass

    def mouse_handler(self, x, y, button, modifiers):
        pass

    def release_handler(self, x, y, button, modifiers):
        pass

    def keyboard_handler(self, symbol, modifiers):
        pass
