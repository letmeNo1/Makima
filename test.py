import re

from makima.helper.operation import initialize_app_ref_for_win

rct = initialize_app_ref_for_win("Calculator")
# print(rct.get_class_name)
rct.find_element_by_wait(automation_id="num1Button").click()
rct.find_element_by_wait(acc_name="Nine").click()
