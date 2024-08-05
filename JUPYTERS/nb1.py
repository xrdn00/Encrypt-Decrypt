## THIS WAS DONE
# pip install cryptography
# pip install jupyter-notebook

##
# removed en and de crypt.py, and merged it into one jupyter-notebook (to avoid a certain (actual) 'hell'  (dependency hell)
# this is what I talk about! https://www.explainxkcd.com/wiki/index.php/1579:_Tech_Loops)

## RESOURCES AND SOURCES
#- https://docs.python.org/3/
#- https://pypi.org/project/cryptography/
#- https://cryptography.io/en/latest/
#- https://docs.python.org/3/library/base64.html
#- https://docs.python.org/3/library/hashlib.html
#EXTERNAL resources
# https://travisdazell.blogspot.com/2012/11/many-time-pad-attack-crib-drag.html
#- https://github.com/loneicewolf/ciphers-python/blob/main/Sectors/1/Funcs.py     (( for the "XOR and STUFF" modified. ))
from cryptography.fernet import Fernet
import hashlib
import base64

def generate_key() -> str:
    """Generate a new Fernet key."""
    key = Fernet.generate_key()
    return key.decode()

def encrypt(message: str, key: str) -> str:
    """Encrypt a message using the provided Fernet key."""
    fernet = Fernet(key.encode())
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message.decode()

def decrypt(encrypted_message: str, key: str) -> str:
    """Decrypt a message using the provided Fernet key."""
    fernet = Fernet(key.encode())
    decrypted_message = fernet.decrypt(encrypted_message.encode())
    return decrypted_message.decode()

def hash_string(input_string: str) -> str:
    """Hash a string using SHA-256."""
    sha256_hash = hashlib.sha256(input_string.encode()).hexdigest()
    ##todo make more algorithms
    ##todo iterations
    ##todo HMAC
    ##opt.TODO: GCM GALOIS
    return sha256_hash
def convert_encoding(data: bytes, encoding: str) -> str:
    """Convert data to the specified encoding."""
    if encoding == 'base64':
        return base64.b64encode(data).decode()
    elif encoding == 'base32':
        return base64.b32encode(data).decode()
    elif encoding == 'hex':
        return data.hex()
    else:
        raise ValueError("Unsupported encoding format")

def convert_from_encoding(encoded_data: str, encoding: str) -> bytes:
    """Convert data from the specified encoding."""
    if encoding == 'base64':
        return base64.b64decode(encoded_data)
    elif encoding == 'base32':
        return base64.b32decode(encoded_data)
    elif encoding == 'hex':
        return bytes.fromhex(encoded_data)
    else:
        raise ValueError("Unsupported encoding format")


def HEX_ENC(data: str) -> str:
    """Convert a string to its hex representation."""
    return data.encode().hex()

def HEX_XOR(s1: str, s2: str) -> str:
    """Perform XOR on two hex-encoded strings."""
    b1 = bytes.fromhex(s1)
    b2 = bytes.fromhex(s2)
    
    if len(b1) != len(b2):
        raise ValueError("Hex strings must be of the same length")

    xor_result = bytes(a ^ b for a, b in zip(b1, b2))
    
    return xor_result.hex()


def xor_strings(s1: str, s2: str) -> str:
    ##todo CRIB DRAG
    # https://travisdazell.blogspot.com/2012/11/many-time-pad-attack-crib-drag.html
    """Perform XOR on two strings."""
    if len(s1) != len(s2):
        raise ValueError("Strings must be of the same length")
    
    b1 = s1.encode()
    b2 = s2.encode()
    xor_result = bytes(a ^ b for a, b in zip(b1, b2))
    return xor_result.decode()

def driver(choice):
    # make a rule list of this instead of if if if(..)
    if choice == 'gen_key':
        key = generate_key()
        print(f"Generated Key: {key}")
    
    ## todo: add decryption based on this, for now this is fine
    if choice == 'enc':
        original_message=input("plaintext")
        key=generate_key()
        ##todo input key
        print(f"Generated Key: {key}")
        encrypted_message = encrypt(original_message, key)
        decrypted_message = decrypt(encrypted_message, key)
        print(f"Original Message: {original_message}")
        print(f"Encrypted Message: {encrypted_message}")
        print(f"Decrypted Message: {decrypted_message}")
    
    if choice == 'hash':
        original_message_to_hash=input("plaintext")
        hash_value = hash_string(original_message_to_hash)
        print(f"SHA-256 Hash: {hash_value}")
    
    ##todo name it better (code as in en and de  code)
    ## todo make this complete
    #if choice == 'code':
    #    encoded_message = convert_encoding(encrypted_message.encode(), 'base64')
    #    decoded_message = convert_from_encoding(encoded_message, 'base64').decode()
    #    print(f"Base64 Encoded: {encoded_message}")
    #    print(f"Base64 Decoded: {decoded_message}")\
    ### UnboundLocalError: cannot access local variable 'encrypted_message' where it is not associated with a value
    if choice == 'xor':
        ##todo input
        msg1 = "Hello"
        msg2 = "World"
        hex_msg1 = HEX_ENC(msg1)
        hex_msg2 = HEX_ENC(msg2)

        xor_result = HEX_XOR(hex_msg1, hex_msg2)
        print(f"XOR Result in Hex: {xor_result}")
#done

##  driver(choice="")#
#driver(choice="xor")#                pass
#driver(choice="hash")#             pass
#driver(choice="code")#             ERROR, TODO
#driver(choice="enc")#               pass
#driver(choice="gen_key")#       pass
