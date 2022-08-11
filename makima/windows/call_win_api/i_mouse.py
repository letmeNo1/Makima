#!/usr/bin/env python

#    Copyright (c) 2014-2017 Max Beloborodko.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

__author__ = 'f1ashhimself@gmail.com'

from abc import ABCMeta, abstractmethod, abstractproperty


class IMouse(object):
    """
    Class to simulate mouse activities.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def LEFT_BUTTON(self):
        """
        Constant for left mouse button.
        """

    @abstractproperty
    def RIGHT_BUTTON(self):
        """
        Constant for right mouse button.
        """

    @abstractmethod
    def move(self, x, y, smooth=True):
        """
        Move the mouse to the specified coordinates.

        :param int x: x coordinate.
        :param int y: y coordinate.
        :param bool smooth: indicates is it needed to simulate smooth movement.
        """

    @abstractmethod
    def drag(self, x1, y1, x2, y2, smooth=True):
        """
        Drags the mouse to the specified coordinates.

        :param int x1: x start coordinate.
        :param int y1: y start coordinate.
        :param int x2: x target coordinate.
        :param int y2: y target coordinate.
        :param bool smooth: indicates is it needed to simulate smooth movement.
        """

    @abstractmethod
    def press_button(self, x, y, button_name=LEFT_BUTTON):
        """
        Presses mouse button as dictated by coordinates and button name.

        :param int x: x coordinate to press mouse at.
        :param int y: y coordinate to press mouse at.
        :param str button_name: mouse button name. Should be one
        of: 'b1c' - left button or 'b3c' - right button.
        """

    @abstractmethod
    def release_button(self, button_name=LEFT_BUTTON):
        """
        Releases mouse button by button name.

        :param str button_name: mouse button name. Should be one
        of: 'b1c' - left button or 'b3c' - right button.
        """

    @abstractmethod
    def click(self, x, y, button_name=LEFT_BUTTON):
        """
        Clicks as dictated by coordinates and button name.

        :param int x: x coordinate to click mouse at.
        :param int y: y coordinate to click mouse at.
        :param str button_name: mouse button name. Should be one
        of: 'b1c' - left button or 'b3c' - right button.
        """

    @abstractmethod
    def double_click(self, x, y, button_name=LEFT_BUTTON):
        """
        Double-clicks as dictated by coordinates and button name.

        :param int x: x coordinate to double-click at.
        :param int y: y coordinate to double-click at.
        :param str button_name: mouse button name. Should be one
        of: 'b1c' - left button or 'b3c' - right button.
        """

    @abstractmethod
    def get_position(self):
        """
        Returns current mouse cursor position.

        :rtype: tuple[int, int]
        :return: x and y coordinates of current mouse cursor position.
        """
