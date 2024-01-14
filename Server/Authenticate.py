from . import Database

class Authenticate:
    def __init__(self, server, client, request):
        self.server = server
        self.request = request
        self.client = client

    def handle(self):
        #Handle user login, return session id
