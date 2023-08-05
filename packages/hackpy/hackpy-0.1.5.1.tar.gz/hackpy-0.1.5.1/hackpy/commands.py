import subprocess
from hackpy.info     import *
from hackpy.settings import *

class command:
    ##|
    ##| Execute system command : hackpy.command.system('command')
    ##| Execute nircmdc command: hackpy.command.nircmdc('command')
    ##|
    def system(recived_command):
        return subprocess.call(recived_command, shell = True)

    def nircmdc(recived_command):
        return command.system(module_location + r'\executable\nircmd.exe ' + recived_command + devnull)