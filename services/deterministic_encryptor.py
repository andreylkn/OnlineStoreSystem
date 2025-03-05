import base64
from Crypto.Cipher import AES

# A fixed encryption key (for demonstration only; store/manage keys securely in production)
ENCRYPTION_KEY = b"16byteSecretKey!"  # Exactly 16 bytes

class DeterministicEncryptor:
    def __init__(self, key):
        # key must be 16, 24, or 32 bytes. Here we use a fixed 16-byte key.
        self.key = key
        self.cipher = AES.new(self.key, AES.MODE_ECB)

    def __pad(self, s):
        pad_len = 16 - (len(s) % 16)
        return s + chr(pad_len) * pad_len

    def __unpad(self, s):
        pad_len = ord(s[-1])
        return s[:-pad_len]

    def encrypt(self, plaintext):
        plaintext_padded = self.__pad(plaintext)
        ciphertext = self.cipher.encrypt(plaintext_padded.encode())
        return base64.b64encode(ciphertext).decode()

    def decrypt(self, token):
        ciphertext = base64.b64decode(token)
        plaintext_padded = self.cipher.decrypt(ciphertext).decode()
        return self.__unpad(plaintext_padded)
