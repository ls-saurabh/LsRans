#### Table of Contents
- Overview
- Features
- Requirements
- Installation
- Usage
- Security Considerations
- Future Enhancements

---

### Overview

This Python program provides functionality for securely encrypting and decrypting files using AES (Advanced Encryption Standard) in CBC (Cipher Block Chaining) mode. It is designed to be used on directories of files, encrypting or decrypting each file with a specified key. It also includes mechanisms for ensuring file integrity using HMAC (Hash-based Message Authentication Code).

### Features

- AES-256 Encryption: Uses a secure 256-bit key for encryption and decryption, ensuring strong protection of your files.
- CBC Mode: AES encryption is performed in CBC mode for added security by using a unique initialization vector (IV) for each file.
- Padding: Automatic padding of file contents to match the AES block size (16 bytes).
- HMAC Integrity Check: The program ensures that files have not been tampered with by calculating and verifying HMACs.
- Logging: Both encryption and decryption processes are logged, with errors and successes written to respective log files (encryption.log and decryption.log).
- Key and Metadata Management: Each file has a corresponding .meta file that stores the encryption key and HMAC, enhancing file security.
- Cross-Platform: The program is designed to be cross-platform and should work on Windows, Linux, and macOS.

### Requirements

- Python 3.7+
- Required Libraries:
  - pycryptodome (for cryptographic operations)

To install the necessary libraries, run:

```
pip install pycryptodome
```

### Installation
 
```
1. git clone https://github.com/ls-saurabh/LsRans
```
2. Install dependencies using pip:

```
pip install pycryptodome
```

3. Modify configuration settings:
   - The encryption and decryption directories are set by default in the script. Update the paths as necessary in the encryption_directory and decryption_directory variables.

### Usage

1. Encrypting Files:
   - To encrypt all files in a directory, run the encryption script:

```
python encrypt.py
```

   - This will recursively encrypt all files in the specified directory and create metadata (.meta) and key (.key) files for each encrypted file. The AES encryption is performed with a randomly generated 256-bit key, and the IV is stored in the encrypted file itself.

2. Decrypting Files:
   - To decrypt the files, use the decryption script:

```
python decrypt.py
```

   - The decryption process will automatically detect the .key and .meta files associated with each encrypted file and use them for decryption. The integrity of each file is verified using the HMAC stored in the .meta file.

### Security Considerations

- Key Management: Currently, the key is stored alongside the encrypted file in a .key file, which is not secure for real-world usage. Consider integrating a secure key management system (KMS) like AWS KMS, Azure Key Vault, or HashiCorp Vault to store and retrieve keys securely.
  
- HMAC Verification: Each file's integrity is verified using an HMAC generated during encryption. If the HMAC check fails during decryption, the process will abort, and an error will be logged.

- Cleanup: Both .key and .meta files are removed after successful decryption to avoid leaving sensitive information behind.

### Future Enhancements

- Key Management Integration: Incorporate a secure key storage and retrieval mechanism, such as a cloud-based KMS or secure local storage.
  
- Multithreading: Improve performance by adding multithreading or parallel processing for handling large directories with many files.
  
- Command-Line Interface (CLI): Add a more user-friendly CLI that allows users to specify directories, file patterns, and other configurations as command-line arguments.
  
- Additional Algorithms: Expand the program to support other encryption algorithms (e.g., RSA, ChaCha20) or allow configurable encryption options.

### License

This project is open-source and distributed under the MIT License.

---

### Contact

For issues or contributions, please reach out via the repository's issues page.