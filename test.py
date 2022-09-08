from makima.helper.operation import initialize_app_ref_for_win
from makima.windows.utils.common import find_windows, set_focus_window

calculator = initialize_app_ref_for_win("Calculator")
# Make the window appear at frontends
hwnd = find_windows("Calculator")[0]
set_focus_window(hwnd)

# Do a 32 by 32 and get the result
calculator.find_element_by_wait(automation_id="num3Button").click()
calculator.find_element_by_wait(automation_id="num2Button").click()
calculator.find_element_by_wait(automation_id="multiplyButton").click()
calculator.find_element_by_wait(automation_id="num3Button").click()
calculator.find_element_by_wait(automation_id="num2Button").click()
calculator.find_element_by_wait(automation_id="equalButton").click()
