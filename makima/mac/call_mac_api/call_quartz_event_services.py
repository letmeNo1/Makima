import time

import Quartz


def mouse_move_event(x, y):
    event = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (x, y), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)


def scroll_wheel_event(x, y):
    event = Quartz.CGEventCreateScrollWheelEvent(None, Quartz.kCGScrollEventUnitLine, 2, x, y)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)


def left_mouse_move_event(x, y):
    mouse_move_event(x, y)


def left_mouse_click_event(x, y, click_count):
    event = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDown, (x, y), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
    Quartz.CGEventSetIntegerValueField(event, Quartz.kCGMouseEventClickState, click_count)
    Quartz.CGEventSetType(event, Quartz.kCGEventLeftMouseUp)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)


def right_mouse_click_event(x, y, click_count):
    event = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventRightMouseDown, (x, y), Quartz.kCGMouseButtonRight)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
    Quartz.CGEventSetIntegerValueField(event, Quartz.kCGMouseEventClickState, click_count)
    Quartz.CGEventSetType(event, Quartz.kCGEventRightMouseUp)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)


def mouse_long_press_event(x, y, duration):
    event = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDown, (x, y), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
    time.sleep(duration)
    Quartz.CGEventSetType(event, Quartz.kCGEventLeftMouseUp)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)


def left_mouse_dragged_event(x, y, x2, y2, duration):
    event = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDown, (x, y), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
    event2 = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDragged, (x2, y2), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event2)
    time.sleep(duration)
    Quartz.CGEventSetType(event, Quartz.kCGEventLeftMouseUp)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
