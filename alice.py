import socket
import sys
import hashlib
import random
from pyDes import *

bob_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
trent_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bob_address = ('localhost', 4000)
trent_address = ('localhost', 3000)
ID = "2"
NONCE = str(random.randint(100000, 999999))
KEY = "12345678"
SESSION_KEY = ""
msg = "To jest wiadomosc klienta do servera"


def get_response(sock):
    response = sock.recv(512)
    if response:
        return response

def get_id(response):
    params = response.split(',')
    return params[0]

def get_nonce(response):
    params = response.split(',')
    return params[1].strip()

def send_request(sock, data):
    sock.sendall(data)

def encrypt(data, key):
    k = des(key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    encrypted_data = k.encrypt(data)
    return encrypted_data

def decrypt(data, key):
    k = des(key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    decrypted_data = k.decrypt(data)
    return decrypted_data

def get_session_key(data):
    params = data.split(',')
    return params[0]

def check_response(response):
    if response[::-1] == msg:
        print "Response correct."
    else:
        print "Response wrong."
    
def generate_hash(value_one, value_two):
    value = hashlib.md5()
    value.update(value_one)
    value.update(value_two)
    return value.hexdigest()

def hahs_function(message):
    value = hashlib.md5()
    value.update(message)
    return value.hexdigest()


def compare_hashes(received_hash, nonce, secured_password):
    return received_hash == generate_hash(secured_password, nonce)   


print 'Connecting to Bob on: %s port %s' % bob_address
bob_sock.connect(bob_address)

print 'Connecting to Trent on: %s port %s' % trent_address
trent_sock.connect(trent_address)

try:
  # Getting information from Bob
  response = get_response(bob_sock)
  bob_id = get_id(response)
  bob_nonce = get_nonce(response)

  # Params sended to TRENT (id_alice, id_bob, nonce_a, nonce_b)
  params_for_trent = [ID, bob_id, NONCE, bob_nonce]
  params_message = ','.join(params_for_trent)

  print 'Sending connection information to Trent'
  send_request(trent_sock, params_message)

  print 'Getting Session key generated by Trent.'
  message_for_me = get_response(trent_sock)

  print 'Message for me received. Sending confirmation.'
  send_request(trent_sock, "Recived")

  message_for_bob = get_response(trent_sock)
  print 'Message for Bob received. Sending confirmation.'

  # Getting SESSION KEY from trent message
  decrypted_data = decrypt(message_for_me, KEY)
  SESSION_KEY = get_session_key(decrypted_data)

  print "Sending session key to Bob."
  send_request(bob_sock, message_for_bob)


  # display message from server
  if get_response(bob_sock):
    print "Authentication proces.."

  # send user name
  user_name = raw_input('Type your login: ')
  send_request(bob_sock, user_name)

  # get nonce from server
  nonce = get_response(bob_sock)

  # get user password
  password = raw_input('Type your password: ')

  # generate hash 
  secured_password = hahs_function(password)
  user_hash = generate_hash(nonce, secured_password)

  # send user_hash to server
  send_request(bob_sock, user_hash) 

  # get response with hash to compare
  hash_from_server = get_response(bob_sock)

  # compare hash to authenticate server
  if compare_hashes(hash_from_server, nonce, secured_password):
      print "Authentication succeeded! Server authenticated!"
      print 'Sending Request: ' + msg
      encrypted_msg = encrypt(msg, SESSION_KEY)
      send_request(bob_sock, encrypted_msg)
      response = get_response(bob_sock)
      decrypted_response = decrypt(response, SESSION_KEY)
      print "Response: " + decrypted_response
      print "Checking if correct response.."
      check_response(decrypted_response)
  else:
      print "Authentication failed"

finally:
    print 'closing socket'
    bob_sock.close()
    # trent_sock.close()