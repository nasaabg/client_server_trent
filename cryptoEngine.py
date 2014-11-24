from pyDes import *

class CryptoEngine:

    def __init__(self, key):
        self.key = key    

    def encrypt(self, data):
        k = des(self.key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
        encrypted_data = k.encrypt(data)
        return encrypted_data

    def decrypt(self, data):
        k = des(self.key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
        decrypted_data = k.decrypt(data)
        return decrypted_data