import os
import base64
from dotenv import load_dotenv

from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

load_dotenv()

key_str = os.getenv("CRYPTO_KEY")
if key_str is None:
    raise ValueError("CRYPTO KEY is not set in .env")
aes_key = base64.b64decode(key_str)

def encrypt(message):
    cipher = AES.new(aes_key, AES.MODE_CBC)
    ciphered_data = cipher.encrypt(pad(message, AES.block_size))
    return cipher.iv + ciphered_data

def decrypt(ciphertext):
    iv = ciphertext[:16]
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
    message = unpad(cipher.decrypt(ciphertext[16:]), AES.block_size)
    return message