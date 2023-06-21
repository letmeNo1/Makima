from apollo.makima_for_jdo.mac.call_mac_api.call_quartz_event_services import *

from makima.mac.call_mac_api.call_quartz_event_services import *


def left_mouse_move_event(x, y):
    mouse_move_event(x, y)


def left_mouse_single_click_event(x, y):
    left_mouse_click_event(x, y, 1)


def left_mouse_double_click_event(x, y):
    left_mouse_click_event(x, y, 2)


def right_mouse_single_click_event(x, y):
    right_mouse_click_event(x, y, 1)


def right_mouse_double_click_event(x, y):
    right_mouse_click_event(x, y, 2)


def scroll_wheel(distance):
    scroll_wheel_event(distance)


def drag(x1, y1, x2, y2):
    mouse_long_press_event(x1, y1)
    left_mouse_move_event(x2, y2)
    mouse_long_release_event(x2, y2)
