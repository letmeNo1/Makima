import subprocess


class WindowOBJ:
    def __init__(self, window_info):
        self.window_info = window_info

    @property
    def get_window_title(self):
        """Get native window title."""
        owner_name = self.window_info.get("kCGWindowOwnerName")
        return owner_name

    @property
    def get_window_name(self):
        """Get native window name."""
        window_name = self.window_info.get("kCGWindowName")
        return window_name

    @property
    def get_window_id(self):
        """Get native window id."""
        return self.window_info.get("kCGWindowOwnerPID")

    @property
    def is_on_screen(self):
        return bool(self.window_info.get("kCGWindowIsOnscreen"))

    @property
    def is_minimize(self):
        return bool(self.window_info.get("kCGWindowIsOnscreen"))

    @property
    def get_bounds(self):
        h = self.window_info.get("kCGWindowBounds").get("Height")
        w = self.window_info.get("kCGWindowBounds").get("Width")
        x = self.window_info.get("kCGWindowBounds").get("X")
        y = self.window_info.get("kCGWindowBounds").get("Y")
        return h, w, x, y

    @property
    def get_owner_name(self):
        return self.window_info.get("kCGWindowOwnerName")

    @property
    def get_owner_pid(self):
        return self.window_info.get("kCGWindowOwnerPID")

    @property
    def get_window_number(self):
        return self.window_info.get("kCGWindowNumber")

    @property
    def is_maximize(self):
        from AppKit import NSScreen
        screen = NSScreen.mainScreen()
        visible_frame = screen.visibleFrame()
        width = visible_frame.size.width
        height = visible_frame.size.height
        return self.get_bounds[0] == height and self.get_bounds[1] == width

    @property
    def is_minimize(self):
        return bool(self.window_info.get("kCGWindowIsOnscreen"))

    def focus_window(self):
        # AppleScript script to activate a specific window
        script = f'''
        tell application "System Events"
            set frontmost of the first process whose unix id is {self.get_window_id} to true
        end tell
        '''
        # Run AppleScript
        subprocess.run(['osascript', '-e', script])

