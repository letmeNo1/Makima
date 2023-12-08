from makima.windows.ui_element import WinUIElement, _IUIAutomation


class Init_App_Ref_For_Win:
    def __call__(self, name, class_name=None, fuzzy_match=True) -> WinUIElement:
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
