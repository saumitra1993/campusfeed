from Crypto.Cipher import AES
import base64
import hashlib

BLOCK_SIZE = 32

PADDING = '{'

pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

def get_password_hash(password):
    secret = hashlib.sha256(password).digest()
    cipher = AES.new(secret)
    encrypted_password = EncodeAES(cipher, password)
    return encrypted_password

def passwords_match(stored, entered):
    encrypted_password = get_password_hash(entered)
    return stored == encrypted_password