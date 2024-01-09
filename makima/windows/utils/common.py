import ctypes
import re
import time
from ctypes import *
from ctypes import wintypes
from ctypes.wintypes import HWND, CHAR, LPSTR

from apollo_makima.windows.utils.keyboard import WinKeyboard

from apollo_makima.windows.utils.hwnd import HWND_OBJ
from typing import List


class WinCommon:
    def __get_window_class_name(self, hwnd):
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

    def find_window_by_wait(self, name=None, timeout=5, **kwargs):
        time_started_sec = time.time()
        while time.time() < time_started_sec + timeout:
            result = self.find_windows(name, **kwargs)
            if len(result) > 0:
                return result
        error = "Can't find window"
        raise TimeoutError(error)

    def find_windows(self, name=None, **query) -> List[HWND_OBJ]:
        """
        Windows Platform find windows
        :param class_name:
        :param name is windows name and class_name is unique one
        return hwnd list
        """
        WNDENUMPROC = WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        hwnd_list = []
        keys = query.keys()
        use_class_name = "class_name" in keys
        use_re = "name_matches" in keys
        use_contains = "name_contains" in keys
        no_use_any = name is not None
        use_hwnd = "hwnd" in keys
        if use_class_name:
            class_name = query.get("class_name")

        if no_use_any:
            name = name

        elif use_contains:
            name = query.get("name_contains")

        elif use_re:
            name = query.get("name_matches")

        elif use_hwnd:
            name = query.get("hwnd").get_window_title
        else:
            raise ValueError("Unsupported query")

        def EnumWindowsProc(hwnd, lParam):
            length = user32.GetWindowTextLengthW(hwnd) + 1
            buffer = create_unicode_buffer(length)
            user32.GetWindowTextW(hwnd, buffer, length)

            if no_use_any and buffer.value == name and user32.IsWindowVisible(hwnd):

                if use_class_name:
                    if "b'%s'" % class_name == self.__get_window_class_name(hwnd):
                        hwnd_list.append(HWND_OBJ(hwnd))
                else:
                    hwnd_list.append(HWND_OBJ(hwnd))
            elif use_contains and name in str(buffer.value) and user32.IsWindowVisible(hwnd):
                if use_class_name:
                    if "b'%s'" % class_name == self.__get_window_class_name(hwnd):
                        hwnd_list.append(HWND_OBJ(hwnd))
                else:
                    hwnd_list.append(HWND_OBJ(hwnd))
            elif use_re and re.search(name, buffer.value) is not None and user32.IsWindowVisible(hwnd):
                if use_class_name:
                    if "b'%s'" % class_name == self.__get_window_class_name(hwnd):
                        hwnd_list.append(HWND_OBJ(hwnd))
                else:
                    hwnd_list.append(HWND_OBJ(hwnd))
            return True

        user32 = windll.LoadLibrary("user32.dll")
        user32.EnumWindows(WNDENUMPROC(EnumWindowsProc), 0)
        return hwnd_list

    def open_app_by_name(self, app_name):
        """
        Windows Platform open app using element click from task search bar.
        :param app_name is text input by search bar
        Note: must ensure search bar opened.
        """
        win_keyboard = WinKeyboard()
        win_keyboard.send_keys(win_keyboard.codes.LEFT_WIN)
        win_keyboard.copy_text(app_name)
        time.sleep(1)
        win_keyboard.send_keys(win_keyboard.codes.CONTROL, win_keyboard.codes.KEY_V, delay=1)
        time.sleep(1)
        win_keyboard.send_keys(win_keyboard.codes.RETURN)
        time.sleep(2)
