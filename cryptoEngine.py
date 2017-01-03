# -*- coding: utf-8 -*-

class CryptoEngine:

    def __init__(self, key):
        self.key = "abcdefghijklmnopqrstuvwxyz:)-!*@#$%^&*()ABCDEFGHIJKLMNOPRSTUWXYZ"  

    def encrypt(self, plaintext):
        result = ''
        for l in plaintext:
            try:
                i = (self.key.index(l) + 5) % 64
                result += self.key[i]
            except ValueError:
                result += l

        return result

    def decrypt(self, ciphertext):
        result = ''
        for l in ciphertext:
            try:
                i = (self.key.index(l) - 5) % 64
                result += self.key[i]
            except ValueError:
                result += l

        return result