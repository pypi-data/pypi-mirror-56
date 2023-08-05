import os
from hackpy.info     import *
from hackpy.network  import *
from hackpy.settings import *
from hackpy.commands import *

# Python
class python:
    def install(version = '3.7.0', path = os.environ['SystemDrive'] + '\\python'):
        ##|
        ##| Install python to system
        ##| Example: hackpy.install_python(version = '3.6.0', path = 'C:\\python36')
        ##| Default version is: 3.7.0 and install path is: C:\python
        ##|
        setup = module_location + r'\tempdata\python_setup.exe'
        wget_download('https://www.python.org/ftp/python/' + version + '/python-' + version + '.exe', bar = None, out = setup)
        command.system(setup + ' /quiet TargetDir=' + path + ' PrependPath=1 Include_test=0 Include_pip=1')
        os.remove(setup)

    def check():
        ##|
        ##| Check if python installed in system
        ##| Example: hackpy.check_python()
        ##| return True if installed and False if not installed
        ##|
        status = command.system('python --version' + devnull)
        if status == 0:
            return True
        else:
            return False