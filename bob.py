import socket
import sys
import hashlib
import random
from pyDes import *


# VARIABLES
SERVER_ADDRESS = ('localhost', 4000)
ID = "1"
NONCE = str(random.randint(100000, 999999))
SESSION_KEY = ""
KEY = "87654321"


# Preper table
def prepere_users_tabel():
    # Usowam znaki konca lini, dziele dane na podgrupy (user_name, secured_password)
    table = file.readlines()

    for i,user in enumerate(table):
        table[i] = user.rstrip()      
        table[i] = table[i].split(',')
    return table

# Tabel of users
file = open('users_table.txt', 'r')
USERS = prepere_users_tabel()


# send response function
def send_response(data):
    connection.send(data)

def get_request():
    request = connection.recv(512)
    if request:
        return request
    
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

def make_some_tasks(data):
    return data[::-1]

# hash function
def hash_function(value_one, value_two):
    value = hashlib.md5()
    value.update(value_one)
    value.update(value_two)
    return value.hexdigest()


# authentication
def authenticate_client():
    # ask about user name
    send_response("User name: ")
    user_name = get_request()

    # send randomly generated nonce to user
    send_response(NONCE)
    
    # get hash from client
    client_hash = get_request()

    # compare hashes
    if compare_hashes(client_hash, user_name):
        user = find(user_name, USERS)
        if user == -1:
            return False
        user_secured_password = user[1]
        hash_for_client = hash_function(user_secured_password, NONCE)
        send_response(hash_for_client)
        return True
    else:
        return False

# Check if hashes are the same
def compare_hashes(received_hash, user_name):
    user = find(user_name, USERS)
    if user == -1:
            return False
    secured_password = user[1]
    hash_to_compare = hash_function(NONCE, secured_password)

    return hash_to_compare == received_hash



# broken connection
def break_connection():
    print "Not authenticated."
    connection.send("401")

# function to find user as ['user_name', 'secured_password']
def find(user_name, table):
    for user in table:
        if user[0] == user_name:
            return user
    return -1



# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
print >>sys.stderr, 'starting up on %s port %s' % SERVER_ADDRESS
sock.bind(SERVER_ADDRESS)

# Listen for incoming connections
sock.listen(1)



# Wait for a connection
print >> sys.stderr, 'waiting for a connection'
connection, client_address = sock.accept()

try:
    print >>sys.stderr, 'connection from', client_address
    data = ID + ", " + str(NONCE)
    send_response(data)

    print "Waiting for session key."
    # Getting SESSION KEY form message
    message = get_request()
    decrypted_message = decrypt(message, KEY)
    SESSION_KEY = get_session_key(decrypted_message)

    print "Session key established. Authentication."

    if authenticate_client():
        # Getting request from Alice, sending response
        request = get_request()
        decrypted_request = decrypt(request, SESSION_KEY)
        response = make_some_tasks(decrypted_request)
        encrypted_response = encrypt(response, SESSION_KEY)
        send_response(encrypted_response)
    else:
        break_connection()

    print "Sending response."


finally:
    # Clean up the connection
    print "Close connection."
    connection.close()