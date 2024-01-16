class Authenticate:
    def __init__(self, server, database, client, request):
        self.server = server
        self.database = database
        self.request = request
        self.client = client

    def handle(self):
        #Handle user login, return session id
        pass
