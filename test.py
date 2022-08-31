import re

from makima.helper.operation import initialize_app_ref_for_win

rct = initialize_app_ref_for_win("Zoom")
# print(rct.get_class_name)
# find_element_by_wait(rct, acc_name="Invite (Alt+I)").click()


ss = ".*Start.*"
print(re.match(ss, "Start a new meeting with video on"))

