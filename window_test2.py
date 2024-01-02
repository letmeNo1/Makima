from makima.windows.utils.common import WinCommon

from makima.helper.operation_win import Init_App_Ref_For_Win

import os
import time
import unittest


class MyTest(unittest.TestCase):
    def setUp(self):
        os.system(r"C:\Windows\System32\calc.exe")
        time.sleep(2)
        self.makima = Init_App_Ref_For_Win()
        self.makima_common = WinCommon()

        self.calculator = self.makima("Calculator")
        # Make the window appear at frontends
        hwnd = self.makima_common.find_windows("Calculator")[0]
        hwnd.focus_window()

    def tearDown(self):
        os.system('taskkill /f /t /im ' + "calculator.exe")

    def test_calculator(self):
        # Do a 32 by 32 and get the result
        # self.calculator.find_element_by_image_by_wait("C:\\Users\\hanhuang\\001.png").double_click()
        self.calculator.ele(automation_id="num2Button").click()
        self.calculator.ele(automation_id="multiplyButton").click()
        self.calculator.ele(automation_id="num3Button").click()
        self.calculator.ele(automation_id="num2Button").click()
        self.calculator.ele(automation_id="equalButton").click()
        self.calculator.ele(automation_id="equalButton").click()

        time.sleep(2)
        # assert self.calculator.find_element_by_wait(automation_id="CalculatorResults").get_acc_name == "Display is 1,024"
        # self.calculator.find_element_by_wait(automation_id="CalculatorResults").input_text("123")
        # assert self.calculator.find_element_by_wait(automation_id="CalculatorResults").get_acc_name == "Display is 123"

if __name__ == "__main__":
    unittest.main()
