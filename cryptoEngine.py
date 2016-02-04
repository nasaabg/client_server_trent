# -*- coding: utf-8 -*-
import base64
from Crypto.Cipher import DES

class CryptoEngine:

    def __init__(self, key):
        self.key = key  

    def encrypt(self, data):
        k = DES.new(self.key, DES.MODE_CBC, '\0\0\0\0\0\0\0\0')
        data_normalized = base64.b64encode(data)
        encrypted_data = k.encrypt(data_normalized)
        return encrypted_data

    def decrypt(self, data):
        k = DES.new(self.key, DES.MODE_CBC, '\0\0\0\0\0\0\0\0')
        decrypted_data = k.decrypt(data)
        data_denormalized = base64.b64decode(decrypted_data)
        return data_denormalized