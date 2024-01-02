from __future__ import annotations
import re
from typing import List

import Cocoa
import CoreFoundation
import ApplicationServices as AppServ
from PyObjCTools import AppHelper
import HIServices

from makima.helper.find_ui_element import *
from makima.mac.utils.common import MacCommon
from makima.mac.utils.mouse import *

"""
Library of Apple A11y functions
"""


def cf_attribute_to_py_oject(self, attr_value):
    def list_helper(list_value):
        list_builder = []
        for item in list_value:
            list_builder.append(cf_attribute_to_py_oject(self, item))
        return list_builder

    def number_helper(number_value):
        success, int_value = CoreFoundation.CFNumberGetValue(number_value, CoreFoundation.kCFNumberIntType, None)
        if success:
            return int(int_value)

        success, float_value = CoreFoundation.CFNumberGetValue(number_value, CoreFoundation.kCFNumberDoubleType, None)
        if success:
            return float(float_value)

        raise ErrorUnsupported('Error converting numeric attribute: {}'.format(number_value))

    def ax_ui_element_helper(element_value):
        return self.with_ref(element_value)

    cf_attr_type = AppServ.CFGetTypeID(attr_value)
    cf_type_mapping = {
        Cocoa.CFStringGetTypeID(): str,
        Cocoa.CFBooleanGetTypeID(): bool,
        Cocoa.CFArrayGetTypeID(): list_helper,
        CoreFoundation.CFNumberGetTypeID(): number_helper,
        HIServices.AXUIElementGetTypeID(): ax_ui_element_helper,
    }
    try:
        return cf_type_mapping[cf_attr_type](attr_value)
    except KeyError:
        # did not get a supported CF type. Move on to AX type
        pass

    ax_attr_type = AppServ.AXValueGetType(attr_value)
    ax_type_map = {
        "kAXValueCGSizeType": 2,
        "kAXValueCGPointType": 1,
        "kAXValueCFRangeType": 4,
    }
    try:
        extracted_str = re.search('{.*}', attr_value.description()).group()
        return {extracted_str.split()[2].split(":")[0]: float(extracted_str.split()[2].split(":")[1]),
                extracted_str.split()[3].split(":")[0]: float(extracted_str.split()[3].split(":")[1])}
    except KeyError:
        raise ErrorUnsupported('Return value not supported yet: {}'.format(ax_attr_type))


def sig_hander(sig):
    AppHelper.stopEventLoop()
    raise KeyboardInterrupt('Keyboard interrupted Run Loop')


def set_error(error_code, error_message):
    error_mapping = {
        HIServices.kAXErrorAttributeUnsupported: ErrorUnsupported,  # -25205
        HIServices.kAXErrorActionUnsupported: ErrorUnsupported,  # -25206
        HIServices.kAXErrorNotificationUnsupported: ErrorUnsupported,  # -25207
        HIServices.kAXErrorAPIDisabled: ErrorAPIDisabled,  # -25211
        HIServices.kAXErrorInvalidUIElement: ErrorInvalidUIElement,  # -25202
        HIServices.kAXErrorCannotComplete: ErrorCannotComplete,  # -25204
        HIServices.kAXErrorNotImplemented: ErrorNotImplemented,  # -25208
        HIServices.kAXErrorFailure: ErrorCommon,  # -25200

    }
    msg = '{} (AX Error {})'.format(error_message, error_code)

    raise error_mapping[error_code](msg)


class Error(Exception):
    pass


class ErrorAPIDisabled(Error):
    pass


class ErrorInvalidUIElement(Error):
    pass


class ErrorCannotComplete(Error):
    pass


class ErrorUnsupported(Error):
    pass


class ErrorNotImplemented(Error):
    pass


class ErrorCommon(Error):
    pass


class MacUIElement(object):
    """
    Apple AXUIElement object
    """
    """
    1. Factory class methods for getAppRefByPid and getSystemObject which
       properly instantiate the class.
    2. Generators and methods for finding objects for use in child classes.
    3. __getattribute__ call for invoking actions.
    4. waitFor utility based upon AX notifications.
    """

    def __init__(self, ref=None, callback_fn=None, callback_args=None, callback_kwargs=None, observer_res=None):
        self.ref = ref
        self.callbackFn = callback_fn
        self.callbackArgs = callback_args
        self.callbackKwargs = callback_kwargs
        self.observerRes = observer_res
        self.get_last_ele = None
        self.get_next_ele = None
        self._mouse = MacMouse()
        self._common = MacCommon()

    def get_attributes(self):
        """
        Get a list of the actions available on the AXUIElement
        :return:
        """
        err, attr = HIServices.AXUIElementCopyAttributeNames(self.ref, None)

        if err != AppServ.kAXErrorSuccess:
            set_error(err, 'Error retrieving attribute list')
        else:
            return list(attr)

    def get_actions(self):
        """
        Get a list of the actions available on the AXUIElement
        :return:
        """
        if self.ref is None:
            raise Error('Not a valid accessibility object')

        err, actions = HIServices.AXUIElementCopyActionNames(self.ref, None)
        if err != AppServ.kAXErrorSuccess:
            set_error(err, 'Error retrieving action names')
        else:
            return list(actions)

    def perform_action(self, action):
        """
        Perform the specified action on the AXUIElement object
        :param action:
        :return:
        """
        err = HIServices.AXUIElementPerformAction(self.ref, action)

        if err != AppServ.kAXErrorSuccess:
            set_error(err, 'Error performing requested action')

    def __get_attribute(self, attr):
        """
        Get the value of the specified attribute
        :param args:
        :return:
        """
        err, attr_value = HIServices.AXUIElementCopyAttributeValue(self.ref, attr, None)
        if err == HIServices.kAXErrorNoValue:
            return

        if err != AppServ.kAXErrorSuccess:
            if err == HIServices.kAXErrorNotImplemented:

                set_error(err, 'Attribute not implemented')
            else:
                set_error(err, 'Error retrieving attribute')
        return cf_attribute_to_py_oject(self, attr_value)

    def __set_attribute(self, attr, val):
        """
        Set the specified attribute to the specified value
        :param args:
        :return:
        """
        self.__get_attribute(attr)
        err, to_set = HIServices.AXUIElementCopyAttributeValue(self.ref, attr, None)
        if err != AppServ.kAXErrorSuccess:
            set_error(err, 'Error retrieving attribute to set')

        err, settable = HIServices.AXUIElementIsAttributeSettable(self.ref, attr, None)
        if err != AppServ.kAXErrorSuccess:
            set_error(err, 'Error querying attribute')

        if not settable:
            raise ErrorUnsupported('Attribute is not settable')

        err = HIServices.HIServices.AXUIElementSetAttributeValue(self.ref, attr, val)
        if err != AppServ.AppServ.kAXErrorSuccess:
            if err == HIServices.kAXErrorIllegalArgument:
                set_error(err, 'Invalid value for element attribute')
            set_error(err, 'Error setting attribute value')

    def __set_string(self, attribute, value):
        err = HIServices.AXUIElementSetAttributeValue(self.ref, attribute, str(value))
        if err != AppServ.kAXErrorSuccess:
            set_error(err, 'Error setting attribute to string')

    def get_pid(self):
        """
        Get the PID of the AXUIElement
        """
        error_code, pid = HIServices.AXUIElementGetPid(self.ref, None)
        if error_code != AppServ.kAXErrorSuccess:
            set_error(error_code, 'Error retrieving PID')
        return pid

    def __set_timeout(self, newTimeout):
        if self.ref is None:
            raise ErrorUnsupported('Operation not supported on null element references')

        err = HIServices.AXUIElementSetMessagingTimeout(self.ref, newTimeout)
        if err == HIServices.kAXErrorIllegalArgument:
            raise ValueError('Accessibility timeout values must be non-negative')
        if err == HIServices.kAXErrorInvalidUIElement:
            set_error(err, 'The element reference is invalid')

    def get_element_at_position(self, x, y):
        if self.ref is None:
            raise ErrorUnsupported('Operation not supported on null element references')

        err, res = HIServices.AXUIElementCopyElementAtPosition(self.ref, x, y, None)
        if err == HIServices.kAXErrorIllegalArgument:
            raise ValueError('Arguments must be two floats.')

        return self.with_ref(res)

    @property
    def get_role(self):
        try:
            return self.__get_attribute(AppServ.kAXRoleAttribute)
        except ErrorUnsupported:
            return None
        except ErrorCommon:
            return None

    def get_acc_children_elements(self):
        try:
            rst = self.__get_attribute(AppServ.kAXChildrenAttribute)

            if rst is None:
                return []
            else:
                return self.__get_attribute(AppServ.kAXChildrenAttribute)
        except ErrorUnsupported:
            return None
        except ErrorCommon:
            return None
        except ErrorCannotComplete:
            return None

    def get_position(self):
        try:
            return self.__get_attribute(AppServ.kAXPositionAttribute)
        except ErrorUnsupported:
            return None
        except ErrorCommon:
            return None

    @property
    def get_identifier(self):
        try:
            return self.__get_attribute(AppServ.kAXIdentifierAttribute)
        except ErrorUnsupported:
            return None
        except ErrorCommon:
            return None

    def get_size(self):
        return self.__get_attribute(AppServ.kAXSizeAttribute)

    @property
    def get_title(self):
        try:
            return self.__get_attribute(AppServ.kAXTitleAttribute)
        except ErrorUnsupported:
            return None
        except ErrorCommon:
            return None

    @property
    def get_value(self):
        try:
            return self.__get_attribute(AppServ.kAXValueAttribute)
        except ErrorUnsupported:
            return None
        except ErrorCommon:
            return None

    @property
    def get_label(self):
        try:
            return self.__get_attribute(AppServ.kAXLabelValueAttribute)
        except ErrorUnsupported:
            return None
        except ErrorCommon:
            return None

    @property
    def get_role_description(self):
        try:
            return self.__get_attribute(AppServ.kAXRoleDescriptionAttribute)
        except ErrorUnsupported:
            return None
        except ErrorCommon:
            return None

    def get_parent(self):
        return self.__get_attribute(AppServ.kAXParentAttribute)

    @property
    def get_help(self):
        try:
            return self.__get_attribute(AppServ.kAXHelpAttribute)
        except ErrorUnsupported:
            return None
        except ErrorCommon:
            return None

    @property
    def get_sub_role(self):
        try:
            return self.__get_attribute(AppServ.kAXSubroleAttribute)
        except ErrorUnsupported:
            return None
        except ErrorCommon:
            return None

    @property
    def get_selected(self) -> bool:
        try:
            return bool(self.__get_attribute(AppServ.kAXSelectedAttribute))
        except ErrorUnsupported:
            return None
        except ErrorCommon:
            return None

    def _set_last_ele(self, ele):
        self.get_last_ele = ele

    def _set_next_ele(self, ele):
        self.get_next_ele = ele

    def get_center_coordinates(self):
        x, y = self.get_position().get("x"), self.get_position().get("y")
        w, h = self.get_size().get("w"), self.get_size().get("h")
        x = x + w / 2
        y = y + h / 2
        return x, y

    def __get_coordinate(self, x_coordinate=None, y_coordinate=None, x_offset: float = None, y_offset: float = None):
        if x_coordinate is not None:
            x = x_coordinate
            y = y_coordinate
        else:
            x, y = self.get_center_coordinates()
            if x_offset is not None:
                x = x + x_offset
            elif y_offset is not None:
                y = y + y_offset

        return x, y

    def click(self, x_coordinate=None, y_coordinate=None, x_offset=None, y_offset=None):
        x, y = self.__get_coordinate(x_coordinate, y_coordinate, x_offset, y_offset)
        self._mouse.left_mouse_single_click_event(x, y)

    def hover(self,x_coordinate=None, y_coordinate=None, x_offset=None, y_offset=None):
        x, y = self.__get_coordinate(x_coordinate, y_coordinate, x_offset, y_offset)
        self._mouse.left_mouse_move_event(x, y)

    def double_click(self, x_coordinate=None, y_coordinate=None, x_offset=None, y_offset=None):
        x, y = self.__get_coordinate(x_coordinate, y_coordinate, x_offset, y_offset)
        self._mouse.left_mouse_double_click_event(x, y)

    def right_click(self, x_coordinate=None, y_coordinate=None, x_offset=None, y_offset=None):
        x, y = self.__get_coordinate(x_coordinate, y_coordinate, x_offset, y_offset)
        self._mouse.right_mouse_single_click_event(x, y)

    def drag_to(self,to_x, to_y, duration, x_coordinate=None, y_coordinate=None, x_offset=None, y_offset=None):
        x, y = self.__get_coordinate(x_coordinate, y_coordinate, x_offset, y_offset)
        left_mouse_dragged_event(x, y, to_x, to_y, duration)

    def input_text(self, text):
        x, y = self.get_center_coordinates
        self._common.input_text(x, y, text)

    def clear(self):
        x, y = self.get_center_coordinates
        self._common.clear(x, y)

    '''
       query:
           identifier = identifier
           help = help
           title = title
           role_description = role description
           role = role name
           sub_role = Subrole
           value = value
       '''

    def ele(self, timeout=5, **query) -> MacUIElement:
        return wait_function(timeout, find_element_by_query, self, **query)

    def eles(self, timeout=5, **query) -> List[MacUIElement]:
        elements_ref = wait_function(timeout, find_elements_by_query, self, **query)
        return elements_ref

    def check_element_exist(self, timeout=5, **query):
        rst = wait_exist(timeout, find_element_by_query, self, **query)
        return rst

    @classmethod
    def with_ref(cls, ref):
        """
        Create a new Python AXUIElement object from a given Apple AXUIElementRef
        :param ref:
        :return:
        """
        if isinstance(ref, cls):
            return cls(ref.ref)
        return cls(ref=ref)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        selr = self.ref
        othr = other.ref
        if self.ref is None and other.ref is None:
            return True

        if self.ref is None or other.ref is None:
            return False

        return CoreFoundation.CFEqual(self.ref, other.ref)

    def __ne__(self, other):
        return not self.__eq__(other)


"""
module functions
"""


def axenabled():
    """
    Return the status of accessibility on the system.
    :return: bool
    """
    return AppServ.AXIsProcessTrusted()


# callbacks
# Callback methods for notifications
def observerCallback(cls, element, contextData):
    axObj = contextData
    cb_fn = contextData.callbackFn
    cb_args = contextData.callbackArgs
    cb_kwargs = contextData.callbackKwargs
    if cb_fn is not None:
        retElem = cls.with_ref(element)
        if retElem is None:
            raise RuntimeError('Could not create new AX UI Element.')

        cb_args = (retElem,) + cb_args
        callbackRes = cb_fn(cb_args, cb_kwargs)

        if callbackRes is None:
            raise RuntimeError('Python callback failed.')

        if callbackRes in (-1, 1):
            AppHelper.stopEventLoop()

        temp = axObj.observerRes
        axObj.observerRes = callbackRes
    else:
        AppHelper.stopEventLoop()
        temp = axObj.observerRes
        axObj.observerRes = True
