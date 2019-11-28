from os import getenv
from shutil import copyfile
import sqlite3
import win32crypt

original_cookie = getenv("LOCALAPPDATA") + "/Google/Chrome/User Data/Default/Cookies"
copyfile(original_cookie, './DecryptedCookies')

with sqlite3.connect('./DecryptedCookies') as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT host_key, name, value, encrypted_value FROM cookies')
    for host_key, name, value, encrypted_value in cursor.fetchall():
        # Decrypt
        decrypted_value = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode('utf-8') or ''

        sql = '''UPDATE cookies
                 SET value = ?
                 WHERE host_key = ? AND name = ?'''
        cursor.execute(sql, (decrypted_value, host_key, name))

    conn.commit()
