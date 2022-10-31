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

