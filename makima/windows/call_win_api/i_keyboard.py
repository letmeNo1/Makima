from abc import ABCMeta, abstractmethod


class Key(object):
    """
    Decorator class to specify modifier key relations.
    """

    def __init__(self, hex_key_code):
        self.code = hex_key_code
        self.children = None

    def modify(self, *args):
        """
        Specifies Keys that will be modified by a current key.

        :param args: Keys to be modified by current key.
        :rtype: Key
        :return: New instance of Key with children Keys to be modified.
        """
        for arg in args:
            if not isinstance(arg, Key):
                raise Exception('Key instance is expected.')

        modified_key_press = Key(self.code)
        modified_key_press.children = args
        return modified_key_press


class IKeyboard(object):

    __metaclass__ = ABCMeta

    def codes(self):
        """
        Container class to store KeyCodes as Keys class.
        """

    @abstractmethod
    def press_key(self, hex_key_code):
        """
        Presses (and releases) key specified by a hex code.

        :param int hex_key_code: integer value holding hexadecimal code for 
        a key to be pressed.
        """

    @abstractmethod
    def press_key_and_hold(self, hex_key_code):
        """
        Presses (and holds) key specified by a hex code.

        :param int hex_key_code: integer value holding hexadecimal code for 
        a key to be pressed.
        """

    @abstractmethod
    def release_key(self, hex_key_code):
        """
        Releases key specified by a hex code.

        :param int hex_key_code: integer value holding hexadecimal code for 
        a key to be released.
        """

    @abstractmethod
    def send(self, *args, **kwargs):
        """
        Send key events as specified by Keys.

        If Key contains children Keys they will be recursively
        processed with current Key code pressed as a modifier key.

        :param args: Keys to send.
        :param kwargs: "delay" between keys in seconds.
        """
