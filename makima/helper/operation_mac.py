from makima.mac.call_mac_api.call_app_kit import get_pid_by_name
from makima.mac.ui_element import MacUIElement
import ApplicationServices as AppServ


def initialize_app_ref_for_mac(name):
    pid = int(get_pid_by_name(name))
    app_windows = AppServ.AXUIElementCreateApplication(pid)
    app = MacUIElement(app_windows)
    return app
