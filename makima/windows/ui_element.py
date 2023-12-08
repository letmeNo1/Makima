#!/usr/bin/env python
from __future__ import annotations

from collections import deque
from xml.dom import minidom

import comtypes.client
from makima.windows.static_variable import state_dict, _control_type, property_id, _tree_scope

from makima.windows.utils.mouse import WinMouse
from makima.windows.utils.keyboard import WinKeyboard

import comtypes.client

from makima.helper.find_ui_element import *

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
        self.mouse = WinMouse()
        self.keyboard = WinKeyboard()
        self.get_last_ele = None
        self.get_next_ele = None


    def __get_state_text(self, state_code):
        state_text = []
        for code, text in state_dict.items():
            if state_code & code:
                state_text.append(text)
        return state_text

    def set_current_hwnd(self, hwnd):
        self.current_hwnd = hwnd

    @property
    def get_current_hwnd(self):
        return self.current_hwnd

    @property
    def get_CachedNativeWindowHandle(self):
        hwnd = self.__IUIAutomationElement.CurrentNativeWindowHandle
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
        IUnknown = self.__IUIAutomationElement.GetCurrentPattern(UIAutomationClient.UIA_TextPatternId)
        IUIAutomationTextPattern = IUnknown.QueryInterface(UIAutomationClient.IUIAutomationTextPattern)
        return IUIAutomationTextPattern.DocumentRange.getText(-1)

    CurrentValue = get_acc_value

    @property
    def get_automation_id(self):
        """Retrieves the UI Automation identifier of the element
        :rtype : unicode
        """
        return self.__IUIAutomationElement.CurrentAutomationId

    AutomationId = get_automation_id

    @property
    def get_acc_location(self):
        """Retrieves the coordinates of the rectangle that completely encloses the element.
        Returns tuple (left, top, right, bottom)
        :rtype : tuple
        """
        rect = self.__IUIAutomationElement.CurrentBoundingRectangle
        return rect.left, rect.top, rect.right, rect.bottom

    BoundingRectangle = get_acc_location

    @property
    def get_class_name(self):
        """Retrieves the class name of the element
        :rtype : unicode
        """
        return self.__IUIAutomationElement.CurrentClassName

    ClassName = get_class_name

    @property
    def get_control_type(self):
        """Retrieves the control type of the element
        :rtype : int
        """
        return self.__IUIAutomationElement.CurrentControlType

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
        return bool(self.__IUIAutomationElement.CurrentIsEnabled)

    IsEnabled = get_is_enabled

    @property
    def get_acc_name(self):
        """Retrieves the name of the element
        :rtype : unicode
        """
        return self.__IUIAutomationElement.CurrentName

    Name = get_acc_name

    @property
    def get_default_action(self):
        IUnknown = self.__IUIAutomationElement.GetCurrentPattern(UIAutomationClient.UIA_LegacyIAccessiblePatternId)
        IUIAutomationLegacyIAccessiblePattern = IUnknown.QueryInterface(
            UIAutomationClient.IUIAutomationLegacyIAccessiblePattern)
        return str(IUIAutomationLegacyIAccessiblePattern.CurrentDefaultAction)

    DefaultAction = get_default_action

    def set_value(self, value):
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

    def set_last_ele(self,ele):
         self.get_last_ele = ele
        
    def set_next_ele(self,ele):
         self.get_next_ele = ele


    @property
    def get_description(self):
        return self.get_iaccessible_property(property_id.LegacyIAccessibleDescriptionProperty)

    @property
    def get_acc_role(self):
        return self.__IUIAutomationElement.CurrentAriaRole

    @property
    def get_state(self):
        return self.__get_state_text(self.get_iaccessible_property(property_id["LegacyIAccessibleStateProperty"]))

    def get_iaccessible_property(self, propertyId):
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

    def Invoke(self):
        IUnknown = self.__IUIAutomationElement.GetCurrentPattern(UIAutomationClient.UIA_InvokePatternId)
        IUIAutomationInvokePattern = IUnknown.QueryInterface(UIAutomationClient.IUIAutomationInvokePattern)
        IUIAutomationInvokePattern.Invoke()

    def __str__(self):
        return '<%s (Name: %s, Class: %s, AutomationId: %s>' % (
            self.get_control_type_name, self.get_acc_name, self.get_class_name, self.get_automation_id)

    def toxml(self):
        xml = minidom.Document()
        queue = deque()
        queue.append((self, xml))
        while queue:
            element, xml_node = queue.popleft()
            xml_element = minidom.Element(element.CurrentControlTypeName)
            xml_element.setAttribute('Name', str(element.CurrentName))
            xml_element.setAttribute('AutomationId', str(element.CurrentAutomationId))
            xml_element.setAttribute('ClassName', str(element.CurrentClassName))
            xml_element.ownerDocument = xml
            xml_node.appendChild(xml_element)
            for child in element.__findall('children'):
                queue.append((child, xml_element))
        return xml.toprettyxml()

    def get_acc_children_elements(self):
        return self.__findall("children")

    @property
    def get_CachedNativeWindowHandle(self):
        hwnd = self.__IUIAutomationElement.CurrentNativeWindowHandle
        return hwnd

    '''
    query:
        automation_id=automation id
        acc_name=acc name
        acc_value=acc value
        class_name=class name
        control_type_name=control type name
    '''

    def find_element_by_image_by_wait(self, path, timeout=5000, distance=0.4, algorithms_name="SIFT"):
        return wait_function_by_image(timeout, find_element_by_image, path, distance, algorithms_name)

    def find_element_by_wait(self, timeout=5000, **query) -> WinUIElement:
        return wait_function(timeout, find_element_by_query, self, **query)

    def find_elements_by_wait(self, timeout=5000, **query) -> WinUIElement:
        return wait_function(timeout, find_elements_by_query, self, **query)

    def check_element_exist(self, timeout=5000, **query):
        rst = False
        try:
            ele = wait_function(timeout, find_elements_by_query, self, **query)
            if ele:
                rst = True
        except:
            rst = False
        return rst

    def scroll_to_find_element(self, scroll_time=15, timeout=5000, **query):
        for i in range(int(scroll_time)):
            ele = wait_function(timeout, find_element_by_query, self, **query)
            if "invisible" not in ele.get_state:
                return ele
            else:
                self.keyboard.send_keys(self.keyboard.codes.DOWN)

        return None

    def click(self, need_move=False, x_offset=None, y_offset=None):
        if x_offset is not None:
            x = x_offset
            y = y_offset
        else:
            rect = self.get_acc_location
            x = rect[0] + (rect[2] - rect[0]) / 2
            y = rect[1] + (rect[3] - rect[1]) / 2

        self.mouse.click(x, y, need_move)

    def hover(self, need_move=False, x_offset=None, y_offset=None):
        if x_offset is not None:
            x = x_offset
            y = y_offset
        else:
            rect = self.get_acc_location

            x = rect[0] + (rect[2] - rect[0]) / 2
            y = rect[1] + (rect[3] - rect[1]) / 2
            print(x, y)

        self.mouse.move(x, y, need_move)

    def input(self, content, x_offset=None, y_offset=None):
        if x_offset is not None:
            x = x_offset
            y = y_offset
        else:
            rect = self.get_acc_location
            x = rect[0] + (rect[2] - rect[0]) / 2
            y = rect[1] + (rect[3] - rect[1]) / 2
        self.mouse.click(x, y)
        self.keyboard.copy_text(content)
        time.sleep(1)
        self.keyboard.send(self.keyboard.codes.CONTROL.modify(self.keyboard.codes.KEY_V), delay=1)

    def right_click(self, need_move=False, x_offset=None, y_offset=None):
        if x_offset is not None:
            x = x_offset
            y = y_offset
        else:
            rect = self.get_acc_location
            x = rect[0] + (rect[2] - rect[0]) / 2
            y = rect[1] + (rect[3] - rect[1]) / 2
        self.mouse.click(x, y, need_move, self.mouse.RIGHT_BUTTON)

    def double_click(self, x_offset=None, y_offset=None):
        if x_offset is not None:
            x = x_offset
            y = y_offset
        else:
            rect = self.get_acc_location
            x = rect[0] + (rect[2] - rect[0]) / 2
            y = rect[1] + (rect[3] - rect[1]) / 2
        self.mouse.double_click(x, y)

    def drag_to(self, x2, y2, x_offset=None, y_offset=None, smooth=True):
        if x_offset is not None:
            x = x_offset
            y = y_offset
        else:
            rect = self.get_acc_location
            x = rect[0] + (rect[2] - rect[0]) / 2
            y = rect[1] + (rect[3] - rect[1]) / 2
        self.mouse.drag(x, y, x2, y2, smooth)

    def input_text(self, text):
        self.click()
        self.keyboard.copy_text(text)
        self.keyboard.send(self.keyboard.codes.CONTROL.modify(self.keyboard.codes.KEY_V), delay=1)

    def clear(self):
        self.click()
        self.keyboard.send(self.keyboard.codes.CONTROL.modify(self.keyboard.codes.KEY_A), delay=1)
        self.keyboard.send(self.keyboard.codes.DELETE)



