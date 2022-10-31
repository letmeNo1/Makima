import ApplicationServices as AppServ


def get_app_ref_by_pid(pid):
    return AppServ.AXUIElementCreateApplication(pid)
