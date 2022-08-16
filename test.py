import ctypes
import time

from win32con import NULL
from makima.helper.operation import initialize_app_ref_for_win

from makima.windows.utils.keyboard import WinKeyboard

win_keyboard = WinKeyboard()

# Launch RCT
win_keyboard.send(win_keyboard.codes.LEFT_WIN)
win_keyboard.copy_text("RCT UWP")
win_keyboard.send(win_keyboard.codes.CONTROL.modify(win_keyboard.codes.KEY_V), delay=0)
win_keyboard.send(win_keyboard.codes.RETURN)

time.sleep(3)
hWnd = ctypes.windll.user32.FindWindowW(NULL, "RCT UWP")
calculator = initialize_app_ref_for_win(hWnd)
# format_list = ["1920 x 1080 @ 30fps YUY2", "1920 x 1080 @ 27fps YUY2", "1920 x 1080 @ 24fps YUY2",
#                "1920 x 1080 @ 15fps "
#                "YUY2",
#                "640 x 360 @ 30fps YUY2", "640 x 360 @ 27fps YUY2", "640 x 360 @ 24fps YUY2", "640 x 360 @ 15fps YUY2",
#                "960 x 540 @ 30fps YUY2", "960 x 540 @ 27fps YUY2", "960 x 540 @ 24fps YUY2", "960 x 540 @ 15fps YUY2",
#                ]
#
# # ctypes.windll.user32.SetForegroundWindow(hWnd)
print(calculator.find_element_by_wait(automation_id="CameraList", class_name="ComboBox").get_class_name)

# ctypes.windll.user32.SetForegroundWindow(hWnd)
# calculator.find_element_by_wait(acc_name="Jabra PanaCast 20").click()
#
# calculator.find_element_by_wait(automation_id="FormatList").click()
#
# print(calculator.find_element_by_wait(5000, class_name="ComboBoxItem"))

# print(calculator.find_element_by_name_by_wait("3840 x 2160 @ 15fps MJPG"))
# print(_format + "'s FPS is " + FPS)

calculator.release()
