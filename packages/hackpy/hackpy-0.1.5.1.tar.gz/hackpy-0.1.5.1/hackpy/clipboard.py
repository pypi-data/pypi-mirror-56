import pyperclip


##|
##| hackpy.clipboard.set('Text') # Copy text to clipboard
##| print('Data in clipboard:' + clipboard.get()) # Get text from clipboard
##|
def set(text):
    pyperclip.copy(text)

def get():
    return pyperclip.paste()
