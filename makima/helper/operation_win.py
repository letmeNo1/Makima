from makima.windows.ui_element import WinUIElement, _IUIAutomation


def initialize_app_ref_for_win(name, class_name=None, fuzzy_match=False):
    for window in WinUIElement(_IUIAutomation.GetRootElement()).get_acc_children_elements():
        if fuzzy_match:
            if class_name is not None:
                if name in window.get_acc_name and window.get_class_name == class_name:
                    return window
            else:
                if name in window.get_acc_name:
                    return window
        else:
            if class_name is not None:
                if window.get_acc_name == name and window.get_class_name == class_name:
                    return window
            else:
                if window.get_acc_name == name:
                    return window
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
