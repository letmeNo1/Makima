import ctypes
from ctypes import *
from ctypes.wintypes import HWND, CHAR, LPSTR, DWORD, RECT
from loguru import logger
import os
import signal

# Constants for GetWindowLongW
GWL_STYLE = -16
GWL_EXSTYLE = -20

class HWND_OBJ:
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.window_name = self.get_window_title

    @property
    def get_window_title(self):
        """Get native window title."""
        cb = windll.user32.GetWindowTextLengthW(self.hwnd) + 1
        title = create_unicode_buffer(cb)
        windll.user32.GetWindowTextW(self.hwnd, title, cb)
        return title.value

    @property
    def get_window_class_name(self):
        _GetClassNameA = windll.user32.GetClassNameA
        _GetClassNameA.argtypes = [HWND, LPSTR, ctypes.c_int]
        _GetClassNameA.restype = ctypes.c_int

        nMaxCount = 0x1000
        dwCharSize = sizeof(CHAR)
        while 1:
            lpClassName = create_string_buffer(nMaxCount)
            nCount = _GetClassNameA(self.hwnd, lpClassName, nMaxCount)
            if nCount == 0:
                raise WinError()
            if nCount < nMaxCount - dwCharSize:
                break
            nMaxCount += 0x1000
        return str(lpClassName.value)

    def focus_window(self, flag=None):
        # "flag" is used in old driver, need to keep it.
        import pygetwindow as gw
        # Find the target window by exact title match
        window = next(win for win in gw.getAllWindows() if win.title == self.window_name)
        logger.debug(f"Window found: {self.window_name}")
        
        # Check if window is minimized and restore if necessary
        if window.isMinimized:
            logger.debug(f"Window {self.window_name} is minimized, restoring it")
            window.restore()
        
        # Activate the window to bring it to foreground
        logger.debug(f"Activating window: {self.window_name}")
        window.activate()
        
        # Ensure the window is visible
        logger.debug(f"Ensuring window is visible: {self.window_name}")
        window.show()
        

    def show_window(self, cmd_show):
        """Maximize or minimize windows
            SW_HIDE = 0
            SW_SHOWNORMAL = 1
            SW_SHOWMINIMIZED = 2
            SW_SHOWMAXIMIZED = 3
            SW_SHOWNOACTIVATE = 4
            SW_SHOW = 5
            SW_MINIMIZE = 6
            SW_SHOWMINNOACTIVE = 7
            SW_SHOWNA = 8
            SW_RESTORE = 9
            SW_SHOWDEFAULT = 10
        """

        user32 = windll.LoadLibrary("user32.dll")
        user32.ShowWindow(self.hwnd, cmd_show)

    def get_pid(self):
        """Retrieve the process ID (PID) corresponding to the window handle (hwnd)"""
        lpdw_process_id = DWORD()
        # Get the thread ID and process ID associated with the window
        windll.user32.GetWindowThreadProcessId(self.hwnd, byref(lpdw_process_id))
        pid = lpdw_process_id.value
        if pid == 0:
            logger.warning(f"Failed to get PID for window handle {self.hwnd}")
        return pid

    def close_window(self):
        """Close the window by obtaining its PID and terminating the process"""
        logger.debug(f"Window handle: {self.hwnd}")  # Output the window handle

        # Get the corresponding PID
        pid = self.get_pid()
        if not pid:
            return False

        logger.debug(f"Obtained PID: {pid}")
        logger.debug(f"Attempting to terminate process with PID: {pid}")

        try:
            # Send termination signal
            os.kill(pid, signal.SIGTERM)  # Graceful termination signal
            logger.debug(f"Termination signal sent to process {pid}")

            # Verify if the process has been terminated
            import psutil  # Requires psutil library (install via pip install psutil)
            if psutil.pid_exists(pid):
                # Force termination if still running
                os.kill(pid, signal.SIGKILL)
                logger.debug(f"Process {pid} forcefully terminated")
            return True

        except PermissionError:
            logger.error(f"Permission denied to terminate process {pid}. Please run as administrator.")
            return False
        except ProcessLookupError:
            logger.debug(f"Process {pid} does not exist or has already terminated")
            return True
        except Exception as e:
            logger.error(f"Error terminating process {pid}: {str(e)}")
            return False
    
    def get_window_status(self):
        """Retrieve current window status information and return as a dictionary"""
        user32 = windll.LoadLibrary("user32.dll")
        
        # Get window rectangle (position and size)
        rect = ctypes.wintypes.RECT()
        user32.GetWindowRect(self.hwnd, byref(rect))
        width = rect.right - rect.left
        height = rect.bottom - rect.top
        
        # Get window styles
        style = user32.GetWindowLongW(self.hwnd, GWL_STYLE)
        ex_style = user32.GetWindowLongW(self.hwnd, GWL_EXSTYLE)
        
        # Check window states
        is_visible = user32.IsWindowVisible(self.hwnd) != 0
        is_minimized = user32.IsIconic(self.hwnd) != 0
        is_maximized = user32.IsZoomed(self.hwnd) != 0
        is_active = user32.GetForegroundWindow() == self.hwnd
        
        # Get PID
        pid = self.get_pid()
        
        # Construct status dictionary
        status = {
            "window_title": self.window_name,
            "hwnd": self.hwnd,
            "class_name": self.get_window_class_name,
            "pid": pid,
            "position": {
                "left": rect.left,
                "top": rect.top,
                "right": rect.right,
                "bottom": rect.bottom
            },
            "size": {
                "width": width,
                "height": height
            },
            "states": {
                "visible": is_visible,
                "minimized": is_minimized,
                "maximized": is_maximized,
                "active": is_active
            },
            "styles": {
                "style": style,
                "ex_style": ex_style
            }
        }
        
        return status
    