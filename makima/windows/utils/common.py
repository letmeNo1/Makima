import ctypes
import re
import time
from ctypes import *
from ctypes import wintypes
from ctypes.wintypes import HWND, CHAR, LPSTR, RECT
import pygetwindow as gw

import _ctypes
import comtypes
from makima.windows.utils.keyboard import WinKeyboard
from makima.windows.utils.hwnd import HWND_OBJ
from loguru import logger


class WinCommon:
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    def __get_window_name(self, hwnd):
        """Returns the window title as a string."""
        textLenInCharacters = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        stringBuffer = ctypes.create_unicode_buffer(
            textLenInCharacters + 1)  # +1 for the \0 at the end of the null-terminated string.
        ctypes.windll.user32.GetWindowTextW(hwnd, stringBuffer, textLenInCharacters + 1)
        # TODO it's ambiguous if an error happened or the title text is just empty. Look into this later.
        return stringBuffer.value

    def __get_window_class_name(self, hwnd):
        _GetClassNameA = self.user32.GetClassNameA
        _GetClassNameA.argtypes = [HWND, LPSTR, ctypes.c_int]
        _GetClassNameA.restype = ctypes.c_int

        nMaxCount = 0x1000
        dwCharSize = sizeof(CHAR)
        while 1:
            lpClassName = ctypes.create_string_buffer(nMaxCount)
            nCount = _GetClassNameA(hwnd, lpClassName, nMaxCount)
            if nCount == 0:
                raise ctypes.WinError()
            if nCount < nMaxCount - dwCharSize:
                break
            nMaxCount += 0x1000
        return str(lpClassName.value.decode())

    def __get_window_size(self, hwnd):
        rect = wintypes.RECT()
        if not self.user32.GetWindowRect(hwnd, ctypes.byref(rect)):
            raise ctypes.WinError()
        width = rect.right - rect.left
        height = rect.bottom - rect.top
        return width, height

    def __get_window_attribute(self, hwnd, attribute):
        if attribute == "name":
            return self.__get_window_name(hwnd)
        elif attribute == "class_name":
            return self.__get_window_class_name(hwnd)
        elif attribute == "area_ratio":
            screen_width = self.user32.GetSystemMetrics(0)
            screen_height = self.user32.GetSystemMetrics(1)
            screen_area = screen_width * screen_height
            width, height = self.__get_window_size(hwnd)
            window_area = width * height
            return window_area / screen_area
        else:
            raise ValueError(f"Unsupported attribute: {attribute}")

    def __assert_ui_element(self, hwnd, **query):
        rst = []
        for query_method, query_string in query.items():
            attribute = query_method.replace("_contains", "").replace("_matches", "")
            if "contains" in query_method:
                element_attr = self.__get_window_attribute(hwnd, attribute)
                rst.append(str(element_attr).find(query_string) != -1)
            elif "matches" in query_method:
                element_attr = self.__get_window_attribute(hwnd, attribute)
                rst.append(re.search(query_string, str(element_attr)) is not None)
            elif "min" in query_method or "max" in query_method:
                element_attr = self.__get_window_attribute(hwnd, "area_ratio")
                if "min" in query_method:
                    rst.append(element_attr >= float(query_string))
                if "max" in query_method:
                    rst.append(element_attr <= float(query_string))
            else:
                element_attr = self.__get_window_attribute(hwnd, attribute)
                rst.append(element_attr == query_string)
        return all(rst)

    def print_windows(self,filter =None):
        windows = gw.getAllWindows()
        for window in windows:
            hwnd = window._hWnd
            buffer = ctypes.create_unicode_buffer(255)
            self.user32.GetWindowTextW(hwnd, buffer, 255)
            class_name = self.__get_window_class_name(hwnd)
            if filter:
                if filter in str(buffer.value):
                    logger.debug(f"Window Handle: {hwnd}, Title: {buffer.value}, Class Name: {class_name}")
            else:
                logger.debug(f"Window Handle: {hwnd}, Title: {buffer.value}, Class Name: {class_name}")

    def __get_ui_automation_objec_class_name(self, hwnd):
        def get_uiautomation():
            try:
                _IUIAutomation = comtypes.CoCreateInstance(comtypes.gen.UIAutomationClient.CUIAutomation._reg_clsid_,
                                                           interface=comtypes.gen.UIAutomationClient.IUIAutomation,
                                                           clsctx=comtypes.CLSCTX_INPROC_SERVER)
            except _ctypes.COMError as E:
                print("UIAutomationClient is not installed")
                return None
            except WindowsError as E:
                print("UIAutomationClient is not installed")
                return None
            except Exception as E:
                print("UIAutomationClient is not installed")
                return None
            return _IUIAutomation
        return getattr(get_uiautomation().ElementFromHandle(hwnd), "CurrentClassName")

    def find_window_by_wait(self, timeout=5, **kwargs):
        time_started_sec = time.time()
        while time.time() < time_started_sec + timeout:
            result = self.find_windows(**kwargs)
            if len(result) > 0:
                if len(result) > 1:
                    error = f"Found more than one window: {len(result)} windows found."
                    for hwnd_obj in result:
                        hwnd = hwnd_obj.hwnd
                        error += f"\nWindow Handle: {hwnd}, title: {hwnd_obj.get_window_title}, class name: {hwnd_obj.get_window_class_name}"
                    raise ValueError(error)
                else:
                    return result[0]
        import json
        error = f"Can't find window by {json.dumps(kwargs)}"
        self.print_windows()
        raise TimeoutError(error)

    def __get_all_window_handles(self):
        hwnd_list = []

        # 枚举窗口回调函数
        def enum_windows_proc(hwnd, lParam):
            hwnd_list.append(hwnd)
            return True

        # 调用 EnumWindows 函数
        self.user32.EnumWindows(self.WNDENUMPROC(enum_windows_proc), 0)
        return hwnd_list

    def open_app_by_name(self, app_name):
        win_keyboard = WinKeyboard()
        win_keyboard.send_keys(win_keyboard.codes.LEFT_WIN)
        win_keyboard.copy_text(app_name)
        time.sleep(1)
        win_keyboard.send_keys(win_keyboard.codes.CONTROL, win_keyboard.codes.KEY_V, delay=1)
        time.sleep(1)
        win_keyboard.send_keys(win_keyboard.codes.RETURN)
        time.sleep(2)

    def find_windows(self, **query):
        windows = gw.getAllWindows()
        hwnd_list = []
        for window in windows:
            hwnd = window._hWnd
            if self.__assert_ui_element(hwnd, **query):
                hwnd_list.append(HWND_OBJ(hwnd))
        return hwnd_list

    def get_foreground_window(self):
        hWnd = self.user32.GetForegroundWindow()
        length = self.user32.GetWindowTextLengthW(hWnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        self.user32.GetWindowTextW(hWnd, buff, length + 1)
        return HWND_OBJ(hWnd)