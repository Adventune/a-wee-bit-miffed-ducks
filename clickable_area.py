class ClickableArea:
    x = 0
    y = 0
    x_2 = 0
    y_2 = 0
    text_anchor_x = None
    text_anchor_y = None

    def __init__(self, x, y, x_2, y_2, onclick=None, text_anchor_x=None, text_anchor_y=None):
        self.x = x
        self.y = y
        self.x_2 = x_2
        self.y_2 = y_2
        self.onclick = onclick
        self.text_anchor_x = text_anchor_x
        self.text_anchor_y = text_anchor_y

    def is_within_bounds(self, click_x, click_y):
        if self.text_anchor_x is None:
            return self.x <= click_x <= self.x_2 and self.y <= click_y <= self.y_2
        else:
            y_corrected = self.y
            x_corrected = self.x
            match self.text_anchor_x:
                case "center":
                    x_corrected -= (self.x_2 - self.x) / 2
                case "right":
                    x_corrected -= (self.x_2 - self.x)
            match self.text_anchor_y:
                case "center":
                    y_corrected -= (self.y_2 - self.y) / 2
                case "top":
                    y_corrected -= (self.y_2 - self.y)
            return x_corrected <= click_x <= self.x_2 and y_corrected <= click_y <= self.y_2

    def onclick(self):
        pass
