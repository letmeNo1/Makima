import Cocoa
import Quartz

from makima.mac.call_mac_api.KeyCodes import KeyCodes
from makima.mac.call_mac_api.call_app_kit import set_paste_board, get_app_by_name
from makima.mac.utils.keyboard import combination_key_operation
from makima.mac.utils.mouse import left_mouse_single_click_event


def type(x, y, input_text):
    set_paste_board(input_text)
    left_mouse_single_click_event(x, y)
    combination_key_operation(KeyCodes.kVK_ANSI_V, Quartz.kCGEventFlagMaskCommand)


def clear(x, y):
    left_mouse_single_click_event(x, y)
    combination_key_operation(KeyCodes.kVK_ANSI_A, Quartz.kCGEventFlagMaskCommand)
    combination_key_operation(KeyCodes.kVK_Delete)


def active_window(name):
    running_app = get_app_by_name(name)
    running_app.activateWithOptions_(Cocoa.NSApplicationActivateIgnoringOtherApps)


def is_finished_launching(name):
    running_app = get_app_by_name(name)
    return running_app.isFinishedLaunching()
