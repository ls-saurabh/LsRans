import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

key_size = 32
block_size = 16

class DecryptionError(Exception):
    pass

def decrypt_file(file_path, key):
    try:
        with open(file_path, 'rb') as file:
            iv = file.read(block_size)
            ciphertext = file.read()

        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = cipher.decrypt(ciphertext)
        data = unpad(padded_data, block_size)

        with open(file_path, 'wb') as file:
            file.write(data)
    except Exception as e:
        print(f"Decryption failed for {file_path}: {e}")

# Decrypt files
for root, dirs, files in os.walk('.'):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        key_file_path = file_path + '.key'

        if os.path.exists(key_file_path):
            with open(key_file_path, 'rb') as key_file:
                key = key_file.read()

            decrypt_file(file_path, key)
            os.remove(key_file_path)

print("Decryption completed.")