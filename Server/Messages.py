class Messages:
    def __init__(self, server, database, client, request):
        self.server = server
        self.database = database
        self.client = client
        self.request = request

    def handle(self, database, client_sock, request):
        
        if not self.validate(): return

        target = self.request['TARGET']
        message = self.request['MESSAGE']
        
        #Send message to target or broadcast
        if target == 'BROADCAST':
            self.server.broadcastMessage(message)

        elif target in self.server.clients:
            client_sock = self.server.clients[target]
            self.server.sendToClient(message, client_sock)
        else:
            self.server.sendToClient(self.server, {
                'type': 'ERROR',
                'msg': f'Invalid target: {target}',
            }, self.client)


    def validate(self):
        #Check if required fields are present in request
        required_fields = {'TARGET', 'MESSAGE', 'session_id'}

        missing_fields = required_fields - set(self.request) # Faster than iterating it using a loop apparently xD

        if missing_fields:
            error_message = f'Missing required fields: {", ".join(missing_fields)}'
            self.server.sendToClient({'type': 'ERROR', 'msg': error_message}, self.client)
            return False
        
        #Check if session_id is valid
        session_id = self.request['session_id']
        if session_id is None or not self.database.sessionIsValid(session_id):
            self.server.sendToClient({
                'type': 'ERROR',
                'msg': 'Invalid session ID',
            }, self.client)
            return False
        return True
