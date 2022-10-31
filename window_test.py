from makima.helper.operation_win import initialize_app_ref_for_win
from makima.windows.utils.common import find_windows, set_focus_window

import os
import time
import unittest


class MyTest(unittest.TestCase):
    def setUp(self):
        self.calculator = initialize_app_ref_for_win("Calculator")
        # Make the window appear at frontends
        hwnd = find_windows("Calculator")[0]
        set_focus_window(hwnd)

    def tearDown(self):
        pass

    def test_calculator(self):
        # Do a 32 by 32 and get the result
        self.calculator.find_element_by_wait(automation_id="num3Button").click()
        self.calculator.find_element_by_wait(automation_id="num2Button").click()
        self.calculator.find_element_by_wait(automation_id="multiplyButton").click()
        self.calculator.find_element_by_wait(automation_id="num3Button").click()
        self.calculator.find_element_by_wait(automation_id="num2Button").click()
        self.calculator.find_element_by_wait(automation_id="equalButton").click()
        time.sleep(2)
        assert self.calculator.find_elements_by_wait(role="AXStaticText")[1].get_value == "1024"


if __name__ == "__main__":
    unittest.main()
