import Quartz
from apollo_makima.mac.call_mac_api.KeyCodes import KeyCodes


class MacKeyBoard:
    class _KeyCodes(object):
        """
        Holder for Windows keyboard codes stored as Keys.
        """

        BACKSPACE = KeyCodes.kVK_Delete  # BACKSPACE key
        CLEAR = KeyCodes.kVK_ANSI_KeypadClear
        TAB = KeyCodes.kVK_Tab  # TAB key
        RETURN = KeyCodes.kVK_Return  # ENTER key
        SHIFT = KeyCodes.kVK_Shift  # SHIFT key
        CONTROL = KeyCodes.kVK_Control  # CTRL key
        COMMAND = KeyCodes.kVK_Command
        ALT = KeyCodes.kVK_Option  # ALT key
        CAPS_LOCK = KeyCodes.kVK_CapsLock  # CAPS LOCK key
        ESCAPE = KeyCodes.kVK_Escape  # ESC key
        SPACE = KeyCodes.kVK_Space  # SPACEBAR
        PAGE_UP = KeyCodes.kVK_PageUp  # PAGE UP key
        PAGE_DOWN = KeyCodes.kVK_PageDown  # PAGE DOWN key
        END = KeyCodes.kVK_End  # END key
        HOME = KeyCodes.kVK_Home  # HOME key
        LEFT = KeyCodes.kVK_LeftArrow  # LEFT ARROW key
        UP = KeyCodes.kVK_UpArrow  # UP ARROW key
        RIGHT = KeyCodes.kVK_RightArrow  # RIGHT ARROW key
        DOWN = KeyCodes.kVK_DownArrow  # DOWN ARROW key
        DELETE = KeyCodes.kVK_ForwardDelete  # DEL key
        KEY_0 = KeyCodes.kVK_ANSI_0  # 0 key
        KEY_1 = KeyCodes.kVK_ANSI_1  # 1 key
        KEY_2 = KeyCodes.kVK_ANSI_2  # 2 key
        KEY_3 = KeyCodes.kVK_ANSI_3  # 3 key
        KEY_4 = KeyCodes.kVK_ANSI_4  # 4 key
        KEY_5 = KeyCodes.kVK_ANSI_5  # 5 key
        KEY_6 = KeyCodes.kVK_ANSI_6  # 6 key
        KEY_7 = KeyCodes.kVK_ANSI_7  # 7 key
        KEY_8 = KeyCodes.kVK_ANSI_8  # 8 key
        KEY_9 = KeyCodes.kVK_ANSI_9  # 9 key
        KEY_A = KeyCodes.kVK_ANSI_A  # A key
        KEY_B = KeyCodes.kVK_ANSI_B  # B key
        KEY_C = KeyCodes.kVK_ANSI_C  # C key
        KEY_D = KeyCodes.kVK_ANSI_D  # D key
        KEY_E = KeyCodes.kVK_ANSI_E  # E key
        KEY_F = KeyCodes.kVK_ANSI_F  # F key
        KEY_G = KeyCodes.kVK_ANSI_G  # G key
        KEY_H = KeyCodes.kVK_ANSI_H  # H key
        KEY_I = KeyCodes.kVK_ANSI_I  # I key
        KEY_J = KeyCodes.kVK_ANSI_J  # J key
        KEY_K = KeyCodes.kVK_ANSI_K  # K key
        KEY_L = KeyCodes.kVK_ANSI_L  # L key
        KEY_M = KeyCodes.kVK_ANSI_M  # M key
        KEY_N = KeyCodes.kVK_ANSI_N  # N key
        KEY_O = KeyCodes.kVK_ANSI_O  # O key
        KEY_P = KeyCodes.kVK_ANSI_P  # P key
        KEY_Q = KeyCodes.kVK_ANSI_Q  # Q key
        KEY_R = KeyCodes.kVK_ANSI_R  # R key
        KEY_S = KeyCodes.kVK_ANSI_S  # S key
        KEY_T = KeyCodes.kVK_ANSI_T  # T key
        KEY_U = KeyCodes.kVK_ANSI_U  # U key
        KEY_V = KeyCodes.kVK_ANSI_V  # V key
        KEY_W = KeyCodes.kVK_ANSI_W  # W key
        KEY_X = KeyCodes.kVK_ANSI_X  # X key
        KEY_Y = KeyCodes.kVK_ANSI_Y  # Y key
        KEY_Z = KeyCodes.kVK_ANSI_Z  # Z key
        NUMPAD0 = KeyCodes.kVK_ANSI_Keypad0  # Numeric keypad 0 key
        NUMPAD1 = KeyCodes.kVK_ANSI_Keypad1  # Numeric keypad 1 key
        NUMPAD2 = KeyCodes.kVK_ANSI_Keypad2  # Numeric keypad 2 key
        NUMPAD3 = KeyCodes.kVK_ANSI_Keypad3  # Numeric keypad 3 key
        NUMPAD4 = KeyCodes.kVK_ANSI_Keypad4  # Numeric keypad 4 key
        NUMPAD5 = KeyCodes.kVK_ANSI_Keypad5  # Numeric keypad 5 key
        NUMPAD6 = KeyCodes.kVK_ANSI_Keypad6  # Numeric keypad 6 key
        NUMPAD7 = KeyCodes.kVK_ANSI_Keypad7  # Numeric keypad 7 key
        NUMPAD8 = KeyCodes.kVK_ANSI_Keypad8  # Numeric keypad 8 key
        NUMPAD9 = KeyCodes.kVK_ANSI_Keypad9  # Numeric keypad 9 key
        F1 = KeyCodes.kVK_F1  # F1 key
        F2 = KeyCodes.kVK_F2  # F2 key
        F3 = KeyCodes.kVK_F3  # F3 key
        F4 = KeyCodes.kVK_F4  # F4 key
        F5 = KeyCodes.kVK_F5  # F5 key
        F6 = KeyCodes.kVK_F6  # F6 key
        F7 = KeyCodes.kVK_F7  # F7 key
        F8 = KeyCodes.kVK_F8  # F8 key
        F9 = KeyCodes.kVK_F9  # F9 key
        F10 = KeyCodes.kVK_F10  # F10 key
        F11 = KeyCodes.kVK_F11  # F11 key
        F12 = KeyCodes.kVK_F12  # F12 key
        RIGHT_SHIFT = KeyCodes.kVK_RightShift  # Right SHIFT key
        RIGHT_CONTROL = KeyCodes.kVK_RightControl  # Right CONTROL key

    codes = _KeyCodes

    class _MaskKeyCodes(object):
        """
        Holder for Windows keyboard codes stored as Keys.
        """

        COMMAND = Quartz.kCGEventFlagMaskCommand  # Command key
        SHIFT = Quartz.kCGEventFlagMaskShift  # Shift key
        OPTION = Quartz.kCGEventFlagMaskAlternate  # Option (Alt) key
        CONTROL = Quartz.kCGEventFlagMaskControl  # Control key
        CAPS_LOCK = Quartz.kCGEventFlagMaskAlphaShift  # Caps Lock key
        HELP = Quartz.kCGEventFlagMaskHelp  # Help key
        SECONDARY_FN = Quartz.kCGEventFlagMaskSecondaryFn  # Secondary Fn key

        # Other event flag masks
        NUM_LOCK = Quartz.kCGEventFlagMaskNumericPad  # Num Lock key
        NON_COALESCED = Quartz.kCGEventFlagMaskNonCoalesced  # Non-coalesced event

    mask_codes = _MaskKeyCodes

    def send_keys(self, *keycodes):
        event = Quartz.CGEventCreateKeyboardEvent(None, keycodes[0], True)
        flags = keycodes[1] if len(keycodes) >= 2 else 0
        for keycode in keycodes[2:]:
            flags |= keycode
        Quartz.CGEventSetFlags(event, flags)
        Quartz.CGEventPost(Quartz.kCGSessionEventTap, event)

    def release_keys(self, *keycodes):
        print(keycodes)
        event = Quartz.CGEventCreateKeyboardEvent(None, keycodes[0], False)
        if len(keycodes) == 4:
            Quartz.CGEventSetFlags(event, keycodes[1] | keycodes[2] | keycodes[3])
        elif len(keycodes) == 3:
            Quartz.CGEventSetFlags(event, keycodes[1] | keycodes[2])
        elif len(keycodes) == 2:
            Quartz.CGEventSetFlags(event, keycodes[1])
        Quartz.CGEventPost(Quartz.kCGSessionEventTap, event)
