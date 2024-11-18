from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Caesar Cipher
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# RSA
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key().decode()
    public_key = key.publickey().export_key().decode()
    return public_key, private_key

def rsa_encrypt(message, public_key_pem):
    try:
        rsa_key = RSA.import_key(public_key_pem)
        cipher = PKCS1_OAEP.new(rsa_key)
        max_message_length = (rsa_key.size_in_bits() // 8) - 42  # OAEP padding uses 42 bytes

        # Validasi panjang pesan
        if len(message.encode()) > max_message_length:
            return f"Pesan terlalu panjang untuk dienkripsi. Maksimum (256-42 = 214) karakter."

        encrypted_message = cipher.encrypt(message.encode())
        return base64.b64encode(encrypted_message).decode()
    except Exception as e:
        return f"Kesalahan dalam enkripsi: {e}"


def rsa_decrypt(encrypted_message, private_key_pem):
    try:
        rsa_key = RSA.import_key(private_key_pem)  # Import private key dari input
        cipher = PKCS1_OAEP.new(rsa_key)
        decrypted_message = cipher.decrypt(base64.b64decode(encrypted_message))
        return decrypted_message.decode()
    except Exception as e:
        raise ValueError(f"Kesalahan dalam dekripsi: {e}")

# Super Encryption
def super_encrypt(text, caesar_key, rsa_public_key):
    encrypted_caesar = caesar_encrypt(text, caesar_key)
    encrypted_rsa = rsa_encrypt(encrypted_caesar, rsa_public_key)
    return encrypted_rsa

def super_decrypt(encrypted_text, caesar_key, rsa_private_key):
    decrypted_rsa = rsa_decrypt(encrypted_text, rsa_private_key)
    decrypted_caesar = caesar_decrypt(decrypted_rsa, caesar_key)
    return decrypted_caesar
