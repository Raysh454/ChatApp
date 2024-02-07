class Messages:
    def __init__(self, server, database, client, request):
        self.server = server
        self.database = database
        self.client = client
        self.request = request

    def handle(self):
        
        if not self.validate(): 
            return

        session_id = self.request['session_id']
        sender_username = self.database.getUsername(session_id)
        receiver = self.request['receiver']
        message = self.request['message']
       
        message_obj = {
                'type': 'MESSAGE',
                'sender': sender_username,
                'message': message
            }

        #Send message to receiver or broadcast
        if receiver == 'BROADCAST':
            self.server.broadcastMessage(message_obj, [sender_username])

        elif receiver in self.server.users:
            receiver_sock = self.server.users[receiver][1]
            self.server.sendToClient(message_obj, receiver_sock)
        else:
            self.server.sendToClient({
                'type': 'ERROR',
                'msg': f'no user: {receiver}',
            }, self.client)


    def validate(self):
        #Check if required fields are present in request
        required_fields = {'receiver', 'message', 'session_id'}

        missing_fields = required_fields - set(self.request)
        if missing_fields:
            error_message = f'Missing required fields: {", ".join(missing_fields)}'
            self.server.sendToClient({'type': 'ERROR', 'msg': error_message}, self.client)
            return False
       
        if not self.request['message']:
            self.server.sendToClient({'type': 'ERROR', 'msg': "message body can't be empty"}, self.client)

        #Check if session_id is valid
        session_id = self.request['session_id']
        if session_id is None or not self.database.sessionIsValid(session_id):
            self.server.sendToClient({
                'type': 'ERROR',
                'msg': 'Invalid session ID',
            }, self.client)
            return False
        return True
