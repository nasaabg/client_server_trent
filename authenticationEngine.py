from communicationModule import CommunicationModule


class AuthenticationEngine:
    def __init__(self, users, hash_engine, connection, nonce):
        self.connection = CommunicationModule(connection)
        self.users = users
        self.hash_engine = hash_engine
        self.nonce = nonce

    # function to find user as ['user_name', 'secured_password']
    def find(self, user_name, table):
        for user in table:
            if user[0] == user_name:
                return user
        return -1

    # Check if hashes are the same
    def compare_hashes(self,received_hash, user_name):
        user = self.find(user_name, self.users)
        if user == -1:
            return False
        secured_password = user[1]
        hash_to_compare = self.hash_engine.generate_hash(self.nonce, secured_password)

        return hash_to_compare == received_hash

    # authentication
    def authenticate_client(self):
        # ask about user name
        self.connection.send_response("User name: ")
        user_name = self.connection.get_request()

        # send randomly generated nonce to user
        self.connection.send_response(self.nonce)
        
        # get hash from client
        client_hash = self.connection.get_request()

        # compare hashes
        if self.compare_hashes(client_hash, user_name):
            user = self.find(user_name, self.users)
            if user == -1:
                return False
            user_secured_password = user[1]
            hash_for_client = self.hash_engine.generate_hash(user_secured_password, self.nonce)
            self.connection.send_response(hash_for_client)
            return True
        else:
            return False


        