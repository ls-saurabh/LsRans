import os
import logging
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Hash import SHA256
from Crypto.Hash import HMAC

# Configuration
key_size = 32  # AES key size in bytes (256 bits)
block_size = 16  # AES block size in bytes
encryption_directory = 'C:\\Users\\Username\\Documents'  # Directory to encrypt
log_file = 'encryption.log'  # Log file to track encryption progress

# Set up logging
logging.basicConfig(filename=log_file, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def encrypt_file(file_path, key):
    try:
        # Read the file content
        with open(file_path, 'rb') as file:
            data = file.read()

        # Pad the data to match the block size
        padded_data = pad(data, block_size)

        # Create a cipher object with a new IV
        cipher = AES.new(key, AES.MODE_CBC)
        
        # Encrypt the padded data
        ciphertext = cipher.encrypt(padded_data)

        # Write the IV and the encrypted data to the file
        with open(file_path, 'wb') as file:
            file.write(cipher.iv + ciphertext)

        # Generate HMAC for integrity check
        hmac = HMAC.new(key, digestmod=SHA256)
        hmac.update(ciphertext)
        
        # Store the HMAC and key securely
        with open(file_path + '.meta', 'wb') as meta_file:
            meta_file.write(key + hmac.digest())

        logging.info(f"File encrypted successfully: {file_path}")
    
    except Exception as e:
        logging.error(f"Encryption failed for {file_path}: {e}")
        print(f"Encryption failed for {file_path}: {e}")

def traverse_directory_and_encrypt(directory):
    # Generate a random key once and store it securely (mock example)
    key = get_random_bytes(key_size)
    
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            encrypt_file(file_path, key)

if __name__ == "__main__":
    # Check if the encryption directory exists
    if not os.path.exists(encryption_directory):
        logging.error(f"Directory not found: {encryption_directory}")
        print(f"Directory not found: {encryption_directory}")
    else:
        traverse_directory_and_encrypt(encryption_directory)
        print("Encryption completed.")