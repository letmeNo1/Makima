import Cocoa
import Quartz
from makima.mac.call_mac_api.KeyCodes import KeyCodes

from makima.mac.call_mac_api.call_app_kit import  get_app_by_name

from makima.mac.call_mac_api.call_app_kit import set_paste_board
from makima.mac.utils.keyboard import MacKeyBoard
from makima.mac.utils.mouse import MacMouse




class MacCommon:
    def input_text(self, x, y, text):
        set_paste_board(text)
        MacMouse().left_mouse_single_click_event(x, y)
        MacKeyBoard().combination_key_operation(KeyCodes.kVK_ANSI_V, Quartz.kCGEventFlagMaskCommand)

    def clear(self, x, y):
        MacMouse().left_mouse_single_click_event(x, y)
        MacKeyBoard().combination_key_operation(KeyCodes.kVK_ANSI_A, Quartz.kCGEventFlagMaskCommand)
        MacKeyBoard().combination_key_operation(KeyCodes.kVK_Delete)

    def active_window(self, name):
        running_app = get_app_by_name(name)
        running_app.activateWithOptions_(Cocoa.NSApplicationActivateIgnoringOtherApps)

    def is_finished_launching(self, name):
        running_app = get_app_by_name(name)
        return running_app.isFinishedLaunching()
