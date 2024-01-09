#!/usr/bin/env python
from __future__ import annotations
from typing import List

import _ctypes
import comtypes.client
from apollo_makima.windows.static_variable import state_dict, _control_type, property_id, _tree_scope

from apollo_makima.windows.utils.mouse import WinMouse
from apollo_makima.windows.utils.keyboard import WinKeyboard

import comtypes.client

from apollo_makima.helper.find_ui_element import *

from apollo_makima.windows.static_variable import role_dict

CO_E_OBJNOTCONNECTED = -2147220995
UIAutomationCore = comtypes.client.GetModule("UIAutomationCore.dll")
IUIAutomation = comtypes.client.CreateObject("{ff48dba4-60ef-4201-aa87-54103eef594e}",
                                             interface=UIAutomationCore.IUIAutomation)

_IUIAutomation = comtypes.CoCreateInstance(comtypes.gen.UIAutomationClient.CUIAutomation._reg_clsid_,
                                           interface=comtypes.gen.UIAutomationClient.IUIAutomation,
                                           clsctx=comtypes.CLSCTX_INPROC_SERVER)

UIAutomationClient = comtypes.gen.UIAutomationClient


class WinUIElement(object):
    def __init__(self, IUIAutomationElement):
        self.__IUIAutomationElement = IUIAutomationElement
        self.current_hwnd = None
        self._mouse = WinMouse()
        self._keyboard = WinKeyboard()
        self.get_last_ele: WinUIElement = None
        self.get_next_ele: WinUIElement = None

    def __get_state_text(self, state_code):
        state_text = []
        for code, text in state_dict.items():
            if state_code & code:
                state_text.append(text)
        return state_text

    def __get_IUIAutomationElement_attr(self, attr):
        try:
            attr = getattr(self.__IUIAutomationElement, attr)
        except _ctypes.COMError:
            attr = ""
        return attr

    def _set_current_hwnd(self, hwnd):
        self.current_hwnd = hwnd

    @property
    def get_current_hwnd(self):
        return self.current_hwnd

    @property
    def get_CachedNativeWindowHandle(self):
        hwnd = self.__get_IUIAutomationElement_attr("CurrentNativeWindowHandle")
        return hwnd

    @property
    def get_toggle_state(self):
        """Retrieves the UI Automation element value
        :rtype : unicode
        """
        IUnknown = self.__IUIAutomationElement.GetCurrentPattern(UIAutomationClient.UIA_TogglePatternId)
        IUIAutomationTogglePattern = IUnknown.QueryInterface(UIAutomationClient.IUIAutomationTogglePattern)
        return IUIAutomationTogglePattern.CurrentToggleState

    CurrentToggleState = get_toggle_state

    @property
    def get_acc_value(self):
        """Retrieves the UI Automation element value
        :rtype : unicode
        """
        return self.__get_iaccessible_property(property_id["LegacyIAccessibleValueProperty"])

    CurrentValue = get_acc_value

    @property
    def get_acc_keyboardshortcut(self):
        return self.__get_iaccessible_property(property_id["LegacyIAccessibleKeyboardShortcutProperty"])

    @property
    def get_automation_id(self):
        """Retrieves the UI Automation identifier of the element
        :rtype : unicode
        """
        return self.__get_IUIAutomationElement_attr("CurrentAutomationId")

    AutomationId = get_automation_id

    def get_acc_location(self):
        """Retrieves the coordinates of the rectangle that completely encloses the element.
        Returns tuple (left, top, right, bottom)
        :rtype : tuple
        """
        rect = self.__get_IUIAutomationElement_attr("CurrentBoundingRectangle")
        return rect.left, rect.top, rect.right, rect.bottom

    BoundingRectangle = get_acc_location

    @property
    def get_class_name(self):
        """Retrieves the class name of the element
        :rtype : unicode
        """
        return self.__get_IUIAutomationElement_attr("CurrentClassName")

    ClassName = get_class_name

    @property
    def get_control_type(self):
        """Retrieves the control type of the element
        :rtype : int
        """
        return self.__get_IUIAutomationElement_attr("CurrentControlType")

    ControlType = get_control_type

    @property
    def get_control_type_name(self):
        """Retrieves the name of the control type of the element.
        Ref: http://msdn.microsoft.com/en-us/library/windows/desktop/ee671198(v=vs.85).aspx
        :rtype : str
        """
        return _control_type[self.get_control_type]

    ControlTypeName = get_control_type_name

    @property
    def get_is_enabled(self):
        """Indicates whether the element is enabled
        :rtype : bool
        """
        return bool(self.__get_IUIAutomationElement_attr("CurrentIsEnabled"))

    IsEnabled = get_is_enabled

    @property
    def get_acc_name(self):
        """Retrieves the name of the element
        :rtype : unicode
        """
        return self.__get_IUIAutomationElement_attr("CurrentName")


    Name = get_acc_name

    @property
    def get_default_action(self):
        IUnknown = self.__IUIAutomationElement.GetCurrentPattern(UIAutomationClient.UIA_LegacyIAccessiblePatternId)
        IUIAutomationLegacyIAccessiblePattern = IUnknown.QueryInterface(
            UIAutomationClient.IUIAutomationLegacyIAccessiblePattern)
        return str(IUIAutomationLegacyIAccessiblePattern.CurrentDefaultAction)

    DefaultAction = get_default_action

    def _set_value(self, value):
        """Retrieves the UI Automation element value
        :rtype : unicode
        """
        IUnknown = self.__IUIAutomationElement.GetCurrentPattern(UIAutomationClient.UIA_ValuePatternId)
        IUIAutomationValuePattern = IUnknown.QueryInterface(UIAutomationClient.IUIAutomationValuePattern)
        IUIAutomationValuePattern.SetValue(value)

    def get_clickable_point(self):
        """Retrieves a point on the element that can be clicked
        Returns tuple (x, y) if a clickable point was retrieved, or None otherwise
        :rtype : tuple
        """
        point = self.__IUIAutomationElement.GetClickablePoint()
        if point[1]:
            return point[0].x, point[0].y
        else:
            return None

    def _set_last_ele(self, ele):
        self.get_last_ele = ele

    def _set_next_ele(self, ele):
        self.get_next_ele = ele

    @property
    def get_description(self):
        return self.__get_iaccessible_property(property_id["LegacyIAccessibleDescriptionProperty"])

    @property
    def get_acc_role(self):
        return role_dict.get(int(self.__get_iaccessible_property(property_id["LegacyIAccessibleRoleProperty"])))

    @property
    def get_state(self):
        return self.__get_state_text(self.__get_iaccessible_property(property_id["LegacyIAccessibleStateProperty"]))

    @property
    def get_window_state(self):
        state = {0: "standard", 1: "maxiuim", 2: "minimize"}
        return state.get(int(self.__get_iaccessible_property(property_id["WindowWindowVisualStateProperty"])))

    def __get_iaccessible_property(self, propertyId):
        return self.__IUIAutomationElement.GetCurrentPropertyValue(propertyId)

    def _build_condition(self, Name, ControlType, AutomationId):
        condition = _IUIAutomation.CreateTrueCondition()

        if Name is not None:
            name_condition = _IUIAutomation.CreatePropertyCondition(UIAutomationClient.UIA_NamePropertyId, Name)
            condition = _IUIAutomation.CreateAndCondition(condition, name_condition)

        if ControlType is not None:
            control_type_condition = _IUIAutomation.CreatePropertyCondition(
                UIAutomationClient.UIA_ControlTypePropertyId, ControlType)
            condition = _IUIAutomation.CreateAndCondition(condition, control_type_condition)

        if AutomationId is not None:
            automation_id_condition = _IUIAutomation.CreatePropertyCondition(
                UIAutomationClient.UIA_AutomationIdPropertyId, AutomationId)
            condition = _IUIAutomation.CreateAndCondition(condition, automation_id_condition)

        return condition

    def __findfirst(self, tree_scope, Name=None, ControlType=None, AutomationId=None):
        """Retrieves the first child or descendant element that matches specified conditions
        Returns None if there is no element that matches specified conditions
        If Name is None, element with any name will match
        If ControlType is None, element with any control type will match
        :param tree_scope: Should be one of 'element', 'children', 'descendants', 'parent', 'ancestors', 'subtree'.
            Ref: http://msdn.microsoft.com/en-us/library/windows/desktop/ee671699(v=vs.85).aspx
        :type tree_scope: str
        :param Name: Name of the element.
        :type Name: str
        :param ControlType: Control type of the element (one of UIAutomationClient.UIA_*ControlTypeId).
            Ref: http://msdn.microsoft.com/en-us/library/windows/desktop/ee671198(v=vs.85).aspx
        :type ControlType: int
        :param AutomationId: UI Automation identifier (ID) for the automation element.
            Ref: http://msdn.microsoft.com/en-us/library/windows/desktop/ee695997(v=vs.85).aspx
        :type AutomationId: str
        :rtype : _UIAutomationElement
        """
        tree_scope = _tree_scope[tree_scope]
        condition = self._build_condition(Name, ControlType, AutomationId)
        element = self.__IUIAutomationElement.__FindFirst(tree_scope, condition)
        return WinUIElement(element) if element else None

    #
    def __findall(self, tree_scope, Name=None, ControlType=None, AutomationId=None):
        """Returns list of UI Automation elements that satisfy specified conditions
        Returns empty list if there are no elements that matches specified conditions
        If Name is None, elements with any name will match
        If ControlType is None, elements with any control type will match
        :param tree_scope: Should be one of 'element', 'children', 'descendants', 'parent', 'ancestors', 'subtree'.
            Ref: http://msdn.microsoft.com/en-us/library/windows/desktop/ee671699(v=vs.85).aspx
        :type tree_scope: str
        :param Name: Name of the element.
        :type Name: str
        :param ControlType: Control type of the element (one of UIAutomationClient.UIA_*ControlTypeId).
            Ref: http://msdn.microsoft.com/en-us/library/windows/desktop/ee671198(v=vs.85).aspx
        :type ControlType: int
        :param AutomationId: UI Automation identifier (ID) for the automation element.
            Ref: http://msdn.microsoft.com/en-us/library/windows/desktop/ee695997(v=vs.85).aspx
        :type AutomationId: str
        :rtype : list
        """
        tree_scope = _tree_scope[tree_scope]
        condition = self._build_condition(Name, ControlType, AutomationId)

        IUIAutomationElementArray = self.__IUIAutomationElement.FindAll(tree_scope, condition)
        return [WinUIElement(IUIAutomationElementArray.GetElement(i)) for i in
                range(IUIAutomationElementArray.Length)]

    def __invoke(self):
        IUnknown = self.__IUIAutomationElement.GetCurrentPattern(UIAutomationClient.UIA_InvokePatternId)
        IUIAutomationInvokePattern = IUnknown.QueryInterface(UIAutomationClient.IUIAutomationInvokePattern)
        IUIAutomationInvokePattern.Invoke()

    def __str__(self):
        return '<%s (Name: %s, Class: %s, AutomationId: %s>' % (
            self.get_control_type_name, self.get_acc_name, self.get_class_name, self.get_automation_id)

    def get_acc_children_elements(self) -> List[WinUIElement]:
        children_list = []
        condition = _IUIAutomation.CreateTrueCondition()
        tree_scope = comtypes.gen.UIAutomationClient.TreeScope_Children
        children = self.__IUIAutomationElement.FindAll(tree_scope, condition)
        for i in range(children.Length):
            child = children.GetElement(i)
            if WinUIElement(child).get_acc_name != "Desktop" and WinUIElement(child).get_acc_name != "Program Manager":
                children_list.append(WinUIElement(child))

        return children_list

    def get_parent(self) -> WinUIElement:
        return self.__findall("parent")[0]

    def get_subtree(self) -> List[WinUIElement]:
        return self.__findall("subtree")

    @property
    def get_CachedNativeWindowHandle(self):
        hwnd = self.__get_IUIAutomationElement_attr("CurrentNativeWindowHandle")
        return hwnd

    '''
    query:
        automation_id=automation id
        acc_name=acc name
        acc_value=acc value
        class_name=class name
        control_type_name=control type name
    '''

    def ele(self, timeout=5, **query) -> WinUIElement:
        return wait_function(timeout, find_element_by_query, self, **query)

    def any_ele(self, query, timeout=5) -> WinUIElement:
        return wait_any(timeout, find_element_by_query, self, query)

    def eles(self, timeout=5, **query) -> List[WinUIElement]:
        return wait_function(timeout, find_elements_by_query, self, **query)

    def check_element_exist(self, timeout=5, **query):
        rst = wait_exist(timeout, find_element_by_query, self, **query)
        return rst

    def scroll_to_find_element(self, scroll_time=15, timeout=5, **query):
        for i in range(int(scroll_time)):
            ele = wait_function(timeout, find_element_by_query, self, **query)
            if "invisible" not in ele.get_state:
                return ele
            else:
                self._keyboard.send_keys(self._keyboard.codes.DOWN)

        return None

    def __get_coordinate(self, x_coordinate=None, y_coordinate=None, x_offset: float = None, y_offset: float = None):
        if x_coordinate is not None:
            x = x_coordinate
            y = y_coordinate
        else:
            rect = self.get_acc_location()
            width = (rect[2] - rect[0])
            hight = (rect[3] - rect[1])
            x = rect[0] + width / 2
            y = rect[1] + hight / 2

            if x_offset is not None:
                x = x + int(width / 2 * x_offset)
            elif y_offset is not None:
                y = y + int(hight / 2 * y_offset)

        return x, y

    def click(self, x_coordinate=None, y_coordinate=None, x_offset: float = None,
              y_offset: float = None, need_move=False):
        x, y = self.__get_coordinate(x_coordinate, y_coordinate, x_offset, y_offset)
        self._mouse.click(x, y, need_move)

    def hover(self, x_coordinate=None, y_coordinate=None, x_offset: float = None,
              y_offset: float = None, need_move=False,):
        x, y = self.__get_coordinate(x_coordinate, y_coordinate, x_offset, y_offset)
        self._mouse.move(x, y, need_move)

    def right_click(self, x_coordinate=None, y_coordinate=None, x_offset: float = None, y_offset: float = None, need_move=False):
        x, y = self.__get_coordinate(x_coordinate, y_coordinate, x_offset, y_offset)
        self._mouse.click(x, y, need_move, self._mouse.RIGHT_BUTTON)

    def double_click(self, x_coordinate=None, y_coordinate=None, x_offset: float = None,
              y_offset: float = None):
        x, y = self.__get_coordinate(x_coordinate, y_coordinate, x_offset, y_offset)

        self._mouse.double_click(x, y)

    def drag_to(self, x2, y2, x_coordinate=None, y_coordinate=None, x_offset=None, y_offset=None, smooth=True):
        x, y = self.__get_coordinate(x_coordinate, y_coordinate, x_offset, y_offset)
        self._mouse.drag(x, y, x2, y2, smooth)

    def wheel_to(self, distans, x_coordinate=None, y_coordinate=None, x_offset=None, y_offset=None):
        x, y = self.__get_coordinate(x_coordinate, y_coordinate, x_offset, y_offset)
        self._mouse.scroll_wheel(x, y, distans)

    def input_text(self, text):
        self.click()
        self._keyboard.copy_text(text)
        self._keyboard.send_keys(self._keyboard.codes.CONTROL, self._keyboard.codes.KEY_V, delay=1)

    def clear(self):
        self.click()
        self._keyboard.send_keys(self._keyboard.codes.CONTROL, self._keyboard.codes.KEY_A, delay=1)
        self._keyboard.send_keys(self._keyboard.codes.DELETE)
