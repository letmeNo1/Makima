import ctypes
from ctypes import *
import os, platform, time
import traceback
from ctypes import wintypes
from ctypes.wintypes import HWND, LPSTR, CHAR

# Launch RCT
# win_keyboard.send(win_keyboard.codes.LEFT_WIN)
# win_keyboard.copy_text("RCT UWP")
# win_keyboard.send(win_keyboard.codes.CONTROL.modify(win_keyboard.codes.KEY_V), delay=0)
# win_keyboard.send(win_keyboard.codes.RETURN)
#
# time.sleep(3)
# hWnd = ctypes.windll.user32.FindWindowW(NULL, "RCT UWP")
# calculator = initialize_app_ref_for_win(hWnd)
# format_list = ["1920 x 1080 @ 30fps YUY2", "1920 x 1080 @ 27fps YUY2", "1920 x 1080 @ 24fps YUY2",
#                "1920 x 1080 @ 15fps "
#                "YUY2",
#                "640 x 360 @ 30fps YUY2", "640 x 360 @ 27fps YUY2", "640 x 360 @ 24fps YUY2", "640 x 360 @ 15fps YUY2",
#                "960 x 540 @ 30fps YUY2", "960 x 540 @ 27fps YUY2", "960 x 540 @ 24fps YUY2", "960 x 540 @ 15fps YUY2",
#                ]
#
# # ctypes.windll.user32.SetForegroundWindow(hWnd)
# print(calculator.find_element_by_wait(automation_id="CameraList", class_name="ComboBox").get_class_name)

# ctypes.windll.user32.SetForegroundWindow(hWnd)
# calculator.find_element_by_wait(acc_name="Jabra PanaCast 20").click()
#
# calculator.find_element_by_wait(automation_id="FormatList").click()
#
# print(calculator.find_element_by_wait(5000, class_name="ComboBoxItem"))

# print(calculator.find_element_by_name_by_wait("3840 x 2160 @ 15fps MJPG"))
# print(_format + "'s FPS is " + FPS)

# calculator.release()
def get_window_class_name(hWnd):
    _GetClassNameA = windll.user32.GetClassNameA
    _GetClassNameA.argtypes = [HWND, LPSTR, ctypes.c_int]
    _GetClassNameA.restype = ctypes.c_int

    nMaxCount = 0x1000
    dwCharSize = sizeof(CHAR)
    while 1:
        lpClassName = ctypes.create_string_buffer(nMaxCount)
        nCount = _GetClassNameA(hWnd, lpClassName, nMaxCount)
        if nCount == 0:
            raise ctypes.WinError()
        if nCount < nMaxCount - dwCharSize:
            break
        nMaxCount += 0x1000
    return str(lpClassName.value)

WNDENUMPROC = WINFUNCTYPE(wintypes.BOOL,
                          wintypes.HWND,
                          wintypes.LPARAM)

def find_windows(name,class_name = None):
    hwnd_list =[]
    def EnumWindowsProc(hwnd, lParam):
        length = user32.GetWindowTextLengthW(hwnd) + 1
        buffer = create_unicode_buffer(length)
        user32.GetWindowTextW(hwnd, buffer, length)
        if buffer.value == name and user32.IsWindowVisible(hwnd):
            if class_name is not None:
                if class_name == GetClassNameA(hwnd):
                   hwnd_list.append(hwnd)
            else:
                   hwnd_list.append(hwnd)
        return True
    user32 = windll.LoadLibrary('user32.dll')
    user32.EnumWindows(WNDENUMPROC(EnumWindowsProc), 0)
    return hwnd_list


def set_foreground_window(hWnd):
    user32 = ctypes.windll.LoadLibrary('user32.dll')
    user32.SetForegroundWindow(hWnd)


set_foreground_window(find_windows("Zoom")[0])