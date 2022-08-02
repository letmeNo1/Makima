import ctypes
import time
from _winapi import NULL
from comtypes import IServiceProvider
from comtypes.GUID import GUID


"""Accessibility Constants"""

from comtypes import IServiceProvider
from comtypes.gen.Accessibility import IAccessible
from comtypes.gen.IAccessible2Lib import IAccessible2

TIMEOUT = 10

CHILDID_SELF = 0x0
S_OK = 0x0

VT_I4 = 0x3
VT_DISPATCH = 0x9

FULL_CHILD_TREE = -1

IServiceProvider_t = IServiceProvider
IID_IServiceProvider = IServiceProvider._iid_

IAccessible_t = IAccessible
IID_IAccessible = IAccessible._iid_

IAccessible2_t = IAccessible2
IID_IAccessible2 = IAccessible2._iid_
import comtypes
from comtypes import IServiceProvider, IUnknown

from helper.operation import initialize_app_ref_for_win

class IAccessibleEx(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{F8b80AdA-2C44-48D0-89BE-5FF23C9CD875}')
    _idlflags_ = []

hWnd = ctypes.windll.user32.FindWindowW(NULL, "Calculator")

calculator = initialize_app_ref_for_win(hWnd)

# calculator.QueryInterface(comtypes.IUnknown)

i_accessible = ctypes.POINTER(
                comtypes.gen.Accessibility.IAccessible)()

ctypes.oledll.oleacc.AccessibleObjectFromWindow(
                hWnd,
                0,
                ctypes.byref(comtypes.gen.Accessibility.IAccessible._iid_),
                ctypes.byref(i_accessible))

obj_child_id = comtypes.automation.VARIANT()
obj_child_id.vt = comtypes.automation.VT_I4
obj_role = comtypes.automation.VARIANT()
obj_role.vt = comtypes.automation.VT_BSTR

i_accessible._IAccessible__com__get_accRole(obj_child_id,
                                                          obj_role)
print(obj_role.value)

p_service = i_accessible.QueryInterface(IServiceProvider)

if p_service is not None:
    ia2_ptr = p_service.QueryService(IAccessibleEx._iid_, IAccessibleEx)

    if ia2_ptr is not None:
        print
        'Accessible object implements IA2'



# other = p.QueryInterface(IUnknown)
# print(other)
