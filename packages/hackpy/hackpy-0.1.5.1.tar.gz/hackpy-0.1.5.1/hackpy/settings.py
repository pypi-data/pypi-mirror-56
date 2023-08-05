import os

# Main server
global server_url
server_url = 'http://f0330673.xsph.ru'

# Install path
try:
    global module_location
    module_location = os.environ['TEMP'] + '\\hackpy'
except:
    raise OSError('ERROR! Hackpy created only for Windows systems!')
