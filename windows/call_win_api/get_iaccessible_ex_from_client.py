import ctypes
from _winapi import NULL

import comtypes.client

from helper.operation import initialize_app_ref_for_win


def get_iaccessible_ex_from_iaccessible(i_accessible):
    p_service = i_accessible.QueryInterface(comtypes.IServiceProvider)

    if p_service is not None:
        ia2_ptr = p_service.QueryService(tss.IAccessibleEx.iid_, tss.IAccessibleEx)

        if ia2_ptr is not None:
            print
            'Accessible object implements IA2'


hWnd = ctypes.windll.user32.FindWindowW(NULL, "Calculator")

calculator = initialize_app_ref_for_win(hWnd)

get_iaccessible_ex_from_iaccessible(calculator)
