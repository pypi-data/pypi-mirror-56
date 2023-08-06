from Crypto.Cipher import AES
from Crypto import Random

import base64
import hashlib
from typing import Union


def _pad(s: str, size: int) -> str:
    p = size - len(s) % size
    return s + p * chr(p)


def _unpad(s: str) -> str:
    return s[:-ord(s[-1])]


def encrypt(key: str, original_text: str, encode_base64: bool = True) -> Union[str, bytes]:
    raw = _pad(original_text, AES.block_size)
    iv = Random.new().read(AES.block_size)
    digested_key = hashlib.sha256(key.encode('utf-8')).digest()
    cipher = AES.new(digested_key, AES.MODE_CBC, iv)

    encrypted = iv + cipher.encrypt(raw)
    if encode_base64:
        encrypted = base64.b64encode(encrypted).decode('utf-8')

    return encrypted


def decrypt(key: str, encrypted_text: Union[str, bytes]) -> Union[None, str]:
    if isinstance(encrypted_text, bytes):
        enc = encrypted_text
    else:
        enc = base64.b64decode(encrypted_text)
    iv = enc[:AES.block_size]
    digested_key = hashlib.sha256(key.encode('utf-8')).digest()
    cipher = AES.new(digested_key, AES.MODE_CBC, iv)

    try:
        return _unpad(cipher.decrypt(enc[AES.block_size:]).decode('utf-8'))
    except:
        return None
