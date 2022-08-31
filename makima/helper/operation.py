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


def GetRootElement():
    return WinUIElement(_IUIAutomation.GetRootElement())


def find_windows(name):
    for window in WinUIElement(_IUIAutomation.GetRootElement()).get_acc_children_elements():
        if window.get_acc_name == name:
            return window
    return None
