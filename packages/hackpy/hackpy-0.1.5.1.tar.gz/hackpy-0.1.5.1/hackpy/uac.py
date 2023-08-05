from hackpy.commands import *

class uac:
    ##|
    ##| hackpy.uac.disable() # Disable UAC // NEED ADMIN!
    ##| hackpy.uac.enable()  # Enable  UAC // NEED ADMIN!
    ##|
    def disable():
        status = command.system('C:\\Windows\\System32\\cmd.exe /k C:\\Windows\\System32\\reg.exe ADD HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA /t REG_DWORD /d 0 /f')
        if status == 0:
            return True
        else:
            return False

    def enable():
        status = command.system('C:\\Windows\\System32\\cmd.exe /k C:\\Windows\\System32\\reg.exe ADD HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA /t REG_DWORD /d 1 /f')
        if status == 0:
            return True
        else:
            return False