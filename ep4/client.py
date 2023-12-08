import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os
from base64 import b64encode, b64decode

email = input("Email: ")
password = input("Password: ")

aes = os.urandom(32)
mac = os.urandom(32)
iv = os.urandom(16)
session_keys = b64encode(aes + mac + iv)

def encrypt(text):
    aes_context = Cipher(algorithms.AES(aes), modes.CTR(iv), backend=default_backend())
    encryptor = aes_context.encryptor()
    cyphertext = encryptor.update(text) + encryptor.finalize()
    return cyphertext

cyphertext = encrypt((email + ":" + password).encode())

def gen_hmac(mac, data):
    hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
    hash.update(mac+data)
    hmac = hash.finalize()
    return hmac

hmac = gen_hmac(mac, cyphertext)

r = requests.post('http://localhost:5000/login/', data={'session_keys': session_keys.decode(),'cyphertext': b64encode(cyphertext).decode(), 'hmac': b64encode(hmac).decode()})
print(r.status_code)
if r.status_code == 200:
    print("Cookies: + ", r.cookies.get('session_id'))



