from makima.mac.utils.mouse import MacMouse


class ImageObject(MacMouse):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


    def click(self):
        self.left_mouse_single_click_event(self.x, self.y)

    def right_click(self):
        self.right_mouse_single_click_event(self.x, self.y)

    def double_click(self):
        self.left_mouse_double_click_event(self.x, self.y)
