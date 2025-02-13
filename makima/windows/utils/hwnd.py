import ctypes
from ctypes import *
from ctypes.wintypes import HWND, CHAR, LPSTR
from loguru import logger

class HWND_OBJ:
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.window_name = self.get_window_title

    @property
    def get_window_title(self):
        """Get native window title."""
        cb = windll.user32.GetWindowTextLengthW(self.hwnd) + 1
        title = create_unicode_buffer(cb)
        windll.user32.GetWindowTextW(self.hwnd, title, cb)
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
            nCount = _GetClassNameA(self.hwnd, lpClassName, nMaxCount)
            if nCount == 0:
                raise WinError()
            if nCount < nMaxCount - dwCharSize:
                break
            nMaxCount += 0x1000
        return str(lpClassName.value)

    def focus_window(self, flag=1):
        if flag == 0:
            from makima.helper.operation_win import Init_App_Ref_For_Win
            from makima.windows.utils.common import WinCommon

            if WinCommon().get_foreground_window() != self.window_name:
                makima = Init_App_Ref_For_Win()
                task_bar = makima(name="", class_name="Shell_TrayWnd")
                if task_bar.check_element_exist(acc_name_contains=self.window_name):
                    task_bar.ele(acc_name_contains=self.window_name).invoke()
            """Set windows front to desktop"""
            user32 = windll.LoadLibrary("user32.dll")
            if user32.IsIconic(self.hwnd):
                user32.ShowWindow(self.hwnd, 9)
            user32.SetForegroundWindow(self.hwnd)
        elif flag == 1:
            import pygetwindow as gw
            window = gw.getWindowsWithTitle(self.window_name)[0]
            try:
                window.activate()
            except gw.PyGetWindowException as e:
                # Handle specific PyGetWindowException
                if 'Error code from Windows: 0' in str(e):
                    logger.debug(f"Specific PyGetWindowException occurred: {e}")
            window.show()

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
        user32.ShowWindow(self.hwnd, cmd_show)
