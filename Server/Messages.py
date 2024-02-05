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
        reciever = self.request['reciever']
        message = self.request['message']
       
        message_obj = {
                'type': 'MESSAGE',
                'sender': sender_username,
                'message': message
            }

        #Send message to reciever or broadcast
        if reciever == 'BROADCAST':
            self.server.broadcastMessage(message_obj)

        elif reciever in self.server.users:
            reciever_sock = self.server.users[reciever][1]
            self.server.sendToClient(message_obj, reciever_sock)
        else:
            self.server.sendToClient({
                'type': 'ERROR',
                'msg': f'no user: {reciever}',
            }, self.client)


    def validate(self):
        #Check if required fields are present in request
        required_fields = {'reciever', 'message', 'session_id'}

        missing_fields = required_fields - set(self.request)
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
