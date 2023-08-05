import time
import ctypes
import win32gui

# Get cursor position
def getCursorPos():
    return win32gui.GetCursorPos()

# Set cursor position
def setCursorPos(x, y):
    return ctypes.windll.user32.SetCursorPos(x, y)

# Get active window
def getActiveWindow():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())


# Check if human use computer
def userIsActive(wait = 2):
    first_x, first_y = getCursorPos()
    time.sleep(wait)
    last_x, last_y   = getCursorPos()

    if first_x != last_x or first_y != last_y:
        return True
    else:
        return False
