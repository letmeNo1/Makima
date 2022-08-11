import re
import sys


def convert_wildcard_to_regex(wildcard):
    """
    Converts wildcard to regex.

    :param str wildcard: wildcard.
    :rtype: str
    :return: regex pattern.
    """
    regex = re.escape(wildcard)
    regex = regex.replace(r'\?', r'[\s\S]{1}')
    regex = regex.replace(r'\*', r'[\s\S]*')

    return '^%s$' % regex


def replace_inappropriate_symbols(text):
    """
    Replaces inappropriate symbols e.g. \xa0 (non-breaking space) to
    normal space.

    :param str text: text in which symbols should be replaced.
    :rtype: str
    :return: processed text.
    """
    replace_pairs = [(u'\xa0', ' '),
                     (u'\u2014', '-')]

    for from_, to_ in replace_pairs:
        text = text.replace(from_, to_)

    return text


def verify_xy_coordinates(x, y):
    """
    Verifies that x and y is instance of int otherwise raises exception.

    :param x: x variable.
    :param y: y variable.
    """
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise Exception(
            'x and y arguments should hold int coordinates.')


def verify_mouse_button_name(button_name, supported_names):
    """
    Verifies that button name is supported otherwise raises exception.

    :param str button_name: button name.
    :param list[str] supported_names: supported button names.
    """
    if button_name not in supported_names:
        raise Exception(
            'Button name should be one of supported %s.' %
            repr(supported_names))