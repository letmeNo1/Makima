import Quartz


def combination_key_operation(*keycodes):
    print(keycodes)
    event = Quartz.CGEventCreateKeyboardEvent(None, keycodes[0], True)
    if len(keycodes) == 4:
        Quartz.CGEventSetFlags(event, keycodes[1] | keycodes[2] | keycodes[3])
    elif len(keycodes) == 3:
        Quartz.CGEventSetFlags(event, keycodes[1] | keycodes[2])
    elif len(keycodes) == 2:
        Quartz.CGEventSetFlags(event, keycodes[1])
    Quartz.CGEventPost(Quartz.kCGSessionEventTap, event)
