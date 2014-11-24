class CommunicationModule:
    def __init__(self, connection):
        self.connection = connection

    # send response function
    def send_response(self, data):
        self.connection.send(data)

    def get_request(self):
        request = self.connection.recv(512)
        if request:
            return request    