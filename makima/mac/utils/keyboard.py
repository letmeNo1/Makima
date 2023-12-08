import Quartz

class MacKeyBoard:
    def combination_key_operation(self,*keycodes):
        event = Quartz.CGEventCreateKeyboardEvent(None, keycodes[0], True)
        flags = keycodes[1] if len(keycodes) >= 2 else 0
        for keycode in keycodes[2:]:
            flags |= keycode
        Quartz.CGEventSetFlags(event, flags)
        Quartz.CGEventPost(Quartz.kCGSessionEventTap, event)
        # Quartz.CFRelease(event)

    def combination_key_operation_release(self,*keycodes):
        print(keycodes)
        event = Quartz.CGEventCreateKeyboardEvent(None, keycodes[0], False)
        if len(keycodes) == 4:
            Quartz.CGEventSetFlags(event, keycodes[1] | keycodes[2] | keycodes[3])
        elif len(keycodes) == 3:
            Quartz.CGEventSetFlags(event, keycodes[1] | keycodes[2])
        elif len(keycodes) == 2:
            Quartz.CGEventSetFlags(event, keycodes[1])
        Quartz.CGEventPost(Quartz.kCGSessionEventTap, event)
