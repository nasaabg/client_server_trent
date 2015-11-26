# Jan Kurzydlo

import socket
import sys
import hashlib
import random
from pyDes import *
from hashEngine import HashEngine
from cryptoEngine import CryptoEngine
from communicationModule import CommunicationModule
from authenticationEngine import AuthenticationEngine



# VARIABLES

ID = "1"

SERVER_ADDRESS = ('localhost', 4000)
NONCE = str(random.randint(100000, 999999))

hash_engine = HashEngine()
crypto_engine_bob = CryptoEngine("87654321")


# Preper table
# Usowam znaki konca lini, dziele dane na podgrupy (user_name, secured_password)
def prepere_users_tabel():
    table = file.readlines()

    for i,user in enumerate(table):
        table[i] = user.rstrip()      
        table[i] = table[i].split(',')
    return table

# Tabel of users
file = open('users_table.txt', 'r')
USERS = prepere_users_tabel()

    
def get_session_key(data):
    params = data.split(',')
    return params[0]

def make_some_tasks(data):
    return data[::-1]

# broken connection
def break_connection():
    print "Not authenticated."
    connection.send("401")    



# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
print >>sys.stderr, 'starting up on %s port %s' % SERVER_ADDRESS
sock.bind(SERVER_ADDRESS)

while True:
    # Listen for incoming connections
    sock.listen(1)



    # Wait for a connection
    print >> sys.stderr, 'Waiting for new connection from Alice :)'
    connection, client_address = sock.accept()

    communication_engine = CommunicationModule(connection)

    try:
        print >>sys.stderr, 'connection from', client_address
        data = ID + ", " + str(NONCE)
        communication_engine.send_response(data)

        print "Waiting for session key."
        # Getting SESSION KEY form message
        message = communication_engine.get_request()
        decrypted_message = crypto_engine_bob.decrypt(message)
        SESSION_KEY = get_session_key(decrypted_message)
        crypto_engine_session = CryptoEngine(SESSION_KEY)

        print "Session key established. Authentication."
        authentication_engine = AuthenticationEngine(USERS, hash_engine, connection, NONCE)
        if authentication_engine.authenticate_client():
            # Getting request from Alice, sending response
            request = communication_engine.get_request()
            decrypted_request = crypto_engine_session.decrypt(request)
            response = make_some_tasks(decrypted_request)
            encrypted_response = crypto_engine_session.encrypt(response)
            communication_engine.send_response(encrypted_response)
        else:
            break_connection()

        print "Sending response."


    finally:
        # Clean up the connection
        print "Did my job."
