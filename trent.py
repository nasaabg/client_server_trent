# Jan Kurzydlo

import socket
import sys
import hashlib
import random
from pyDes import *
from cryptoEngine import CryptoEngine
from communicationModule import CommunicationModule

# VARIABLES
SERVER_ADDRESS = ('localhost', 3000)

# Tren knows users:
BOB_ID = "1"
BOB_KEY = "87654321"
ALICE_ID = "2"
ALICE_KEY = "12345678"
crypto_engine_bob = CryptoEngine(BOB_KEY)
crypto_engine_alice = CryptoEngine(ALICE_KEY)

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

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
print >>sys.stderr, 'Trent starting up on %s port %s' % SERVER_ADDRESS
sock.bind(SERVER_ADDRESS)

while True:
  # Listen for incoming connections
  sock.listen(1)



  # Wait for a connection
  print >>sys.stderr, 'waiting for a connection'
  connection, client_address = sock.accept()
  communication_engine = CommunicationModule(connection)

  try:
      print >>sys.stderr, 'connection from', client_address
      request = communication_engine.get_request()
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

        encrypted_data_a = crypto_engine_alice.encrypt(message_for_a)
        encrypted_data_b = crypto_engine_bob.encrypt(message_for_b)

        communication_engine.send_response(encrypted_data_a)
        request = communication_engine.get_request()
        communication_engine.send_response(encrypted_data_b)
        print "Session key sent."
      else:
        print "Something went wrong."
       



  finally:
      # Clean up the connection
      print "I did my job. Waiting for new connection."