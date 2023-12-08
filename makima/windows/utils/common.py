import ctypes
import time
from ctypes import *
from ctypes import wintypes
from ctypes.wintypes import HWND, CHAR, LPSTR

from makima.windows.utils.keyboard import WinKeyboard


class WinCommon:
    def get_window_title(self,hwnd):
        """Get native window title."""
        cb = windll.user32.GetWindowTextLengthW(hwnd) + 1
        title = create_unicode_buffer(cb)
        windll.user32.GetWindowTextW(hwnd, title, cb)
        return title.value


    def get_window_class_name(self,hwnd):
        _GetClassNameA = windll.user32.GetClassNameA
        _GetClassNameA.argtypes = [HWND, LPSTR, ctypes.c_int]
        _GetClassNameA.restype = ctypes.c_int

        nMaxCount = 0x1000
        dwCharSize = sizeof(CHAR)
        while 1:
            lpClassName = create_string_buffer(nMaxCount)
            nCount = _GetClassNameA(hwnd, lpClassName, nMaxCount)
            if nCount == 0:
                raise WinError()
            if nCount < nMaxCount - dwCharSize:
                break
            nMaxCount += 0x1000
        return str(lpClassName.value)

    def find_window_by_wait(self, name, class_name=None, fuzzy_match=True):
        while time.time() < time_started_sec + timeout / 1000.0:
            result = find_windows(name, class_name, fuzzy_match)
            if len(result)>0:
                finish_time = time.time() - time_started_sec
                # print("Found element in {} s".format(finish_time))
                return result
            error = "Can't find window" % (timeout / 1000.0, query_method, query_string)
            raise TimeoutError(error)

    def find_windows(self,name, class_name=None, fuzzy_match=True):
        """
        Windows Platform find windows
        :param class_name:
        :param name is windows name and class_name is unique one
        return hwnd list
        """
        WNDENUMPROC = WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        hwnd_list = []

        def EnumWindowsProc(hwnd, lParam):
            length = user32.GetWindowTextLengthW(hwnd) + 1
            buffer = create_unicode_buffer(length)
            user32.GetWindowTextW(hwnd, buffer, length)
            if fuzzy_match:
                if buffer.value in name and user32.IsWindowVisible(hwnd):
                    if class_name is not None:
                        if "b'%s'" % class_name == self.get_window_class_name(hwnd):
                            hwnd_list.append(hwnd)
                    else:
                        hwnd_list.append(hwnd)
            else:
                if buffer.value == name and user32.IsWindowVisible(hwnd):
                    if class_name is not None:
                        if "b'%s'" % class_name == self.get_window_class_name(hwnd):
                            hwnd_list.append(hwnd)
                    else:
                        hwnd_list.append(hwnd)
            return True

        user32 = windll.LoadLibrary("user32.dll")
        user32.EnumWindows(WNDENUMPROC(EnumWindowsProc), 0)
        return hwnd_list


    def set_focus_window(self,hwnd):
        """Set windows front to desktop"""
        user32 = windll.LoadLibrary("user32.dll")
        if user32.IsIconic(hwnd):
            user32.ShowWindow(hwnd, 9)
        user32.SetForegroundWindow(hwnd)


    def show_windows(self,hwnd, cmd_show):
        """ Maxinum or Mininum windows
            SW_HIDE = 0
            SW_SHOWNORMAL = 1
            SW_SHOWMINIMIZED = 2
            SW_SHOWMAXIMIZED = 3
            SW_SHOWNOACTIVATE = 4
            SW_SHOW = 5
            SW_MINIMIZE = 6
            SW_SHOWMINNOACTIVE = 7
            SW_SHOWNA = 8
            SW_RESTORE = 9
            SW_SHOWDEFAULT = 10
        """

        user32 = windll.LoadLibrary("user32.dll")
        user32.ShowWindow(hwnd, cmd_show)

    def open_app_by_name(self,app_name):
        """
        Windows Platform open app using element click from task search bar.
        :param app_name is text input by search bar
        Note: must ensure search bar opened.
        """
        win_keyboard = WinKeyboard()
        win_keyboard.send(win_keyboard.codes.LEFT_WIN)
        win_keyboard.copy_text(app_name)
        time.sleep(1)
        win_keyboard.send(win_keyboard.codes.CONTROL.modify(win_keyboard.codes.KEY_V), delay=1)
        time.sleep(1)
        win_keyboard.send(win_keyboard.codes.RETURN)
        time.sleep(2)
