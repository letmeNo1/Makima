import re

from makima.windows.ui_element import WinUIElement, _IUIAutomation



class Init_App_Ref_For_Win:
    def __call__(self, name=None, **query) -> WinUIElement:
        keys = query.keys()
        use_class_name = "class_name" in keys
        use_re = "name_matches" in keys
        use_contains = "name_contains" in keys
        no_use_any = name is not None
        use_hwnd = "hwnd" in keys
        use_subtree = "use_subtree" in keys and query.get("use_subtree")
        if use_class_name:
            class_name = query.get("class_name")

        if no_use_any:
            name = name

        elif use_contains:
            name = query.get("name_contains")

        elif use_re:
            name = query.get("name_matches")

        elif use_hwnd:
            no_use_any = True
            name = query.get("hwnd").get_window_title
        else:
            raise ValueError("Unsupported query")
        if use_subtree:
            self.root = WinUIElement(_IUIAutomation.GetRootElement()).get_subtree()
        else:
            self.root = WinUIElement(_IUIAutomation.GetRootElement()).get_acc_children_elements()

        for window in self.root:
            if use_contains and name in window.get_acc_name:
                if use_class_name:
                    if class_name == window.get_class_name:
                        return window
                else:
                    return window
            elif use_re and re.search(name, window.get_acc_name) is not None:
                if use_class_name:
                    if class_name == window.get_class_name:
                        return window
                else:
                    return window
            elif no_use_any and name == window.get_acc_name:
                if name == window.get_acc_name:
                    if use_class_name:
                        if class_name == window.get_class_name:
                            return window
                    else:
                        return window

    def get_root(self) -> WinUIElement:
        return WinUIElement(_IUIAutomation.GetRootElement())
