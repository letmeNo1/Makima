import ctypes
from time import sleep

from apollo_makima.windows.call_win_api.i_keyboard import IKeyboard, Key

send_input = ctypes.windll.user32.SendInput
pointer_unsigned_long = ctypes.POINTER(ctypes.c_ulong)


class KeyboardInput(ctypes.Structure):
    """
    Keyboard input C struct definition.
    """

    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", pointer_unsigned_long)]


class HardwareInput(ctypes.Structure):
    """
    Hardware input C struct definition.
    """

    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    """
    Hardware input C struct definition.
    """

    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", pointer_unsigned_long)]


class EventStorage(ctypes.Union):
    """
    Event storage C struct definition.
    """

    _fields_ = [("ki", KeyboardInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    """
    Input C struct definition.
    """

    _fields_ = [("type", ctypes.c_ulong),
                ("ii", EventStorage)]


class WinKeyboard(IKeyboard):

    class _KeyCodes(object):
        """
        Holder for Windows keyboard codes stored as Keys.
        """

        BACKSPACE = Key(0x08)  # BACKSPACE key
        TAB = Key(0x09)  # TAB key
        CLEAR = Key(0x0C)  # CLEAR key
        RETURN = Key(0x0D)  # ENTER key
        SHIFT = Key(0x10)  # SHIFT key
        CONTROL = Key(0x11)  # CTRL key
        ALT = Key(0x12)  # ALT key
        PAUSE = Key(0x13)  # PAUSE key
        CAPS_LOCK = Key(0x14)  # CAPS LOCK key
        ESCAPE = Key(0x1B)  # ESC key
        SPACE = Key(0x20)  # SPACEBAR
        PAGE_UP = Key(0x21)  # PAGE UP key
        PAGE_DOWN = Key(0x22)  # PAGE DOWN key
        END = Key(0x23)  # END key
        HOME = Key(0x24)  # HOME key
        LEFT = Key(0x25)  # LEFT ARROW key
        UP = Key(0x26)  # UP ARROW key
        RIGHT = Key(0x27)  # RIGHT ARROW key
        DOWN = Key(0x28)  # DOWN ARROW key
        PRINT_SCREEN = Key(0x2C)  # PRINT SCREEN key
        INSERT = Key(0x2D)  # INS key
        DELETE = Key(0x2E)  # DEL key
        VK_HELP = Key(0x2F)  # HELP key
        KEY_0 = Key(0x30)  # 0 key
        KEY_1 = Key(0x31)  # 1 key
        KEY_2 = Key(0x32)  # 2 key
        KEY_3 = Key(0x33)  # 3 key
        KEY_4 = Key(0x34)  # 4 key
        KEY_5 = Key(0x35)  # 5 key
        KEY_6 = Key(0x36)  # 6 key
        KEY_7 = Key(0x37)  # 7 key
        KEY_8 = Key(0x38)  # 8 key
        KEY_9 = Key(0x39)  # 9 key
        KEY_A = Key(0x41)  # A key
        KEY_B = Key(0x42)  # B key
        KEY_C = Key(0x43)  # C key
        KEY_D = Key(0x44)  # D key
        KEY_E = Key(0x45)  # E key
        KEY_F = Key(0x46)  # F key
        KEY_G = Key(0x47)  # G key
        KEY_H = Key(0x48)  # H key
        KEY_I = Key(0x49)  # I key
        KEY_J = Key(0x4A)  # J key
        KEY_K = Key(0x4B)  # K key
        KEY_L = Key(0x4C)  # L key
        KEY_M = Key(0x4D)  # M key
        KEY_N = Key(0x4E)  # N key
        KEY_O = Key(0x4F)  # O key
        KEY_P = Key(0x50)  # P key
        KEY_Q = Key(0x51)  # Q key
        KEY_R = Key(0x52)  # R key
        KEY_S = Key(0x53)  # S key
        KEY_T = Key(0x54)  # T key
        KEY_U = Key(0x55)  # U key
        KEY_V = Key(0x56)  # V key
        KEY_W = Key(0x57)  # W key
        KEY_X = Key(0x58)  # X key
        KEY_Y = Key(0x59)  # Y key
        KEY_Z = Key(0x5A)  # Z key
        LEFT_WIN = Key(0x5B)  # Left Windows key (Natural keyboard)
        RIGHT_WIN = Key(0x5C)  # Right Windows key (Natural keyboard)
        SLEEP = Key(0x5F)  # Computer Sleep key
        NUMPAD0 = Key(0x60)  # Numeric keypad 0 key
        NUMPAD1 = Key(0x61)  # Numeric keypad 1 key
        NUMPAD2 = Key(0x62)  # Numeric keypad 2 key
        NUMPAD3 = Key(0x63)  # Numeric keypad 3 key
        NUMPAD4 = Key(0x64)  # Numeric keypad 4 key
        NUMPAD5 = Key(0x65)  # Numeric keypad 5 key
        NUMPAD6 = Key(0x66)  # Numeric keypad 6 key
        NUMPAD7 = Key(0x67)  # Numeric keypad 7 key
        NUMPAD8 = Key(0x68)  # Numeric keypad 8 key
        NUMPAD9 = Key(0x69)  # Numeric keypad 9 key
        MULTIPLY = Key(0x6A)  # Multiply key
        ADD = Key(0x6B)  # Add key
        SEPARATOR = Key(0x6C)  # Separator key
        SUBTRACT = Key(0x6D)  # Subtract key
        DECIMAL = Key(0x6E)  # Decimal key
        DIVIDE = Key(0x6F)  # Divide key
        F1 = Key(0x70)  # F1 key
        F2 = Key(0x71)  # F2 key
        F3 = Key(0x72)  # F3 key
        F4 = Key(0x73)  # F4 key
        F5 = Key(0x74)  # F5 key
        F6 = Key(0x75)  # F6 key
        F7 = Key(0x76)  # F7 key
        F8 = Key(0x77)  # F8 key
        F9 = Key(0x78)  # F9 key
        F10 = Key(0x79)  # F10 key
        F11 = Key(0x7A)  # F11 key
        F12 = Key(0x7B)  # F12 key
        NUM_LOCK = Key(0x90)  # NUM LOCK key
        SCROLL_LOCK = Key(0x91)  # SCROLL LOCK
        LEFT_SHIFT = Key(0xA0)  # Left SHIFT key
        RIGHT_SHIFT = Key(0xA1)  # Right SHIFT key
        LEFT_CONTROL = Key(0xA2)  # Left CONTROL key
        RIGHT_CONTROL = Key(0xA3)  # Right CONTROL key
        OEM_1 = Key(0xBA)  # For the US standard keyboard, the ';:' key
        OEM_PLUS = Key(0xBB)  # For any country/region, the '+' key
        OEM_COMMA = Key(0xBC)  # For any country/region, the ',' key
        OEM_MINUS = Key(0xBD)  # For any country/region, the '-' key
        OEM_PERIOD = Key(0xBE)  # For any country/region, the '.' key
        OEM_2 = Key(0xBF)  # For the US standard keyboard, the '/?' key
        OEM_3 = Key(0xC0)  # For the US standard keyboard, the '`~' key
        OEM_4 = Key(0xDB)  # For the US standard keyboard, the '[{' key
        OEM_5 = Key(0xDC)  # For the US standard keyboard, the '\|' key
        OEM_6 = Key(0xDD)  # For the US standard keyboard, the ']}' key
        OEM_7 = Key(0xDE)  # For the US standard keyboard, the ''/"' key

    codes = _KeyCodes

    def press_key(self, hex_key_code):
        """
        Presses (and releases) key specified by a hex code.

        :param int hex_key_code: hexadecimal code for a key to be pressed.
        """
        self.press_key_and_hold(hex_key_code)
        self.release_key(hex_key_code)

    def press_key_and_hold(self, hex_key_code):
        """
        Presses (and holds) key specified by a hex code.

        :param int hex_key_code: hexadecimal code for a key to be pressed.
        """
        extra = ctypes.c_ulong(0)
        ii_ = EventStorage()
        ii_.ki = KeyboardInput(hex_key_code, 0x48, 0, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        send_input(1, ctypes.pointer(x), ctypes.sizeof(x))

    def release_key(self, hex_key_code):
        """
        Releases key specified by a hex code.

        :param int hex_key_code: hexadecimal code for a key to be pressed.
        """
        extra = ctypes.c_ulong(0)
        ii_ = EventStorage()
        ii_.ki = KeyboardInput(
            hex_key_code, 0x48, 0x0002, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        send_input(1, ctypes.pointer(x), ctypes.sizeof(x))

    def __create_key_combo(self, *keys):
        key_combo = keys[-1]
        for key in reversed(keys[:-1]):
            key_combo = key.modify(key_combo)
        return key_combo

    def __send(self, *args, **kwargs):
        """
        Send key events as specified by Keys.

        If Key contains children Keys they will be recursively
        processed with current Key code pressed as a modifier key.

        :param args: keys to send.
        """
        delay = kwargs.get('delay', 0)

        for key in args:
            if key.children:
                self.press_key_and_hold(key.code)
                self.__send(*key.children)
                self.release_key(key.code)
            else:
                self.press_key(key.code)
            self._wait_for_key_combo_to_be_processed()
            sleep(delay)

    def send_keys(self, *keys, **kwargs):
        key_combo = self.__create_key_combo(*keys)
        self.__send(key_combo, **kwargs)


    @staticmethod
    def _wait_for_key_combo_to_be_processed():
        # For key combinations timeout is needed to be processed.
        # This method is expressive shortcut to be used where needed.
        sleep(.05)

    @staticmethod
    def copy_text(string):
        import pyperclip
        pyperclip.copy(string)
