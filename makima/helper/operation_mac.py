from apollo_makima.mac.call_mac_api.call_app_kit import CallAppKit
from apollo_makima.mac.ui_element import MacUIElement
import ApplicationServices as AppServ


class Init_App_Ref_For_Mac(CallAppKit):
    def __call__(self, name=None, **query) -> MacUIElement:
        if name == "TopApplication":
            pid = self.get_frontmost_pid()
        else:
            keys = query.keys()
            use_pid = "pid" in keys
            use_re = "name_matches" in keys
            use_contains = "name_contains" in keys
            no_use_any = name is not None
            query_type = None
            if no_use_any:
                name = name
            elif use_contains:
                query_type = "use_contains"
                name = query.get("name_contains")
            elif use_re:
                query_type = "use_re"
                name = query.get("name_matches")
            elif use_pid:
                pid = int(query.get("pid"))
                return MacUIElement(AppServ.AXUIElementCreateApplication(pid))
            else:
                raise ValueError("Unsupported query")
            pid = self.get_pid_by_name(name, query_type)
        if pid is not None:
            app_windows = AppServ.AXUIElementCreateApplication(int(pid))
            app = MacUIElement(app_windows)
        else:
            app = None
        return app
