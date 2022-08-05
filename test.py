import ctypes
from _winapi import NULL

import comtypes.client
from comtypes.gen._944DE083_8FB8_45CF_BCB7_C477ACB2F897_0_1_0 import IRawElementProviderSimple

from helper.operation import initialize_app_ref_for_win
from windows.utils.find_ui_element import find_element_by_automation_id_by_wait

hWnd = ctypes.windll.user32.FindWindowW(NULL, "Calculator")

calculator = initialize_app_ref_for_win(hWnd)
# calculator.AccessibleChildren()
aa = []

print(find_element_by_automation_id_by_wait(4000,calculator,"CalculatorResults").get_acc_location)
# print(calculator.get_acc_children_elements()[4].get_acc_children_elements()[1].get_acc_children_elements()[3].get_acc_children_elements()[1].get_acc_children_elements()[1].get_acc_children_elements()[1].get_acc_children_elements()[1].get_acc_children_elements()[1].get_automation_id)
#
# aaa = calculator.get_acc_children_elements()[3]
# bbb = aaa.get_acc_children_elements()[1]
# ccc = bbb.get_acc_children_elements()[3]
# GGG = ccc.get_acc_children_elements()[1]
# hhh = GGG.get_acc_children_elements()[1]
# print(hhh.get_automation_id)