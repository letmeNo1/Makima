import ctypes
from ctypes import *
from ctypes.wintypes import HWND, CHAR, LPSTR


class HWND_OBJ:
    def __init__(self, hwnd_id):
        self.hwnd_id = hwnd_id

    @property
    def get_window_title(self):
        """Get native window title."""
        cb = windll.user32.GetWindowTextLengthW(self.hwnd_id) + 1
        title = create_unicode_buffer(cb)
        windll.user32.GetWindowTextW(self.hwnd_id, title, cb)
        return title.value

    @property
    def get_window_class_name(self):
        _GetClassNameA = windll.user32.GetClassNameA
        _GetClassNameA.argtypes = [HWND, LPSTR, ctypes.c_int]
        _GetClassNameA.restype = ctypes.c_int

        nMaxCount = 0x1000
        dwCharSize = sizeof(CHAR)
        while 1:
            lpClassName = create_string_buffer(nMaxCount)
            nCount = _GetClassNameA(self.hwnd_id, lpClassName, nMaxCount)
            if nCount == 0:
                raise WinError()
            if nCount < nMaxCount - dwCharSize:
                break
            nMaxCount += 0x1000
        return str(lpClassName.value)

    def focus_window(self):
        """Set windows front to desktop"""
        user32 = windll.LoadLibrary("user32.dll")
        if user32.IsIconic(self.hwnd_id):
            user32.ShowWindow(self.hwnd_id, 9)
        user32.SetForegroundWindow(self.hwnd_id)

    def show_window(self, cmd_show):
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
        user32.ShowWindow(self.hwnd_id, cmd_show)
