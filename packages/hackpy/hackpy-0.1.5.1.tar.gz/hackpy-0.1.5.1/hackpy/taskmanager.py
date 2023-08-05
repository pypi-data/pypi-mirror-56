import os
import random
from hackpy.info     import *
from hackpy.commands import *


class taskmanager:
    ##|
    ##| hackpy.taskmanager.enable()
    ##| hackpy.taskmanager.disable()
    ##|
    ##| hackpy.taskmanager('process_name.exe').kill()
    ##| hackpy.taskmanager('process_name.exe').start()
    ##| hackpy.taskmanager('process_name.exe').find() # return True or False
    ##| hackpy.taskmanager.list() # return all process list
    ##|
    def __init__(self, process):
        self.process = process

    def enable():
        status = command.system('@reg.exe ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /f /v "DisableTaskMgr" /t REG_DWORD /d 0' + devnull)
        if status == 0:
            return True
        else:
            return False

    def disable():
        status = command.system('@reg.exe ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /f /v "DisableTaskMgr" /t REG_DWORD /d 1' + devnull)
        if status == 0:
            return True
        else:
            return False

    def kill(self):
        status = command.system('@taskkill /F /IM ' + self.process + devnull)
        if status == 0:
            return True
        else:
            return False

    def start(self):
        status = command.system('@start ' + self.process + devnull)
        if status == 0:
            return True
        else:
            return False

    def find(self):
        process_list = taskmanager.list()
        if (self.process in process_list):
            return True
        else:
            return False

    def list():
        random_number = str(random.randint(1, 99999))
        list_path = module_location + r'\tempdata\process_list_' + random_number + '.tmp'
        command.system('@tasklist > ' + list_path)
        with open(list_path, 'r', encoding = "utf8", errors = 'ignore') as file:
            process_list = []
            for line in file.readlines():
                line = line.replace('\n', '').split()
                if (line):
                    process = line[0]
                    if (process.endswith('.exe')):
                        process_list.append(process)
        os.remove(list_path)
        return process_list