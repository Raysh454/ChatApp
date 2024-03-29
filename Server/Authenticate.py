class Authenticate:
    def __init__(self, server, database, client, request):
        self.server = server
        self.database = database
        self.request = request
        self.client = client

    def validate(self):
        if 'username' not in self.request or 'password' not in self.request:
            self.server.sendToClient({
                'type': 'ERROR',
                'msg': 'Missing username or password in the request',
                }, self.client)
            return False

        return True
        

    def handle(self):
        if not self.validate():
            return

        username = self.request['username']
        password = self.request['password']
        
        if not self.database.isAnUser(username) or not self.database.loginIsValid(username, password):
            self.server.sendToClient({
                'type':'ERROR',
                'msg' :'Invalid username or password',
            }, self.client)
            return
        
        # if it got to here it means Authentication was successful. Time to generate Sesh Id
        session_id = self.database.assignSession(username)

        self.server.sendToClient({
            'type': 'SUCCESS',
            'msg': 'Authentication successful',
            'session_id': session_id,
        }, self.client)
        
        self.server.addUser(username, session_id, self.client)
