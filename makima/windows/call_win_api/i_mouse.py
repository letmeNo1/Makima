import abc
from abc import ABCMeta, abstractmethod, abstractproperty


class IMouse(object):
    """
    Class to simulate mouse activities.
    """

    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def LEFT_BUTTON(self):
        """
        Constant for left mouse button.
        """

    @abc.abstractmethod
    def RIGHT_BUTTON(self):
        """
        Constant for right mouse button.
        """

    @abc.abstractmethod
    def move(self, x, y, smooth=True):
        """
        Move the mouse to the specified coordinates.

        :param int x: x coordinate.
        :param int y: y coordinate.
        :param bool smooth: indicates is it needed to simulate smooth movement.
        """

    @abc.abstractmethod
    def drag(self, x1, y1, x2, y2, smooth=True):
        """
        Drags the mouse to the specified coordinates.

        :param int x1: x start coordinate.
        :param int y1: y start coordinate.
        :param int x2: x target coordinate.
        :param int y2: y target coordinate.
        :param bool smooth: indicates is it needed to simulate smooth movement.
        """

    @abc.abstractmethod
    def press_button(self, x, y, button_name=LEFT_BUTTON):
        """
        Presses mouse button as dictated by coordinates and button name.

        :param int x: x coordinate to press mouse at.
        :param int y: y coordinate to press mouse at.
        :param str button_name: mouse button name. Should be one
        of: 'b1c' - left button or 'b3c' - right button.
        """

    @abc.abstractmethod
    def release_button(self, button_name=LEFT_BUTTON):
        """
        Releases mouse button by button name.

        :param str button_name: mouse button name. Should be one
        of: 'b1c' - left button or 'b3c' - right button.
        """

    @abc.abstractmethod
    def click(self, x, y, button_name=LEFT_BUTTON):
        """
        Clicks as dictated by coordinates and button name.

        :param int x: x coordinate to click mouse at.
        :param int y: y coordinate to click mouse at.
        :param str button_name: mouse button name. Should be one
        of: 'b1c' - left button or 'b3c' - right button.
        """

    @abc.abstractmethod
    def double_click(self, x, y, button_name=LEFT_BUTTON):
        """
        Double-clicks as dictated by coordinates and button name.

        :param int x: x coordinate to double-click at.
        :param int y: y coordinate to double-click at.
        :param str button_name: mouse button name. Should be one
        of: 'b1c' - left button or 'b3c' - right button.
        """

    @abc.abstractmethod
    def get_position(self):
        """
        Returns current mouse cursor position.

        :rtype: tuple[int, int]
        :return: x and y coordinates of current mouse cursor position.
        """
