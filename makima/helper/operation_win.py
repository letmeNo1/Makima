import psutil
from makima.mac.call_mac_api.call_app_server import get_app_ref_by_pid
from makima.mac.ui_element import MacUIElement
from makima.windows.ui_element import WinUIElement, _IUIAutomation


def initialize_app_ref_for_win(name, class_name=None):
    for window in WinUIElement(_IUIAutomation.GetRootElement()).get_acc_children_elements():
        if class_name is not None:
            if window.get_acc_name == name and window.get_class_name == class_name:
                return window
        else:
            if window.get_acc_name == name:
                return window
    return None


def initialize_app_ref_for_mac(name):
    pids = psutil.pids()
    for pid in pids:
        process = psutil.Process(pid)
        if name == process.name():
            app = MacUIElement(get_app_ref_by_pid(pid))
            return app
        else:
            return None


# Only for win
def GetRootElement():
    return WinUIElement(_IUIAutomation.GetRootElement())


# Only for win
def find_windows(name):
    for window in WinUIElement(_IUIAutomation.GetRootElement()).get_acc_children_elements():
        if window.get_acc_name == name:
            return window
    return None
