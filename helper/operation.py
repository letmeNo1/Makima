import pythoncom

from windows.ui_element import WinUIElement


def initialize_app_ref_for_win(obj_handle):
    return WinUIElement(obj_handle, 0)


