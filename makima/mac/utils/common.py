import time
import re
from typing import List
import Cocoa
import Quartz
from AppKit import NSScreen
from makima.mac.utils.keyboard import MacKeyBoard
from makima.mac.utils.mouse import MacMouse
from makima.mac.call_mac_api.call_app_kit import CallAppKit
from makima.mac.utils.window_obj import WindowOBJ
from loguru import logger

_window_type = {
    1: [Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID],
    2: [Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID]
}


class MacCommon(CallAppKit):
    def open_app_by_name(self, app_name):
        workspace = NSWorkspace.sharedWorkspace()
        app_path = workspace.fullPathForApplication_(app_name)
        if app_path:
            workspace.launchApplication_(app_path)
            print(f"{app_name} The application has started successfully！")
        else:
            print(f"Can't found {app_name}.")

    def input_text(self, text, x=None, y=None):
        self.set_paste_board(text)
        if x is not None:
            MacMouse().left_mouse_single_click_event(x, y)
        MacKeyBoard().send_keys(MacKeyBoard().codes.KEY_V, MacKeyBoard().mask_codes.COMMAND)

    def clear(self, x=None, y=None):
        if x is not None:
            MacMouse().left_mouse_single_click_event(x, y)
        MacKeyBoard().send_keys(MacKeyBoard().codes.KEY_A, MacKeyBoard().mask_codes.COMMAND)
        MacKeyBoard().send_keys(MacKeyBoard().codes.DELETE)

    def active_app(self, app_name):
        running_app = self.get_app_by_name(app_name)
        running_app.activateWithOptions_(Cocoa.NSApplicationActivateIgnoringOtherApps)

    def hide_app(self, app_name):
        running_app = self.get_app_by_name(app_name)
        running_app.hide()

    def unhide_app(self, app_name):
        running_app = self.get_app_by_name(app_name)
        running_app.unhide()

    def is_finished_launching(self, app_name):
        running_app = self.get_app_by_name(app_name)
        return running_app.isFinishedLaunching()

    def is_hide(self, app_name):
        running_app = self.get_app_by_name(app_name)
        return running_app.isHidden()

    def is_active(self, app_name):
        running_app = self.get_app_by_name(app_name)
        return running_app.isActive()

    def __assert_ui_window(self, window, **query):
        rst = []
        for query_method, query_string in query.items():
            if "name" in query_method:
                element_attr = window.get_window_title
            if "window_name" in query_method:
                element_attr = window.get_window_name
            if "pid" in query_method:
                query_string = int(query_string)
                element_attr = window.get_owner_pid
            if "contains" in query_method:
                rst.append(query_string in element_attr)
            elif "matches" in query_method:
                rst.append(re.search(query_string, element_attr) is not None)
            else:
                rst.append(element_attr == query_string)
        return all(rst)

    def _get_all_window_obj(self, window_type=1):
        window_list = Quartz.CGWindowListCopyWindowInfo(_window_type.get(window_type)[0],
                                                        _window_type.get(window_type)[1])
        return [WindowOBJ(window) for window in window_list]

    def get_all_window(self, window_type=1):
        window_list = Quartz.CGWindowListCopyWindowInfo(_window_type.get(window_type)[0],
                                                        _window_type.get(window_type)[1])
        return window_list

    def get_screen_size(self):
        screen = NSScreen.mainScreen()
        visible_frame = screen.visibleFrame()
        width = visible_frame.size.width
        height = visible_frame.size.height
        return width, height

    def find_window_by_wait(self, window_type=1, timeout=5, **query) -> WindowOBJ:
        time_started_sec = time.time()
        while time.time() < time_started_sec + timeout:
            result = self.find_windows(window_type, **query)
            if len(result) > 0:
                if len(result) > 1:
                    error = f"Found more than one window: {len(result)} windows found."
                    for window_obj in result:
                        pid = window_obj.get_owner_pid
                        error += f"\nWindow PID: {pid}, title: {window_obj.get_window_title}"
                    raise ValueError(error)
                else:
                    return result[0]
        import json
        error = f"Can't find window by {json.dumps(query)}"
        self.print_windows()
        raise TimeoutError(error)

    def find_windows(self, window_type=1, **query) -> List[WindowOBJ]:
        rst = []
        windows = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListExcludeDesktopElements | Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
        for win in windows:
            window_obj = WindowOBJ(win)
            if self.__assert_ui_window(window_obj, **query):
                rst.append(window_obj)
        return rst

    def print_windows(self, filter_window_name=None, window_type=1):
        """
        Prints information about all windows. If filter_window_name is provided, only windows with titles containing this string will be printed.

        Parameters:
        filter_window_name (str): Optional parameter used to filter window names. Only windows with titles containing this string will be printed.
        """
        windows = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListExcludeDesktopElements | Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
        for window in windows:
            window_obj = WindowOBJ(window)
            if filter_window_name:
                if filter_window_name in str(window_obj.get_window_title):
                    logger.debug(f"Window Pid: {window_obj.get_owner_pid},window title: {window_obj.get_window_title}, window_name: {window_obj.get_window_name}")
            else:
                logger.debug(f"Window Pid: {window_obj.get_owner_pid},window title: {window_obj.get_window_title}, window_name: {window_obj.get_window_name}")