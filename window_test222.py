from makima.helper.operation_win import initialize_app_ref_for_win
from makima.windows.utils.common import find_windows, set_focus_window

import os
import time
import unittest


class MyTest(unittest.TestCase):
    def setUp(self):
        self.meeting_with = initialize_app_ref_for_win("Meeting with", None, True)

    # def tearDown(self):
    #     # os.system('taskkill /f /t /im ' + "calculator.exe")

    def test_calculator(self):
        # Do a 32 by 32 and get the result
        print(self.meeting_with.find_element_by_wait(automation_id="microphone-button").get_description)



if __name__ == "__main__":
    unittest.main()
