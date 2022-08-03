import ctypes.wintypes

import comtypes
from comtypes import GUID, IUnknown, COMMETHOD, POINTER, helpstring
from comtypes.gen._1EA4DBF0_3C3B_11CF_810C_00AA00389B71_0_1_1 import IAccessible
from comtypes.gen._944DE083_8FB8_45CF_BCB7_C477ACB2F897_0_1_0 import IRawElementProviderSimple

HRESULT = ctypes.wintypes.DWORD
comtypes.client.GetModule('uiautomationcore.dll')

class IAccessibleEx(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{F8b80AdA-2C44-48D0-89BE-5FF23C9CD875}')
    _idlflags_ = []


_methods_ = [
    COMMETHOD(
        [helpstring('Method GetObjectForChild')],
        HRESULT,
        'GetObjectForChild',
        (['in'], ctypes.c_ulong, 'idChild'),
        (
            ['retval', 'out'],
            POINTER(POINTER(IAccessibleEx)),
            'pRetVal'
        ),
    ),
    COMMETHOD(
        [helpstring('Method GetIAccessiblePair')],
        HRESULT,
        'GetIAccessiblePair',
        (['out'], POINTER(POINTER(IAccessible)), 'ppAcc'),
        (['out'], ctypes.c_ulong, 'pidChild'),
    ),
    COMMETHOD(
        [helpstring('Method GetRuntimeId')],
        HRESULT,
        'GetRuntimeId',
        (['out', 'retval'], ctypes.c_int, 'pRetVal'),
    ),
    COMMETHOD(
        [helpstring('Method ConvertReturnedElement')],
        HRESULT,
        'ConvertReturnedElement',
        (['in'], POINTER(IRawElementProviderSimple), 'pIn'),
        (
            ['out'],
            POINTER(POINTER(IAccessibleEx)),
            'ppRetValOut'
        ),
    ),
]
