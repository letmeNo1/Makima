# from AppKit import NSWorkspace
import Quartz
import ApplicationServices as AppServ
import time

from makima.mac.a11y import AXUIElement

# from AXClasses import BaseAXUIElement
#
# from makima.mac.a11y import AXUIElement
#
#
# # from application_window import ApplicationWindow
#
#
# class ActiveWindow():
#     def __init__(self):
#         self.app_name = str()
#         self.app_pid = int()
#         self.active_screen_index = int()
#         # self.window_size = ApplicationWindow(0, 0, 0, 0)
#
#     # def get_frontmost_application(self):
#     #     frontmost_application = NSWorkspace.sharedWorkspace().activeApplication()
#     #     self.app_name = frontmost_application["NSApplicationName"]
#     #     self.app_pid = frontmost_application["NSApplicationProcessIdentifier"]
#     #     return frontmost_application
#
#     # TODO: refactor it as getters/setters
#     def set_position(self, app_ref):
#         new_coordinates = AppServ.CGPoint(self.window_size.x, self.window_size.y)
#         position = AppServ.AXValueCreate(AppServ.kAXValueCGPointType, new_coordinates)
#         AppServ.AXUIElementSetAttributeValue(app_ref, AppServ.kAXPositionAttribute, position)
#
#     def set_window_size(self, app_ref):
#         # new_size = AppServ.CGSize(self.window_size.width,self.window_size.height)
#         new_size = AppServ.CGSize(self.window_size.width, self.window_size.height)
#
#         size = AppServ.AXValueCreate(AppServ.kAXValueCGSizeType, new_size)
#         AppServ.AXUIElementSetAttributeValue(app_ref, AppServ.kAXSizeAttribute, size)
#         AppServ.AXUIElementSetAttributeValue(app_ref, AppServ.kAXSizeAttribute, size)
#
#     def get_window_info(self):
#         windows = Quartz.CGWindowListCopyWindowInfo(
#             Quartz.kCGWindowListExcludeDesktopElements | Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
#         for win in windows:
#             if self.app_name in (win[Quartz.kCGWindowOwnerName], win.get(Quartz.kCGWindowName, '')):
#                 return win["kCGWindowBounds"]
#
#     # def get_window_size(self):
#     #     window_info = self.get_window_info()
#     #     return ApplicationWindow(window_info["X"], window_info["Y"], window_info["Width"], window_info["Height"])
#     #
#     # def resize(self, window: ApplicationWindow.count_window_size):
#     #     self.get_frontmost_application()
#
#         # get window coordinates and size
#         self.window_size = self.get_window_size()
#         print("WINDOW SIZE", self.window_size.__dict__)
#         self.active_screen_index = self.window_size.set_window_location()
#         self.window_size = window(self.active_screen_index)
#
#         app_windows = AppServ.AXUIElementCreateApplication(self.app_pid)  # AXUIElementRef
#
#         # get list of windows with the same PID ""
#         windowList = AppServ.AXUIElementCopyAttributeValue(app_windows, AppServ.kAXWindowsAttribute, None)
#
#         # get front app window from the list
#         app_ref = windowList[1][0]  # AXUIElement
#         "Set position of application window"
#         self.set_position(app_ref)
#         time.sleep(0.5)
#         self.set_window_size(app_ref)
#
#         # TODO: fix bug - be sure if both operations were made
#         # get current coordinates and size of application window, if something is not valid -> invoke again (how to get coordinates without loading all opened applications??)
#         # set size of application windo
#         #
#         # w

app_windows = AppServ.AXUIElementCreateApplication(11741)  # AXUIElementRef
# windowList = AppServ.AXUIElementCopyAttributeValue(app_windows, AppServ.kAXPositionAttribute, None)
# AXUIElement
aa = AXUIElement(app_windows)
print(aa.get_pid())
print(aa.get_attribute(AppServ.kAXChildrenAttribute))
