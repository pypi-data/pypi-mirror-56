import os
import shutil
import ctypes

class file:
    ##|
    ##| hackpy.file.exists('file.txt') # return True/False
    ##| hackpy.file.remove('file.txt')
    ##| hackpy.file.rename('file.txt', 'newfile.txt')
    ##| hackpy.file.copy('file.txt', 'C:\\Windows')
    ##| hackpy.file.scan('C:\') # return files in dict
    ##| hackpy.file.start('file.txt') 
    ##| hackpy.file.startAsAdmin('file.txt')
    ##| hackpy.file.atributeHidden('file.txt')
    ##| hackpy.file.atributeNormal('file.txt')
    ##| hackpy.file.get_drives() # return dict with all drives
    ##|

    def exists(file):
        return os.path.exists(file)

    def remove(file):
        return os.remove(file)

    def rename(oldFile, newFile):
        return os.rename(oldFile, newFile)

    def copy(src, dst):
        return shutil.copy(src, dst)

    def scan(path):
        return os.listdir(path)

    def mkdir(dir):
        return os.mkdir(dir)

    def start(file):
        return os.startfile(file)

    def startAsAdmin(file):
        status = ctypes.windll.shell32.ShellExecuteW(None, "runas", file, '', None, 1)
        if (status == 42):
            return True, 'User allowed'
        elif (status == 5):
            return False, 'User denied'
        elif (status == 31):
            return False, 'Invalid file type'
        elif (status == 2):
            return False, 'File not found'
        else:
            return False, status

    def get_drives():
        drives = []
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        letter = ord('A')
        while bitmask > 0:
            if bitmask & 1:
                drives.append(chr(letter) + ':\\')
            bitmask >>= 1
            letter += 1
        return drives

    def atributeNormal(file):
        return ctypes.windll.kernel32.SetFileAttributesW(file, 1)

    def atributeHidden(file):
        return ctypes.windll.kernel32.SetFileAttributesW(file, 2)
