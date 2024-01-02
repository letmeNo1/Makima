import Cocoa
import Quartz
from makima.mac.utils.keyboard import MacKeyBoard
from makima.mac.utils.mouse import MacMouse

from makima.mac.call_mac_api.call_app_kit import CallAppKit


class MacCommon(CallAppKit):
    def input_text(self, x, y, text):
        self.set_paste_board(text)
        MacMouse().left_mouse_single_click_event(x, y)
        MacKeyBoard().send_keys(MacKeyBoard().codes.KEY_V, MacKeyBoard().mask_codes.COMMAND)

    def clear(self, x, y):
        MacMouse().left_mouse_single_click_event(x, y)
        MacKeyBoard().send_keys(MacKeyBoard().codes.KEY_A, MacKeyBoard().mask_codes.COMMAND)
        MacKeyBoard().send_keys(MacKeyBoard().codes.DELETE)

    def active_window(self, name):
        running_app = self.get_app_by_name(name)
        running_app.activateWithOptions_(Cocoa.NSApplicationActivateIgnoringOtherApps)

    def hide_window(self, name):
        running_app = self.get_app_by_name(name)
        running_app.hide()

    def unhide_window(self, name):
        running_app = self.get_app_by_name(name)
        running_app.unhide()

    def is_finished_launching(self, name):
        running_app = self.get_app_by_name(name)
        return running_app.isFinishedLaunching()
