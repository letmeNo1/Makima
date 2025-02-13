from makima.windows.ui_element import WinUIElement, get_uiautomation
from makima.windows.utils.common import WinCommon



class Init_App_Ref_For_Win:
    def __call__(self, window_name=None, timeout=10, **query) -> WinUIElement:
        keys = query.keys()
        if "hwnd" in keys:
            hwnd_obj = query.get("hwnd")
            return WinUIElement(get_uiautomation().ElementFromHandle(hwnd_obj.hwnd))

        win_common = WinCommon()
        hwnd_obj = win_common.find_window_by_wait(timeout, **query)
        return WinUIElement(get_uiautomation().ElementFromHandle(hwnd_obj.hwnd),hwnd_obj.hwnd)

    def get_root(self) -> WinUIElement:
        return WinUIElement(get_uiautomation().GetRootElement())