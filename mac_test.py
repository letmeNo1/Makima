import os
import time
import unittest

from makima.helper.operation_mac import Init_App_Ref_For_Mac
from makima.mac.utils.common import MacCommon


class MyTest(unittest.TestCase):
    def setUp(self):
        os.system("""osascript -e 'tell app "Calculator" to open'""")
        time.sleep(2)
        self.makima = Init_App_Ref_For_Mac()
        self.makima_common = MacCommon()
        self.calculator = self.makima("Calculator")

        # Make the window appear at frontends
        self.makima_common.active_window("Calculator")
        assert self.makima_common.is_finished_launching("Calculator") is True

    def tearDown(self):
        pass
        # os.system("""osascript -e 'tell app "Calculator" to quit'""")

    def test_calculator(self):
        aa = self.calculator.get_acc_children_elements()
        # for a in aa:
        #     print(a.get_title)
        self.calculator.ele(title="3").click()
        self.calculator.ele(title="2").click()
        self.calculator.ele(title="×").click()
        self.calculator.ele(title="3").click()
        self.calculator.ele(title="2").click()
        self.calculator.ele(title="=").click()
        time.sleep(2)
        assert self.calculator.eles(role="AXStaticText")[1].get_value == "1024"


if __name__ == "__main__":
    unittest.main()
