import os

class autorun:
    def __init__(self, path):
        self.path = os.path.dirname(os.path.realpath(path))
        self.file = path.split('\\')[-1]
        self.name = self.file.split('.')[0]
        self.autorunDirPath = (os.environ['SystemDrive'] + '\\Users\\' + os.getenv('USERNAME') + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        self.autorunBatPath = (self.autorunDirPath + '\\' + self.name + '.cmd')
    
    # Add file to startup
    def install(self):
        if os.path.isfile(self.file):
            if (self.file.endswith('.py') or self.file.endswith('.pyw')):
                execute = 'python '
            else:
                execute = 'start \"\" '
            with open(self.autorunBatPath, 'w', encoding = "utf8", errors = 'ignore') as tempfile:
                tempfile.write(
                    '\n@echo off'     +
                    '\nchcp 65001'    +
                    '\ncd ' + self.path    +
                    '\n'    + execute + self.file
                    )
            return os.path.exists(self.autorunBatPath)
        else:
            return False

    # Delete file from startup
    def uninstall(self):
        try:
            os.remove(self.autorunBatPath)
        except:
            return False
        return not os.path.exists(self.autorunBatPath)