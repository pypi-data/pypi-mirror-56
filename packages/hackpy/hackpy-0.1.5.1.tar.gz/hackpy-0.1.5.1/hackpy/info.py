import os
import platform

# System information
userInfo         = os.getenv('USERNAME')
versionInfo      = platform.version()
releaseInfo      = platform.release()
systemInfo       = platform.system()
nodeInfo         = platform.node()
machineInfo      = platform.machine()
processorInfo    = platform.processor()
platformInfo     = platform.platform()
architectureInfo = platform.architecture()
devnull          = ' > ' + os.devnull + ' 2>&1'