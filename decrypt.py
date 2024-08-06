from cryptography.fernet import Fernet

# Load the previously generated key from 'filekey.key'
with open('filekey.key', 'rb') as filekey:
    key = filekey.read()

# Initialize a Fernet object with the key
fernet = Fernet(key)

# Read the encrypted file
with open('delta1.png', 'rb') as enc_file:
    encrypted = enc_file.read()

# Decrypt the data
decrypted = fernet.decrypt(encrypted)

# Write the decrypted data to a new file
with open('delta1.png', 'wb') as dec_file:
    dec_file.write(decrypted)

print("File successfully decrypted and saved as 'delta1.png")
