import os
import logging
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Hash import SHA256, HMAC

# Configuration
key_size = 32  # AES key size in bytes (256 bits)
block_size = 16  # AES block size in bytes
decryption_directory = '.'  # Directory to decrypt
log_file = 'decryption.log'  # Log file to track decryption progress

# Set up logging
logging.basicConfig(filename=log_file, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class DecryptionError(Exception):
    """Custom exception for decryption errors."""
    pass

def decrypt_file(file_path, key):
    try:
        with open(file_path, 'rb') as file:
            iv = file.read(block_size)
            ciphertext = file.read()

        # Create the cipher object
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Decrypt the ciphertext
        padded_data = cipher.decrypt(ciphertext)
        
        # Unpad the decrypted data
        data = unpad(padded_data, block_size)

        # Verify integrity using HMAC
        meta_file_path = file_path + '.meta'
        if not os.path.exists(meta_file_path):
            raise DecryptionError(f"Meta file not found for {file_path}")
        
        with open(meta_file_path, 'rb') as meta_file:
            stored_key = meta_file.read(key_size)
            stored_hmac = meta_file.read()

            if stored_key != key:
                raise DecryptionError(f"Key mismatch for {file_path}")

            # Verify the HMAC to check file integrity
            hmac = HMAC.new(key, digestmod=SHA256)
            hmac.update(ciphertext)
            
            try:
                hmac.verify(stored_hmac)
            except ValueError:
                raise DecryptionError(f"Integrity check failed for {file_path}")

        # Write decrypted data back to the file
        with open(file_path, 'wb') as file:
            file.write(data)

        # Log successful decryption
        logging.info(f"File decrypted successfully: {file_path}")

        # Clean up the metadata file
        os.remove(meta_file_path)
    
    except Exception as e:
        logging.error(f"Decryption failed for {file_path}: {e}")
        print(f"Decryption failed for {file_path}: {e}")

def traverse_directory_and_decrypt(directory):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            key_file_path = file_path + '.key'

            if os.path.exists(key_file_path):
                with open(key_file_path, 'rb') as key_file:
                    key = key_file.read()

                # Decrypt the file
                decrypt_file(file_path, key)

                # Remove the key file after successful decryption
                os.remove(key_file_path)

if __name__ == "__main__":
    # Check if the decryption directory exists
    if not os.path.exists(decryption_directory):
        logging.error(f"Directory not found: {decryption_directory}")
        print(f"Directory not found: {decryption_directory}")
    else:
        traverse_directory_and_decrypt(decryption_directory)
        print("Decryption completed.")