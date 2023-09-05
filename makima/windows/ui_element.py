#!/usr/bin/env python
import time
from collections import deque
from xml.dom import minidom

import comtypes.client

from makima.helper.find_ui_element import wait_function, find_element_by_query, find_elements_by_query, \
    wait_function_by_image, find_element_by_image
from makima.windows.utils.mouse import WinMouse
from makima.windows.utils.keyboard import WinKeyboard

import comtypes.client


CO_E_OBJNOTCONNECTED = -2147220995
UIAutomationCore = comtypes.client.GetModule("UIAutomationCore.dll")
IUIAutomation = comtypes.client.CreateObject("{ff48dba4-60ef-4201-aa87-54103eef594e}",
                                             interface=UIAutomationCore.IUIAutomation)

_IUIAutomation = comtypes.CoCreateInstance(comtypes.gen.UIAutomationClient.CUIAutomation._reg_clsid_,
                                           interface=comtypes.gen.UIAutomationClient.IUIAutomation,
                                           clsctx=comtypes.CLSCTX_INPROC_SERVER)

UIAutomationClient = comtypes.gen.UIAutomationClient

_control_type = {
    UIAutomationClient.UIA_ButtonControlTypeId: 'UIA_ButtonControlTypeId',
    UIAutomationClient.UIA_CalendarControlTypeId: 'UIA_CalendarControlTypeId',
    UIAutomationClient.UIA_CheckBoxControlTypeId: 'UIA_CheckBoxControlTypeId',
    UIAutomationClient.UIA_ComboBoxControlTypeId: 'UIA_ComboBoxControlTypeId',
    UIAutomationClient.UIA_CustomControlTypeId: 'UIA_CustomControlTypeId',
    UIAutomationClient.UIA_DataGridControlTypeId: 'UIA_DataGridControlTypeId',
    UIAutomationClient.UIA_DataItemControlTypeId: 'UIA_DataItemControlTypeId',
    UIAutomationClient.UIA_DocumentControlTypeId: 'UIA_DocumentControlTypeId',
    UIAutomationClient.UIA_EditControlTypeId: 'UIA_EditControlTypeId',
    UIAutomationClient.UIA_GroupControlTypeId: 'UIA_GroupControlTypeId',
    UIAutomationClient.UIA_HeaderControlTypeId: 'UIA_HeaderControlTypeId',
    UIAutomationClient.UIA_HeaderItemControlTypeId: 'UIA_HeaderItemControlTypeId',
    UIAutomationClient.UIA_HyperlinkControlTypeId: 'UIA_HyperlinkControlTypeId',
    UIAutomationClient.UIA_ImageControlTypeId: 'UIA_ImageControlTypeId',
    UIAutomationClient.UIA_ListControlTypeId: 'UIA_ListControlTypeId',
    UIAutomationClient.UIA_ListItemControlTypeId: 'UIA_ListItemControlTypeId',
    UIAutomationClient.UIA_MenuBarControlTypeId: 'UIA_MenuBarControlTypeId',
    UIAutomationClient.UIA_MenuControlTypeId: 'UIA_MenuControlTypeId',
    UIAutomationClient.UIA_MenuItemControlTypeId: 'UIA_MenuItemControlTypeId',
    UIAutomationClient.UIA_PaneControlTypeId: 'UIA_PaneControlTypeId',
    UIAutomationClient.UIA_ProgressBarControlTypeId: 'UIA_ProgressBarControlTypeId',
    UIAutomationClient.UIA_RadioButtonControlTypeId: 'UIA_RadioButtonControlTypeId',
    UIAutomationClient.UIA_ScrollBarControlTypeId: 'UIA_ScrollBarControlTypeId',
    UIAutomationClient.UIA_SeparatorControlTypeId: 'UIA_SeparatorControlTypeId',
    UIAutomationClient.UIA_SliderControlTypeId: 'UIA_SliderControlTypeId',
    UIAutomationClient.UIA_SpinnerControlTypeId: 'UIA_SpinnerControlTypeId',
    UIAutomationClient.UIA_SplitButtonControlTypeId: 'UIA_SplitButtonControlTypeId',
    UIAutomationClient.UIA_StatusBarControlTypeId: 'UIA_StatusBarControlTypeId',
    UIAutomationClient.UIA_TabControlTypeId: 'UIA_TabControlTypeId',
    UIAutomationClient.UIA_TabItemControlTypeId: 'UIA_TabItemControlTypeId',
    UIAutomationClient.UIA_TableControlTypeId: 'UIA_TableControlTypeId',
    UIAutomationClient.UIA_TextControlTypeId: 'UIA_TextControlTypeId',
    UIAutomationClient.UIA_ThumbControlTypeId: 'UIA_ThumbControlTypeId',
    UIAutomationClient.UIA_TitleBarControlTypeId: 'UIA_TitleBarControlTypeId',
    UIAutomationClient.UIA_ToolBarControlTypeId: 'UIA_ToolBarControlTypeId',
    UIAutomationClient.UIA_ToolTipControlTypeId: 'UIA_ToolTipControlTypeId',
    UIAutomationClient.UIA_TreeControlTypeId: 'UIA_TreeControlTypeId',
    UIAutomationClient.UIA_TreeItemControlTypeId: 'UIA_TreeItemControlTypeId',
    UIAutomationClient.UIA_WindowControlTypeId: 'UIA_WindowControlTypeId'
}
class Property_Id:
    """
    PropertyId from IUIAutomation.
    Refer https://docs.microsoft.com/en-us/windows/win32/winauto/uiauto-automation-element-propids
    Refer https://docs.microsoft.com/en-us/windows/win32/winauto/uiauto-control-pattern-propids
    """
    AcceleratorKeyProperty = 30006
    AccessKeyProperty = 30007
    AnnotationAnnotationTypeIdProperty = 30113
    AnnotationAnnotationTypeNameProperty = 30114
    AnnotationAuthorProperty = 30115
    AnnotationDateTimeProperty = 30116
    AnnotationObjectsProperty = 30156
    AnnotationTargetProperty = 30117
    AnnotationTypesProperty = 30155
    AriaPropertiesProperty = 30102
    AriaRoleProperty = 30101
    AutomationIdProperty = 30011
    BoundingRectangleProperty = 30001
    CenterPointProperty = 30165
    ClassNameProperty = 30012
    ClickablePointProperty = 30014
    ControlTypeProperty = 30003
    ControllerForProperty = 30104
    CultureProperty = 30015
    DescribedByProperty = 30105
    DockDockPositionProperty = 30069
    DragDropEffectProperty = 30139
    DragDropEffectsProperty = 30140
    DragGrabbedItemsProperty = 30144
    DragIsGrabbedProperty = 30138
    DropTargetDropTargetEffectProperty = 30142
    DropTargetDropTargetEffectsProperty = 30143
    ExpandCollapseExpandCollapseStateProperty = 30070
    FillColorProperty = 30160
    FillTypeProperty = 30162
    FlowsFromProperty = 30148
    FlowsToProperty = 30106
    FrameworkIdProperty = 30024
    FullDescriptionProperty = 30159
    GridColumnCountProperty = 30063
    GridItemColumnProperty = 30065
    GridItemColumnSpanProperty = 30067
    GridItemContainingGridProperty = 30068
    GridItemRowProperty = 30064
    GridItemRowSpanProperty = 30066
    GridRowCountProperty = 30062
    HasKeyboardFocusProperty = 30008
    HelpTextProperty = 30013
    IsAnnotationPatternAvailableProperty = 30118
    IsContentElementProperty = 30017
    IsControlElementProperty = 30016
    IsCustomNavigationPatternAvailableProperty = 30151
    IsDataValidForFormProperty = 30103
    IsDockPatternAvailableProperty = 30027
    IsDragPatternAvailableProperty = 30137
    IsDropTargetPatternAvailableProperty = 30141
    IsEnabledProperty = 30010
    IsExpandCollapsePatternAvailableProperty = 30028
    IsGridItemPatternAvailableProperty = 30029
    IsGridPatternAvailableProperty = 30030
    IsInvokePatternAvailableProperty = 30031
    IsItemContainerPatternAvailableProperty = 30108
    IsKeyboardFocusableProperty = 30009
    IsLegacyIAccessiblePatternAvailableProperty = 30090
    IsMultipleViewPatternAvailableProperty = 30032
    IsObjectModelPatternAvailableProperty = 30112
    IsOffscreenProperty = 30022
    IsPasswordProperty = 30019
    IsPeripheralProperty = 30150
    IsRangeValuePatternAvailableProperty = 30033
    IsRequiredForFormProperty = 30025
    IsScrollItemPatternAvailableProperty = 30035
    IsScrollPatternAvailableProperty = 30034
    IsSelectionItemPatternAvailableProperty = 30036
    IsSelectionPattern2AvailableProperty = 30168
    IsSelectionPatternAvailableProperty = 30037
    IsSpreadsheetItemPatternAvailableProperty = 30132
    IsSpreadsheetPatternAvailableProperty = 30128
    IsStylesPatternAvailableProperty = 30127
    IsSynchronizedInputPatternAvailableProperty = 30110
    IsTableItemPatternAvailableProperty = 30039
    IsTablePatternAvailableProperty = 30038
    IsTextChildPatternAvailableProperty = 30136
    IsTextEditPatternAvailableProperty = 30149
    IsTextPattern2AvailableProperty = 30119
    IsTextPatternAvailableProperty = 30040
    IsTogglePatternAvailableProperty = 30041
    IsTransformPattern2AvailableProperty = 30134
    IsTransformPatternAvailableProperty = 30042
    IsValuePatternAvailableProperty = 30043
    IsVirtualizedItemPatternAvailableProperty = 30109
    IsWindowPatternAvailableProperty = 30044
    ItemStatusProperty = 30026
    ItemTypeProperty = 30021
    LabeledByProperty = 30018
    LandmarkTypeProperty = 30157
    LegacyIAccessibleChildIdProperty = 30091
    LegacyIAccessibleDefaultActionProperty = 30100
    LegacyIAccessibleDescriptionProperty = 30094
    LegacyIAccessibleHelpProperty = 30097
    LegacyIAccessibleKeyboardShortcutProperty = 30098
    LegacyIAccessibleNameProperty = 30092
    LegacyIAccessibleRoleProperty = 30095
    LegacyIAccessibleSelectionProperty = 30099
    LegacyIAccessibleStateProperty = 30096
    LegacyIAccessibleValueProperty = 30093
    LevelProperty = 30154
    LiveSettingProperty = 30135
    LocalizedControlTypeProperty = 30004
    LocalizedLandmarkTypeProperty = 30158
    MultipleViewCurrentViewProperty = 30071
    MultipleViewSupportedViewsProperty = 30072
    NameProperty = 30005
    NativeWindowHandleProperty = 30020
    OptimizeForVisualContentProperty = 30111
    OrientationProperty = 30023
    OutlineColorProperty = 30161
    OutlineThicknessProperty = 30164
    PositionInSetProperty = 30152
    ProcessIdProperty = 30002
    ProviderDescriptionProperty = 30107
    RangeValueIsReadOnlyProperty = 30048
    RangeValueLargeChangeProperty = 30051
    RangeValueMaximumProperty = 30050
    RangeValueMinimumProperty = 30049
    RangeValueSmallChangeProperty = 30052
    RangeValueValueProperty = 30047
    RotationProperty = 30166
    RuntimeIdProperty = 30000
    ScrollHorizontalScrollPercentProperty = 30053
    ScrollHorizontalViewSizeProperty = 30054
    ScrollHorizontallyScrollableProperty = 30057
    ScrollVerticalScrollPercentProperty = 30055
    ScrollVerticalViewSizeProperty = 30056
    ScrollVerticallyScrollableProperty = 30058
    Selection2CurrentSelectedItemProperty = 30171
    Selection2FirstSelectedItemProperty = 30169
    Selection2ItemCountProperty = 30172
    Selection2LastSelectedItemProperty = 30170
    SelectionCanSelectMultipleProperty = 30060
    SelectionIsSelectionRequiredProperty = 30061
    SelectionItemIsSelectedProperty = 30079
    SelectionItemSelectionContainerProperty = 30080
    SelectionSelectionProperty = 30059
    SizeOfSetProperty = 30153
    SizeProperty = 30167
    SpreadsheetItemAnnotationObjectsProperty = 30130
    SpreadsheetItemAnnotationTypesProperty = 30131
    SpreadsheetItemFormulaProperty = 30129
    StylesExtendedPropertiesProperty = 30126
    StylesFillColorProperty = 30122
    StylesFillPatternColorProperty = 30125
    StylesFillPatternStyleProperty = 30123
    StylesShapeProperty = 30124
    StylesStyleIdProperty = 30120
    StylesStyleNameProperty = 30121
    TableColumnHeadersProperty = 30082
    TableItemColumnHeaderItemsProperty = 30085
    TableItemRowHeaderItemsProperty = 30084
    TableRowHeadersProperty = 30081
    TableRowOrColumnMajorProperty = 30083
    ToggleToggleStateProperty = 30086
    Transform2CanZoomProperty = 30133
    Transform2ZoomLevelProperty = 30145
    Transform2ZoomMaximumProperty = 30147
    Transform2ZoomMinimumProperty = 30146
    TransformCanMoveProperty = 30087
    TransformCanResizeProperty = 30088
    TransformCanRotateProperty = 30089
    ValueIsReadOnlyProperty = 30046
    ValueValueProperty = 30045
    VisualEffectsProperty = 30163
    WindowCanMaximizeProperty = 30073
    WindowCanMinimizeProperty = 30074
    WindowIsModalProperty = 30077
    WindowIsTopmostProperty = 30078
    WindowWindowInteractionStateProperty = 30076
    WindowWindowVisualStateProperty = 30075



_tree_scope = {
    'ancestors': UIAutomationClient.TreeScope_Ancestors,
    'children': UIAutomationClient.TreeScope_Children,
    'descendants': UIAutomationClient.TreeScope_Descendants,
    'element': UIAutomationClient.TreeScope_Element,
    'parent': UIAutomationClient.TreeScope_Parent,
    'subtree': UIAutomationClient.TreeScope_Subtree
}


class WinUIElement(object):
    def __init__(self, IUIAutomationElement):
        self.IUIAutomationElement = IUIAutomationElement
        self.current_hwnd = None

    _mouse = WinMouse()
    _keyboard = WinKeyboard()

    def set_current_hwnd(self, hwnd):
        self.current_hwnd = hwnd

    @property
    def get_current_hwnd(self):
        return self.current_hwnd

    @property
    def get_CachedNativeWindowHandle(self):
        hwnd = self.IUIAutomationElement.CurrentNativeWindowHandle
        return hwnd

    @property
    def get_toggle_state(self):
        """Retrieves the UI Automation element value
        :rtype : unicode
        """
        IUnknown = self.IUIAutomationElement.GetCurrentPattern(UIAutomationClient.UIA_TogglePatternId)
        IUIAutomationTogglePattern = IUnknown.QueryInterface(UIAutomationClient.IUIAutomationTogglePattern)
        return IUIAutomationTogglePattern.CurrentToggleState

    CurrentToggleState = get_toggle_state

    @property
    def get_acc_value(self):
        """Retrieves the UI Automation element value
        :rtype : unicode
        """
        IUnknown = self.IUIAutomationElement.GetCurrentPattern(UIAutomationClient.UIA_TextPatternId)
        IUIAutomationTextPattern = IUnknown.QueryInterface(UIAutomationClient.IUIAutomationTextPattern)
        return IUIAutomationTextPattern.DocumentRange.getText(-1)

    CurrentValue = get_acc_value

    @property
    def get_automation_id(self):
        """Retrieves the UI Automation identifier of the element
        :rtype : unicode
        """
        return self.IUIAutomationElement.CurrentAutomationId

    AutomationId = get_automation_id

    @property
    def get_acc_location(self):
        """Retrieves the coordinates of the rectangle that completely encloses the element.
        Returns tuple (left, top, right, bottom)
        :rtype : tuple
        """
        rect = self.IUIAutomationElement.CurrentBoundingRectangle
        return rect.left, rect.top, rect.right, rect.bottom

    BoundingRectangle = get_acc_location

    @property
    def get_class_name(self):
        """Retrieves the class name of the element
        :rtype : unicode
        """
        return self.IUIAutomationElement.CurrentClassName

    ClassName = get_class_name

    @property
    def get_control_type(self):
        """Retrieves the control type of the element
        :rtype : int
        """
        return self.IUIAutomationElement.CurrentControlType

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
        return bool(self.IUIAutomationElement.CurrentIsEnabled)

    IsEnabled = get_is_enabled

    @property
    def get_acc_name(self):
        """Retrieves the name of the element
        :rtype : unicode
        """
        return self.IUIAutomationElement.CurrentName

    Name = get_acc_name

    @property
    def get_default_action(self):
        IUnknown = self.IUIAutomationElement.GetCurrentPattern(UIAutomationClient.UIA_LegacyIAccessiblePatternId)
        IUIAutomationLegacyIAccessiblePattern = IUnknown.QueryInterface(
            UIAutomationClient.IUIAutomationLegacyIAccessiblePattern)
        return str(IUIAutomationLegacyIAccessiblePattern.CurrentDefaultAction)

    DefaultAction = get_default_action

    def set_value(self, value):
        """Retrieves the UI Automation element value
        :rtype : unicode
        """
        IUnknown = self.IUIAutomationElement.GetCurrentPattern(UIAutomationClient.UIA_ValuePatternId)
        IUIAutomationValuePattern = IUnknown.QueryInterface(UIAutomationClient.IUIAutomationValuePattern)
        IUIAutomationValuePattern.SetValue(value)

    def get_clickable_point(self):
        """Retrieves a point on the element that can be clicked
        Returns tuple (x, y) if a clickable point was retrieved, or None otherwise
        :rtype : tuple
        """
        point = self.IUIAutomationElement.GetClickablePoint()
        if point[1]:
            return point[0].x, point[0].y
        else:
            return None

    @property
    def get_description(self):
        return self.get_iaccessible_property(Property_Id.LegacyIAccessibleDescriptionProperty)

    def get_iaccessible_property(self, propertyId):
        return self.IUIAutomationElement.GetCurrentPropertyValue(propertyId)
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

    def findfirst(self, tree_scope, Name=None, ControlType=None, AutomationId=None):
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
        element = self.IUIAutomationElement.FindFirst(tree_scope, condition)
        return WinUIElement(element) if element else None

    #
    def findall(self, tree_scope, Name=None, ControlType=None, AutomationId=None):
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

        IUIAutomationElementArray = self.IUIAutomationElement.FindAll(tree_scope, condition)
        return [WinUIElement(IUIAutomationElementArray.GetElement(i)) for i in
                range(IUIAutomationElementArray.Length)]

    def Invoke(self):
        IUnknown = self.IUIAutomationElement.GetCurrentPattern(UIAutomationClient.UIA_InvokePatternId)
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
            for child in element.findall('children'):
                queue.append((child, xml_element))
        return xml.toprettyxml()

    def get_acc_children_elements(self):
        return self.findall("children")

    @property
    def get_CachedNativeWindowHandle(self):
        hwnd = self.IUIAutomationElement.CurrentNativeWindowHandle
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
        return wait_function_by_image(timeout,  find_element_by_image, path, distance, algorithms_name)

    def find_element_by_wait(self, timeout=5000, use_re=False, **query):
        return wait_function(timeout, use_re, find_element_by_query, self, **query)

    def find_next_element_by_wait(self, timeout=5000, use_re=False, **query):
        return wait_function(timeout, use_re, find_element_by_query, self, "next", **query)

    def find_last_element_by_wait(self, timeout=5000, use_re=False, **query):
        return wait_function(timeout, use_re, find_element_by_query, self, "last", **query)

    def find_elements_by_wait(self, timeout=5000, use_re=False, **query):
        return wait_function(timeout, use_re, find_elements_by_query, self, **query)

    def click(self, need_move=False, x_offset=None, y_offset=None):
        if x_offset is not None:
            x = x_offset
            y = y_offset
        else:
            rect = self.get_acc_location
            x = rect[0] + (rect[2] - rect[0]) / 2
            y = rect[1] + (rect[3] - rect[1]) / 2

        self._mouse.click(x, y, need_move)

    def hover(self, need_move=False, x_offset=None, y_offset=None):
        if x_offset is not None:
            x = x_offset
            y = y_offset
        else:
            rect = self.get_acc_location

            x = rect[0] + (rect[2] - rect[0]) / 2
            y = rect[1] + (rect[3] - rect[1]) / 2
            print(x, y)

        self._mouse.move(x, y, need_move)

    def input(self, content, x_offset=None, y_offset=None):
        if x_offset is not None:
            x = x_offset
            y = y_offset
        else:
            rect = self.get_acc_location
            x = rect[0] + (rect[2] - rect[0]) / 2
            y = rect[1] + (rect[3] - rect[1]) / 2
        self._mouse.click(x, y)
        self._keyboard.copy_text(content)
        time.sleep(1)
        self._keyboard.send(self._keyboard.codes.CONTROL.modify(self._keyboard.codes.KEY_V), delay=1)

    def right_click(self, need_move=False, x_offset=None, y_offset=None):
        if x_offset is not None:
            x = x_offset
            y = y_offset
        else:
            rect = self.get_acc_location
            x = rect[0] + (rect[2] - rect[0]) / 2
            y = rect[1] + (rect[3] - rect[1]) / 2
        self._mouse.click(x, y, need_move, self._mouse.RIGHT_BUTTON)

    def double_click(self, x_offset=None, y_offset=None):
        if x_offset is not None:
            x = x_offset
            y = y_offset
        else:
            rect = self.get_acc_location
            x = rect[0] + (rect[2] - rect[0]) / 2
            y = rect[1] + (rect[3] - rect[1]) / 2
        self._mouse.double_click(x, y)

    def drag_to(self, x2, y2, x_offset=None, y_offset=None, smooth=True):
        if x_offset is not None:
            x = x_offset
            y = y_offset
        else:
            rect = self.get_acc_location
            x = rect[0] + (rect[2] - rect[0]) / 2
            y = rect[1] + (rect[3] - rect[1]) / 2
        self._mouse.drag(x, y, x2, y2, smooth)

    def input_text(self, text):
        self.click()
        self._keyboard.copy_text(text)
        self._keyboard.send(self._keyboard.codes.CONTROL.modify(self._keyboard.codes.KEY_V),delay=1)

    def clear(self):
        self.click()
        self._keyboard.send(self._keyboard.codes.CONTROL.modify(self._keyboard.codes.KEY_A),delay=1)
        self._keyboard.send(self._keyboard.codes.DELETE)



