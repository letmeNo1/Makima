import re
import time

import AppKit
import psutil


class CallAppKit:

    def get_frontmost_pid(self):
        """
        Return the PID of the application in the foreground.
        :return: int
        """
        frontmost_app = AppKit.NSWorkspace.sharedWorkspace().frontmostApplication()
        pid = frontmost_app.processIdentifier()
        return pid

    def get_paste_board(self):
        return AppKit.NSPasteboard.generalPasteboard().stringForType_(AppKit.NSPasteboardTypeString)

    def clear_paste_board(self):
        AppKit.NSPasteboard.generalPasteboard().clearContents()

    def set_paste_board(self,text):
        AppKit.NSPasteboard.generalPasteboard().clearContents()
        AppKit.NSPasteboard.generalPasteboard().setString_forType_(text, AppKit.NSPasteboardTypeString)

    # more info off app object please view link:https://developer.apple.com/documentation/appkit/nsrunningapplication
    def get_app_by_name(self,name):
        running_apps = AppKit.NSWorkspace.sharedWorkspace().runningApplications()
        for app in running_apps:
            if name == app.localizedName():
                return app
        return None

    def get_identifier_by_pid(self,pid):
        running_apps = AppKit.NSWorkspace.sharedWorkspace().runningApplications()
        for app in running_apps:
            if app.processIdentifier() == pid:
                return app.bundleIdentifier()
        return None

    def get_pid_by_identifier(self,bundleIdentifier):
        running_apps = AppKit.NSWorkspace.sharedWorkspace().runningApplications()
        for app in running_apps:
            print(app.bundleIdentifier())
            if app.bundleIdentifier() == bundleIdentifier:
                return app.processIdentifier()
        return None

    def _get_pid_by_name(self,name,query_type):
        for proc in psutil.process_iter(['pid', 'name']):
            if query_type is None and proc.info['name'] == name:
                return proc.info['pid']
            elif query_type == "use_contains" and name in proc.info['name']:
                return proc.info['pid']
            elif query_type == "use_re" and re.search(name, proc.info['name']) is not None:
                return proc.info['pid']
                # print(proc.info['pid'])
        return None

    def get_pid_by_name(self,name,query_type):
        for i in range(4):
            pid = self._get_pid_by_name(name,query_type)
            if pid is not None:
                break
            else:
                time.sleep(2)
                continue
        return pid
