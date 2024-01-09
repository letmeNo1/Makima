from apollo_makima.windows.utils.mouse import WinMouse


class ImageObject:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    _mouse = WinMouse()

    def click(self):
        print(self.x)
        self._mouse.click(self.x, self.y)

    def right_click(self):
        self._mouse.click(self.x, self.y, self._mouse.RIGHT_BUTTON)

    def double_click(self):
        self._mouse.double_click(self.x, self.y)

    def drag_to(self, x2, y2, smooth=True):
        self._mouse.drag(self.x, self.y, x2, y2, smooth)
