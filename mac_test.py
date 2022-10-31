import os
import time
import unittest

from makima.helper.operation_mac import initialize_app_ref_for_mac
from makima.mac.utils.common import active_window, is_finished_launching


class MyTest(unittest.TestCase):
    def setUp(self):
        os.system("""osascript -e 'tell app "Calculator" to open'""")
        time.sleep(2)
        self.calculator = initialize_app_ref_for_mac("Calculator")
        # Make the window appear at frontends
        active_window("Calculator")
        assert is_finished_launching("Calculator") is True

    def tearDown(self):
        pass

    def test_calculator(self):
        self.calculator.find_elements_by_wait(title="3")[1].click()
        self.calculator.find_elements_by_wait(title="2")[1].click()
        self.calculator.find_elements_by_wait(title="×")[0].click()
        self.calculator.find_elements_by_wait(title="3")[1].click()
        self.calculator.find_elements_by_wait(title="2")[1].click()
        self.calculator.find_elements_by_wait(title="=")[0].click()
        time.sleep(2)
        assert self.calculator.find_elements_by_wait(role="AXStaticText")[1].get_value == "1024"


if __name__ == "__main__":
    unittest.main()
