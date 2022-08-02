import ctypes
from asyncio.windows_events import NULL
from  ctypes  import  windll, oledll, WinError, byref, POINTER
from  ctypes.wintypes  import  POINT

import comtypes
from  comtypes  import  COMError
from  comtypes.automation  import  VARIANT
from  comtypes.client  import  GetModule

#  create wrapper for the oleacc.dll type library
GetModule( "oleacc.dll" )
#  import the interface we need from the wrapper



def  AccessibleObjectFromWindow(hwnd):
    ptr  =  POINTER(comtypes.gen.Accessibility.IAccessible)()
    res  =  oledll.oleacc.AccessibleObjectFromWindow(
    hwnd,0,
    byref(comtypes.gen.Accessibility.IAccessible._iid_),byref(ptr))
    return  ptr

hWnd = ctypes.windll.user32.FindWindowW(NULL, "Calculator")
AccessibleObjectFromWindow(hWnd)