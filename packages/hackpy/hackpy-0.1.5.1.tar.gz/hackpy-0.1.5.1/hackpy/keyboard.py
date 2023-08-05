import os
from hackpy.commands import *
from hackpy.settings import *

# SendKey
def sendKey(key):
    ##|
    ##| SendKey('Hello my L0rd!!{ENTER}')
    ##| All keys: https://pastebin.com/Ns3P7UiH
    ##|
    tempfile = module_location + r'\tempdata\keyboard.vbs'
    with open(tempfile, 'w', encoding = "utf8", errors = 'ignore') as keyboard_path:
        keyboard_path.write('WScript.CreateObject(\"WScript.Shell\").SendKeys \"' + str(key) + '\"')
    command.system(tempfile)
    os.remove(tempfile)
