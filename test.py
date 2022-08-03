import ctypes
from _winapi import NULL

import comtypes.client
from comtypes.gen._944DE083_8FB8_45CF_BCB7_C477ACB2F897_0_1_0 import IRawElementProviderSimple

from helper.operation import initialize_app_ref_for_win
from windows.call_win_api import i_accessible_ex
from windows.utils import find_ui_element
from windows.utils.find_ui_element import find_element_by_text

hWnd = ctypes.windll.user32.FindWindowW(NULL, "Calculator")

calculator = initialize_app_ref_for_win(hWnd)
calculator.get_acc_children_elements
print(calculator._cached_children)
