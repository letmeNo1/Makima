#!/usr/bin/env python

import ctypes
import ctypes.wintypes

import _ctypes
import comtypes.client
from comtypes import automation
from comtypes.automation import *
from comtypes.hresult import S_OK

from windows.call_win_api import i_accessible_ex
from windows.call_win_api.i_element import IElement
from windows.utils.common import replace_inappropriate_symbols
from windows.utils.mouse import WinMouse

comtypes.client.GetModule('oleacc.dll')
comtypes.CoInitializeEx()

CO_E_OBJNOTCONNECTED = -2147220995


class WinUIElement(IElement):
    """
    http://msdn.microsoft.com/en-us/library/dd318466(v=VS.85).aspx
    """

    _acc_role_name_map = {
        1: u'title bar',  # TitleBar
        2: u'menu bar',  # MenuBar
        3: u'scroll bar',  # ScrollBar
        4: u'grip',  # Grip
        5: u'sound',  # Sound
        6: u'cursor',  # Cursor
        7: u'caret',  # Caret
        8: u'alert',  # Alert
        9: u'window',  # Window
        10: u'client',  # Client
        11: u'popup menu',  # PopupMenu
        12: u'menu item',  # MenuItem
        13: u'tool tip',  # Tooltip
        14: u'application',  # Application
        15: u'document',  # Document
        16: u'pane',  # Pane
        17: u'chart',  # Chart
        18: u'dialog',  # Dialog
        19: u'border',  # Border
        20: u'grouping',  # Grouping
        21: u'separator',  # Separator
        22: u'tool bar',  # ToolBar
        23: u'status nar',  # StatusBar
        24: u'table',  # Table
        25: u'column header',  # ColumnHeader
        26: u'row header',  # RowHeader
        27: u'column',  # Column
        28: u'row',  # Row
        29: u'cell',  # Cell
        30: u'link',  # Link
        31: u'help balloon',  # HelpBalloon
        32: u'character',  # Character
        33: u'list',  # List
        34: u'list item',  # ListItem
        35: u'outline',  # Outline
        36: u'outline item',  # OutlineItem
        37: u'page tab',  # PageTab
        38: u'property page',  # PropertyPage
        39: u'indicator',  # Indicator
        40: u'graphic',  # Graphic
        41: u'text',  # Text
        42: u'editable text',  # EditableText
        43: u'push button',  # PushButton
        44: u'check box',  # CheckBox
        45: u'radio button',  # RadioButton
        46: u'combo box',  # ComboBox
        47: u'drop down',  # DropDown
        48: u'progress bar',  # ProgressBar
        49: u'dial',  # Dial
        50: u'hotKey field',  # HotKeyField
        51: u'slider',  # Slider
        52: u'spin box',  # SpinBox
        53: u'diagram',  # Diagram
        54: u'animation',  # Animation
        55: u'equation',  # Equation
        56: u'drop down button',  # DropDownButton
        57: u'menu button',  # MenuButton
        58: u'grid drop down button',  # GridDropDownButton
        59: u'white space',  # WhiteSpace
        60: u'page tab list',  # PageTabList
        61: u'clock',  # Clock
        62: u'split button',  # SplitButton
        63: u'ip address',  # IPAddress
        64: u'outline button'  # OutlineButton
    }

    _mouse = WinMouse()

    class _StateFlag(object):
        SYSTEM_NORMAL = 0
        SYSTEM_UNAVAILABLE = 0x1
        SYSTEM_SELECTED = 0x2
        SYSTEM_FOCUSED = 0x4
        SYSTEM_PRESSED = 0x8
        SYSTEM_CHECKED = 0x10
        SYSTEM_MIXED = 0x20
        SYSTEM_READONLY = 0x40
        SYSTEM_HOTTRACKED = 0x80
        SYSTEM_DEFAULT = 0x100
        SYSTEM_EXPANDED = 0x200
        SYSTEM_COLLAPSED = 0x400
        SYSTEM_BUSY = 0x800
        SYSTEM_FLOATING = 0x1000
        SYSTEM_MARQUEED = 0x2000
        SYSTEM_ANIMATED = 0x4000
        SYSTEM_INVISIBLE = 0x8000
        SYSTEM_OFFSCREEN = 0x10000
        SYSTEM_SIZEABLE = 0x20000
        SYSTEM_MOVEABLE = 0x40000
        SYSTEM_SELFVOICING = 0x80000
        SYSTEM_FOCUSABLE = 0x100000
        SYSTEM_SELECTABLE = 0x200000
        SYSTEM_LINKED = 0x400000
        SYSTEM_TRAVERSED = 0x800000
        SYSTEM_MULTISELECTABLE = 0x1000000
        SYSTEM_EXTSELECTABLE = 0x2000000
        SYSTEM_ALERT_LOW = 0x4000000
        SYSTEM_ALERT_MEDIUM = 0x8000000
        SYSTEM_ALERT_HIGH = 0x10000000
        SYSTEM_PROTECTED = 0x20000000
        SYSTEM_HASPOPUP = 0x40000000
        SYSTEM_VALID = 0x7fffffff

    class _SelectionFlag(object):
        NONE = 0
        TAKEFOCUS = 0x1
        TAKESELECTION = 0x2
        EXTENDSELECTION = 0x4
        ADDSELECTION = 0x8
        REMOVESELECTION = 0x10
        VALID = 0x20

    def __init__(self, obj_handle, i_object_id):
        """
        Constructor.

        :param obj_handle: instance of i_accessible or window handle.
        :param int i_object_id: object id.
        """

        if isinstance(obj_handle, comtypes.gen.Accessibility.IAccessible):
            i_accessible = obj_handle
        else:
            i_accessible = ctypes.POINTER(
                comtypes.gen.Accessibility.IAccessible)()
            ctypes.oledll.oleacc.AccessibleObjectFromWindow(
                obj_handle,
                0,
                ctypes.byref(comtypes.gen.Accessibility.IAccessible._iid_),
                ctypes.byref(i_accessible))

        self._i_accessible = i_accessible
        self._i_object_id = i_object_id
        self._cached_children = set()
        self._simple_elements = dict()

    def check_state(self, state):
        """
        Checks state.

        :param int state: state flag.

        :rtype: bool
        :return: bool flag indicator.
        """
        return bool(self._acc_state & state)

    @property
    def get_hwnd_from_accessible(self):
        """
        Property for window handler.
        """
        hwnd = ctypes.c_int()
        ctypes.oledll.oleacc.WindowFromAccessibleObject(self._i_accessible,
                                                        ctypes.byref(hwnd))

        return hwnd.value

    @property
    def get_role(self):
        """
        Property for element role.
        """
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self._i_object_id
        obj_role = comtypes.automation.VARIANT()
        obj_role.vt = comtypes.automation.VT_BSTR

        self._i_accessible._IAccessible__com__get_accRole(obj_child_id,
                                                          obj_role)

        return obj_role.value

    def _select(self, i_selection):
        if self._i_object_id:
            return self._i_accessible.accSelect(i_selection, self._i_object_id)
        else:
            return self._i_accessible.accSelect(i_selection)

    def click(self, x_offset=0, y_offset=0):
        x, y, w, h = self.acc_location
        x += x_offset if x_offset is not None else w / 2
        y += y_offset if y_offset is not None else h / 2

        self._mouse.click(x, y)

    def right_click(self, x_offset=0, y_offset=0):
        x, y, w, h = self.acc_location
        x += x_offset if x_offset is not None else w / 2
        y += y_offset if y_offset is not None else h / 2

        self._mouse.click(x, y, self._mouse.RIGHT_BUTTON)

    def double_click(self, x_offset=0, y_offset=0):
        x, y, w, h = self.acc_location
        x += x_offset if x_offset is not None else w / 2
        y += y_offset if y_offset is not None else h / 2

        self._mouse.double_click(x, y)

    def drag_to(self, x, y, x_offset=None, y_offset=None, smooth=True):
        el_x, el_y, el_w, el_h = self.acc_location
        el_x += x_offset if x_offset is not None else el_w / 2
        el_y += y_offset if y_offset is not None else el_h / 2

        self._mouse.drag(el_x, el_y, x, y, smooth)

    @property
    def proc_id(self):
        hwnd = ctypes.c_long(self._hwnd)
        proc_id = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd,
                                                      ctypes.byref(proc_id))

        return proc_id.value

    @property
    def is_top_level_window(self):
        # Top level window have 2 parents, clnt and frm for Desktop.
        return self.acc_parent_count == 2

    @property
    def is_selected(self):
        return self._check_state(self._StateFlag.SYSTEM_SELECTED)

    @property
    def is_checked(self):
        return self._check_state(self._StateFlag.SYSTEM_CHECKED)

    @property
    def is_visible(self):
        return not self._check_state(self._StateFlag.SYSTEM_INVISIBLE)

    @property
    def is_enabled(self):
        return not self._check_state(self._StateFlag.SYSTEM_UNAVAILABLE)

    @property
    def acc_parent_count(self):
        parent_count = 0
        parent = self.acc_parent
        while parent:
            parent_count += 1
            parent = parent.acc_parent

        return parent_count

    @property
    def acc_child_count(self):
        if self._i_object_id == 0:
            return self._get_child_count_safely(self._i_accessible)
        else:
            return 0

    @property
    def get_acc_name(self):
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self._i_object_id

        obj_name = comtypes.automation.BSTR()
        try:
            self._i_accessible._IAccessible__com__get_accName(
                obj_child_id, ctypes.byref(obj_name))
            result = obj_name.value or ''
        except _ctypes.COMError:
            result = ""

        return replace_inappropriate_symbols(result)

    def set_focus(self):
        self._select(self._SelectionFlag.TAKEFOCUS)

    @property
    def get_acc_location(self):
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self._i_object_id

        obj_l, obj_t, obj_w, obj_h = ctypes.c_long(), ctypes.c_long(), \
                                     ctypes.c_long(), ctypes.c_long()

        self._i_accessible._IAccessible__com_accLocation(ctypes.byref(obj_l),
                                                         ctypes.byref(obj_t),
                                                         ctypes.byref(obj_w),
                                                         ctypes.byref(obj_h),
                                                         obj_child_id)

        return obj_l.value, obj_t.value, obj_w.value, obj_h.value

    @property
    def get_acc_value(self):
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self._i_object_id
        obj_bstr_value = comtypes.automation.BSTR()
        self._i_accessible._IAccessible__com__get_accValue(
            obj_child_id, ctypes.byref(obj_bstr_value))

        return obj_bstr_value.value

    def set_value(self, value):
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self._i_object_id

        self._i_accessible._IAccessible__com__set_accValue(obj_child_id, value)

    @property
    def get_acc_description(self):
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self._i_object_id
        obj_description = comtypes.automation.BSTR()
        self._i_accessible._IAccessible__com__get_accDescription(
            obj_child_id, ctypes.byref(obj_description))

        return obj_description.value

    @property
    def get_acc_parent(self):
        result = None
        if self._i_accessible.accParent:
            result = \
                WinUIElement(self._i_accessible.accParent, self._i_object_id)

        return result

    @property
    def get_acc_selection(self):
        obj_children = comtypes.automation.VARIANT()
        self._i_accessible._IAccessible__com__get_accSelection(
            ctypes.byref(obj_children))

        return obj_children.value

    @property
    def get_acc_state(self):
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self._i_object_id
        obj_state = comtypes.automation.VARIANT()
        self._i_accessible._IAccessible__com__get_accState(
            obj_child_id, ctypes.byref(obj_state))

        return obj_state.value

    @property
    def get_acc_focused_element(self):
        result = None
        if self._i_accessible.accFocus:
            result = WinUIElement(self._i_accessible.accFocus, self._i_object_id)

        return result

    @property
    def get_acc_focused_element(self):
        result = None
        if self._i_accessible.accFocus:
            result = WinUIElement(self._i_accessible.accFocus, self._i_object_id)

        return result

    @property
    def get_acc_role_name(self):
        return self._acc_role_name_map.get(self.get_role, 'unknown')

    @property
    def get_automation_id(self):
        return self.get_property_value(comtypes.gen.UIAutomationClient.UIA_AutomationIdPropertyId)

    @property
    def get_full_description(self):
        return self.get_property_value(comtypes.gen.UIAutomationClient.UIA_FullDescriptionPropertyId)

    def get_class_name(self):
        return self.get_property_value(comtypes.gen.UIAutomationClient.UIA_ClassNamePropertyId)

    def get_acc_children_elements(self):
        accChildren = []

        obj_acc_child_array = (comtypes.automation.VARIANT *
                               self._i_accessible.accChildCount)()
        obj_acc_child_count = ctypes.c_long()

        ctypes.oledll.oleacc.AccessibleChildren(
            self._i_accessible,
            0,
            self._i_accessible.accChildCount,
            obj_acc_child_array,
            ctypes.byref(obj_acc_child_count))

        for i in range(obj_acc_child_count.value):
            obj_acc_child = obj_acc_child_array[i]
            if obj_acc_child.vt == comtypes.automation.VT_DISPATCH:
                accChildren.append(WinUIElement(obj_acc_child.value.QueryInterface(
                    comtypes.gen.Accessibility.IAccessible), 0))
            else:
                accChildren.append(WinUIElement(self._i_accessible, obj_acc_child.value))
        return accChildren

    def is_object_exists(self, **kwargs):
        try:
            self.find(**kwargs)
            return True
        except Exception:
            return False

    def _get_child_count_safely(self, i_accessible):
        """
        Safely gets child count.

        :param i_accessible: instance of i_accessible.
        :rtype: int
        :return: object child count
        """
        try:
            return i_accessible.accChildCount
        except Exception as ex:
            if isinstance(ex, comtypes.COMError) and getattr(ex, 'hresult') \
                    in (CO_E_OBJNOTCONNECTED,):
                return 0

    def get_property_value(self, identifiers):
        p_service = self._i_accessible.QueryInterface(comtypes.IServiceProvider)

        if p_service is not None:
            try:
                i_accessible_ex_ptr = p_service.QueryService(i_accessible_ex.IAccessibleEx._iid_,
                                                             i_accessible_ex.IAccessibleEx)

                if i_accessible_ex_ptr is not None:
                    ia_ex_service = i_accessible_ex_ptr.QueryInterface(
                        comtypes.gen.UIAutomationClient.IRawElementProviderSimple)

                    if ia_ex_service is not None:
                        return ia_ex_service.GetPropertyValue(identifiers)
            except Exception:
                pass
