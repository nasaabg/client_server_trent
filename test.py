from hashEngine import HashEngine
from cryptoEngine import CryptoEngine

x = CryptoEngine("12345678")

msg = x.encrypt("message")

print msg

z = x.decrypt(msg)

print z