import ctypes
import re
from ctypes import *
from ctypes import wintypes
from ctypes.wintypes import HWND, CHAR, LPSTR



def convert_wildcard_to_regex(wildcard):
    """
    Converts wildcard to regex.

    :param str wildcard: wildcard.
    :rtype: str
    :return: regex pattern.
    """
    regex = re.escape(wildcard)
    regex = regex.replace(r'\?', r'[\s\S]{1}')
    regex = regex.replace(r'\*', r'[\s\S]*')

    return '^%s$' % regex


def replace_inappropriate_symbols(text):
    """
    Replaces inappropriate symbols e.g. \xa0 (non-breaking space) to
    normal space.

    :param str text: text in which symbols should be replaced.
    :rtype: str
    :return: processed text.
    """
    replace_pairs = [(u'\xa0', ' '),
                     (u'\u2014', '-')]

    for from_, to_ in replace_pairs:
        text = text.replace(from_, to_)

    return text


def verify_xy_coordinates(x, y):
    """
    Verifies that x and y is instance of int otherwise raises exception.

    :param x: x variable.
    :param y: y variable.
    """
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise Exception(
            'x and y arguments should hold int coordinates.')


def verify_mouse_button_name(button_name, supported_names):
    """
    Verifies that button name is supported otherwise raises exception.

    :param str button_name: button name.
    :param list[str] supported_names: supported button names.
    """
    if button_name not in supported_names:
        raise Exception(
            'Button name should be one of supported %s.' %
            repr(supported_names))


def get_window_title(hwnd):
    """Get native window title."""
    cb = windll.user32.GetWindowTextLengthW(hwnd) + 1
    title = create_unicode_buffer(cb)
    windll.user32.GetWindowTextW(hwnd, title, cb)
    return title.value


def get_window_class_name(hwnd):
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


def find_windows(name, class_name=None):
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
        if buffer.value == name and user32.IsWindowVisible(hwnd):
            if class_name is not None:
                if "b'%s'" % class_name == get_window_class_name(hwnd):
                    hwnd_list.append(hwnd)
            else:
                hwnd_list.append(hwnd)
        return True

    user32 = windll.LoadLibrary("user32.dll")
    user32.EnumWindows(WNDENUMPROC(EnumWindowsProc), 0)
    return hwnd_list


def set_focus_window(hwnd):
    """Set windows front to desktop"""
    user32 = windll.LoadLibrary("user32.dll")
    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, 9)
    user32.SetForegroundWindow(hwnd)


def show_windows(hwnd, cmd_show):
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
