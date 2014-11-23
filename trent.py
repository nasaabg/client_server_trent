import socket
import sys
import hashlib
import random
from pyDes import *

# VARIABLES
SERVER_ADDRESS = ('localhost', 3000)

# Tren knows users:
BOB_ID = "1"
BOB_KEY = "87654321"
ALICE_ID = "2"
ALICE_KEY = "12345678"

def get_request():
    request = connection.recv(512)
    if request:
        return request

def send_response(data):
    connection.send(data)
    
def get_values(message):
    params = message.split(',')
    return params

def key_generator():
    key = str(random.randint(10000000, 99999999))
    return key

def valid_users(params):
  # This function check if users are in the same network
  # I assume that we have only two users for this test
    if params[0] == ALICE_ID and params[1] == BOB_ID:
       return True
    else:
       return False

def encrypt(data, key):
    k = des(key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    encrypted_data = k.encrypt(data)
    return encrypted_data

def decrypt(data, key):
    k = des(key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    decrypted_data = k.decrypt(data)
    return decrypted_data
    


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
print >>sys.stderr, 'Trent starting up on %s port %s' % SERVER_ADDRESS
sock.bind(SERVER_ADDRESS)

# Listen for incoming connections
sock.listen(1)



# Wait for a connection
print >>sys.stderr, 'waiting for a connection'
connection, client_address = sock.accept()

try:
    print >>sys.stderr, 'connection from', client_address
    request = get_request()
    params_from_alice = get_values(request)

    alice_id = params_from_alice[0]
    bob_id = params_from_alice[1]
    alice_nonce = params_from_alice[2]
    bob_nonce = params_from_alice[3]

    if valid_users:
      print "OK I know this users. Generate key for them."
      key_a_b = key_generator()
      params_for_a = [key_a_b, bob_id, alice_nonce] 
      params_for_b = [key_a_b,alice_id,bob_nonce]
      
      message_for_a = ','.join(params_for_a)
      message_for_b = ','.join(params_for_b)

      encrypted_data_a = encrypt(message_for_a, ALICE_KEY)
      encrypted_data_b = encrypt(message_for_b, BOB_KEY)

      send_response(encrypted_data_a)
      request = get_request()
      send_response(encrypted_data_b)
      print "Session key sent."
    else:
      print "Something went wrong."
     



finally:
    # Clean up the connection
    print "Close connection."
    connection.close()