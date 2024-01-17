class Logout:
    def __init__(self, server, database, client, request):
        self.server = server
        self.database = database
        self.request = request
        self.client = client

    def handle(self):
        session_id = self.request.get('session_id', '')
        username = self.database.getUsername(session_id)
        if session_id and self.database.sessionIsValid(session_id):
            self.server.deleteUser(username)
            self.database.deleteSession(session_id)
