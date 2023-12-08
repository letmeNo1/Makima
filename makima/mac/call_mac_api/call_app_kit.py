import time

import AppKit
import psutil


def get_frontmost_pid():
    """
    Return the PID of the application in the foreground.
    :return: int
    """
    frontmost_app = AppKit.NSWorkspace.sharedWorkspace().frontmostApplication()
    pid = frontmost_app.processIdentifier()
    return pid


def get_paste_board():
    return AppKit.NSPasteboard.generalPasteboard().stringForType_(AppKit.NSPasteboardTypeString)


def clear_paste_board():
    AppKit.NSPasteboard.generalPasteboard().clearContents()


def set_paste_board(text):
    AppKit.NSPasteboard.generalPasteboard().clearContents()
    AppKit.NSPasteboard.generalPasteboard().setString_forType_(text, AppKit.NSPasteboardTypeString)


# more info off app object please view link:https://developer.apple.com/documentation/appkit/nsrunningapplication
def get_app_by_name(name):
    running_apps = AppKit.NSWorkspace.sharedWorkspace().runningApplications()
    for app in running_apps:
        if name == app.localizedName():
            return app
    return None


def get_identifier_by_pid(pid):
    running_apps = AppKit.NSWorkspace.sharedWorkspace().runningApplications()
    for app in running_apps:
        if app.processIdentifier() == pid:
            return app.bundleIdentifier()
    return None


def get_pid_by_identifier(bundleIdentifier):
    running_apps = AppKit.NSWorkspace.sharedWorkspace().runningApplications()
    for app in running_apps:
        if app.bundleIdentifier() == bundleIdentifier:
            return app.processIdentifier()
    return None

def _get_pid_by_name(name):
    # pool = AppKit.NSAutoreleasePool.alloc().init()
    for proc in psutil.process_iter(['pid', 'name']):
        # print(proc.info['name'])
        if proc.info['name'] == name:
            return proc.info['pid']
            # print(proc.info['pid'])
    return None


def get_pid_by_name(name):
    for i in range(4):
        pid = _get_pid_by_name(name)
        if pid is not None:
            break
        else:
            time.sleep(2)
            continue
    return pid


# print(get_pid_by_name("Finder"))

