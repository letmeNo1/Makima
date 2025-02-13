import time

from makima.mac.call_mac_api.call_quartz_event_services import *


class MacMouse:
    def left_mouse_move_event(self,x, y):
        mouse_move_event(x, y)

    def left_mouse_single_click_event(self,x, y):
        time.sleep(0.5)
        left_mouse_click_event(x, y, 1)

    def left_mouse_double_click_event(self,x, y):
        left_mouse_click_event(x, y, 2)

    def right_mouse_single_click_event(self,x, y):
        right_mouse_click_event(x, y, 1)

    def right_mouse_double_click_event(self,x, y):
        right_mouse_click_event(x, y, 2)

    def scroll_wheel(self,distance,x=None, y=None):
        if x is not None and y is not None:
            left_mouse_move_event(x, y)
        scroll_wheel_event(distance)