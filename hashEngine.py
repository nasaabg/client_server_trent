import hashlib
import random

class HashEngine:
     
    def generate_hash(self, value_one, value_two):
        value = hashlib.md5()
        value.update(value_one)
        value.update(value_two)
        return value.hexdigest()

    def hahs_function(self, message):
        value = hashlib.md5()
        value.update(message)
        return value.hexdigest()


    def compare_hashes(self, hash1, hash2):
        return hash1 == hash2  