from makima.mac.call_mac_api.call_app_kit import get_pid_by_name, get_frontmost_pid
from makima.mac.ui_element import MacUIElement
import ApplicationServices as AppServ


class Init_App_Ref_For_Mac:
    def __call__(self,name):
        if name == "TopApplication":
            pid = get_frontmost_pid()
        else:
            pid = get_pid_by_name(name)
        if pid is not None:
            app_windows = AppServ.AXUIElementCreateApplication(int(pid))
            app = MacUIElement(app_windows)
        else:
            app = None
        return app
