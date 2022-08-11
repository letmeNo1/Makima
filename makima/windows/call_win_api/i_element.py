#!/usr/bin/env python

import abc
from abc import ABCMeta, abstractmethod, abstractproperty
import xml.dom.minidom

from comtypes import IUnknown


class IElement(IUnknown):
    """
    Class that describes UI object.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def click(self, x_offset=None, y_offset=None):
        """
        Clicks by left mouse button on this object.

        :param int x_offset: if not defined half of element width will be used.
        :param int y_offset: y offset, if not defined half of element height 
        will be used.
        """

    @abstractmethod
    def right_click(self, x_offset=None, y_offset=None):
        """
        Clicks by right mouse button on this object.

        :param int x_offset: if not defined half of element width will be used.
        :param int y_offset: y offset, if not defined half of element height 
        will be used.
        """

    @abstractmethod
    def double_click(self, x_offset=None, y_offset=None):
        """
        Double clicks by left mouse button on this object.

        :param int x_offset: if not defined half of element width will be used.
        :param int y_offset: y offset, if not defined half of element height 
        will be used
        """

    @abstractmethod
    def drag_to(self, x, y, x_offset=None, y_offset=None, smooth=True):
        """
        Drags this object to coordinates.

        :param int x: x coordinate.
        :param int y: y coordinate.
        :param int x_offset: if not defined half of element width will be used.
        :param int y_offset: if not defined half of element height 
        will be used.
        :param bool smooth: indicates is it needed to simulate smooth movement.
        """

    @abc.abstractmethod
    def proc_id(self):
        """
        Indicates process id.
        """

    @abc.abstractmethod
    def is_top_level_window(self):
        """
        Indicates is top level window or not.
        """

    @abc.abstractmethod
    def is_selected(self):
        """
        Indicates selected state.
        """

    @abc.abstractmethod
    def is_checked(self):
        """
        Indicates checked state.
        """

    @abc.abstractmethod
    def is_visible(self):
        """
        Indicates visible state.
        """

    @abc.abstractmethod
    def is_enabled(self):
        """
        Indicates enabled state.
        """

    @abc.abstractmethod
    def acc_parent_count(self):
        """
        Property for parent child count.
        """

    @abc.abstractmethod
    def acc_child_count(self):
        """
        Property for element child count.
        """

    @abc.abstractmethod
    def acc_name(self):
        """
        Property for element name.
        Also need to specify setter for this property
        """

    @abstractmethod
    def set_focus(self):
        """
        Sets focus to element.
        """

    @abc.abstractmethod
    def acc_location(self):
        """
        Property for element location.
        """

    @abc.abstractmethod
    def acc_value(self):
        """
        Property for element value.
        Also need to specify setter for this property.
        """

    @abstractmethod
    def set_value(self, value):
        """
        Sets element value.

        :param str value: element value.
        """

    @abc.abstractmethod
    def acc_description(self):
        """
        Property for element description.
        """

    @abc.abstractmethod
    def acc_parent(self):
        """
        Property for element parent.
        """

    @abc.abstractmethod
    def acc_selection(self):
        """
        Property for element selection.
        """

    @abc.abstractmethod
    def acc_focused_element(self):
        """
        Property for element in focus.
        """

    @abc.abstractmethod
    def acc_role_name(self):
        """
        Property for element role name.
        """

    @abstractmethod
    def __iter__(self):
        """Iterate all child Element"""

    @abstractmethod
    def is_object_exists(self, **kwargs):
        """
        Verifies is object exists.

        :param bool only_visible: flag that indicates will we search only
        through visible elements.
        :param str role: string or lambda e.g. lambda x: x == 13
        :param str name: string or lambda.
        :param str c_name: string or lambda.
        :param str location: string or lambda.
        :param str value: string or lambda.
        :param str description: string or lambda.
        :param str selection: string or lambda.
        :param str role_name: string or lambda.
        :param str parent_count: string or lambda.
        :param str child_count: string or lambda.
        :rtype: bool
        :return: True if object exists otherwise False.
        """

    def toxml(self):
        """
        Convert Element Tree to XML.
        """
        obj_document = xml.dom.minidom.Document()
        lst_queue = [(self, obj_document)]

        while lst_queue:
            obj_element, obj_tree = lst_queue.pop(0)
            role_name = obj_element.acc_role_name
            obj_name = obj_element.acc_name
            str_name = str(obj_name) if obj_name else ''
            str_location = ','.join(str(x) for x in obj_element.acc_location)
            obj_sub_tree = xml.dom.minidom.Element(role_name)
            obj_sub_tree.ownerDocument = obj_document

            try:
                obj_sub_tree.attributes['Name'] = str_name
            except:
                obj_sub_tree.attributes['Name'] = \
                    str_name.encode('unicode-escape')

            obj_sub_tree.attributes['Location'] = str_location
            obj_tree.appendChild(obj_sub_tree)

            if obj_element.acc_child_count:
                for obj_element_child in obj_element:
                    lst_queue.append((obj_element_child, obj_sub_tree))

        return obj_document.toprettyxml()
