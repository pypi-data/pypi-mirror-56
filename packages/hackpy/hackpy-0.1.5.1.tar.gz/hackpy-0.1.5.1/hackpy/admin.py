import ctypes

# Check if program started as admin
def isAdmin():
    status = ctypes.windll.shell32.IsUserAnAdmin()
    if (status == 1):
        return True
    else:
        return False

# Set wallpaper
def setWallpaper(image):
    return ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 0)
