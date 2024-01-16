import re

class Register:
    def __init__(self, server, database, client, request):
        self.server = server
        self.database = database
        self.request = request
        self.client = client

    def validate(self):
        username = self.request.get('username', '')
        password = self.request.get('password', '')

        usernamePattern = re.compile(r'^[0-9A-Za-z]{6,16}$')
        passwordPattern = re.compile(r'^(?=.*?[0-9])(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[^0-9A-Za-z]).{8,32}$')

        if not bool(usernamePattern.match(username)):
            self.server.sendToClient({
                'type': 'ERROR',
                'msg': 'Username can be between 6 and 16 characters and can only contain letters or numbers',
                }, self.client)
            return False
        elif not bool(passwordPattern.match(password)):
            self.server.sendToClient({
                'type': 'ERROR',
                'msg': 'A strong password requires at least one uppercase letter, at least one lowercase letter, and at least one special character.',
                }, self.client)
            return False

        return True


    def handle(self):
        if not self.validate():
            return
        if self.database.isAnUser(self.request['username']):
            self.server.sendToClient({
                'type': 'ERROR',
                'msg': 'Username exists'
                }, self.client)
            return
        
        self.database.createUser(self.request['username'], self.request['password'])
        self.server.sendToClient({
            'type': 'SUCCESS',
            'msg': 'User created'
            }, self.client)
