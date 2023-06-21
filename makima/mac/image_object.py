from makima.mac.utils.mouse import left_mouse_single_click_event, right_mouse_single_click_event, \
    left_mouse_double_click_event


class ImageObject:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def click(self):
        print(self.x)
        left_mouse_single_click_event(self.x, self.y)

    def right_click(self):
        right_mouse_single_click_event(self.x, self.y)

    def double_click(self):
        left_mouse_double_click_event(self.x, self.y)

    def drag_to(self, x2, y2, smooth=True):
        self._mouse.drag(self.x, self.y, x2, y2, smooth)
