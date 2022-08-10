import ctypes
import time

from win32con import NULL
from helper.operation import initialize_app_ref_for_win
from windows.utils.keyboard import WinKeyboard

# desktop = ctypes.windll.user32.GetDesktopWindow()


win_keyboard = WinKeyboard()

# Launch RCT
win_keyboard.send(win_keyboard.codes.LEFT_WIN)
win_keyboard.copy_text("RCT UWP")
win_keyboard.send(win_keyboard.codes.CONTROL.modify(win_keyboard.codes.KEY_V), delay=0)
win_keyboard.send(win_keyboard.codes.RETURN)


time.sleep(3)
hWnd = ctypes.windll.user32.FindWindowW(NULL, "RCT UWP")
calculator = initialize_app_ref_for_win(hWnd)

format_list = ["1920 x 1080 @ 30fps YUY2", "1920 x 1080 @ 27fps YUY2", "1920 x 1080 @ 24fps YUY2",
               "1920 x 1080 @ 15fps "
               "YUY2",
               "640 x 360 @ 30fps YUY2", "640 x 360 @ 27fps YUY2", "640 x 360 @ 24fps YUY2", "640 x 360 @ 15fps YUY2",
               "960 x 540 @ 30fps YUY2", "960 x 540 @ 27fps YUY2", "960 x 540 @ 24fps YUY2", "960 x 540 @ 15fps YUY2",
               ]

# ctypes.windll.user32.SetForegroundWindow(hWnd)
calculator.find_element_by_automation_id_by_wait("CameraList").click()

# ctypes.windll.user32.SetForegroundWindow(hWnd)
calculator.find_element_by_name_by_wait("Jabra PanaCast 20").click()

for _format in format_list:
    calculator.find_element_by_automation_id_by_wait("FormatList").click()
    calculator.find_element_by_name_by_wait(_format).click()
    time.sleep(10)
    FPS = calculator.find_last_element_by_name_by_wait("Jitter (ms):").get_acc_name
    print(_format + "'s FPS is " + FPS)

calculator.release()
