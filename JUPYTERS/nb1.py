#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
## THIS WAS DONE
# pip install cryptography

## removed en and de crypt.py, and merged it into one jupyter-notebook (to avoid a certain (actual) 'hell'  (dependency hell)
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
# CHATGPT FOR GUI (minor improvements was made after)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
from cryptography.fernet import Fernet
import hashlib
import base64
import ipywidgets as widgets
from IPython.display import display

# Functions remain unchanged
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
    """Perform XOR on two strings."""
    if len(s1) != len(s2):
        raise ValueError("Strings must be of the same length")
    
    b1 = s1.encode()
    b2 = s2.encode()
    xor_result = bytes(a ^ b for a, b in zip(b1, b2))
    return xor_result.decode()

def perform_action(choice, original_message=None, key=None, message_to_hash=None):
    """Perform actions based on the choice."""
    output = ""
    if choice == 'gen_key':
        key = generate_key()
        output = f"Generated Key: {key}"
    
    if choice == 'enc':
        if not original_message or not key:
            raise ValueError("Original message and key are required.")
        encrypted_message = encrypt(original_message, key)
        decrypted_message = decrypt(encrypted_message, key)
        output = (
            f"Original Message: {original_message}\n"
            f"Generated Key: {key}\n"
            f"Encrypted Message: {encrypted_message}\n"
            f"Decrypted Message: {decrypted_message}"
        )
    
    if choice == 'hash':
        if not message_to_hash:
            raise ValueError("Message to hash is required.")
        hash_value = hash_string(message_to_hash)
        output = f"SHA-256 Hash: {hash_value}"
    
    if choice == 'xor':
        if not original_message:
            raise ValueError("Two messages are required for XOR.")
        msg1, msg2 = original_message
        hex_msg1 = HEX_ENC(msg1)
        hex_msg2 = HEX_ENC(msg2)
        xor_result = HEX_XOR(hex_msg1, hex_msg2)
        output = f"XOR Result in Hex: {xor_result}"
    
    return output

# GUI Elements

# Dropdown for selecting action
action_dropdown = widgets.Dropdown(
    options=['Select', 'gen_key', 'enc', 'hash', 'xor'],
    value='Select',
    description='Action:',
)

# Input fields
original_message_input = widgets.Text(
    value='',
    placeholder='Enter your message',
    description='Message:',
)

key_input = widgets.Text(
    value='',
    placeholder='Enter the key',
    description='Key:',
)

message_to_hash_input = widgets.Text(
    value='',
    placeholder='Enter message to hash',
    description='Message to Hash:',
)

# Output area
output_area = widgets.Output()

def on_button_click(b):
    with output_area:
        # Clear previous output
        output_area.clear_output()
        
        # Get selected action
        action = action_dropdown.value
        original_message = original_message_input.value
        key = key_input.value
        message_to_hash = message_to_hash_input.value
        
        if action == 'xor':
            # For XOR, we need two messages, so we split the input
            original_messages = original_message.split(',')
            if len(original_messages) != 2:
                print("For XOR, provide two comma-separated messages.")
                return
            output = perform_action(action, original_message=original_messages)
        else:
            output = perform_action(action, original_message=original_message, key=key, message_to_hash=message_to_hash)
        
        print(output)

# Button to trigger action
button = widgets.Button(description="Run")
button.on_click(on_button_click)

# Display GUI
display(action_dropdown, original_message_input, key_input, message_to_hash_input, button, output_area)
