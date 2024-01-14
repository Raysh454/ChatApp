import re

from . import Database

class Register:
    def __init__(self, server, client, request):
        self.server = server
        self.request = request
        self.client = client

    def validate(self):
        username = self.request.get('username')
        password = self.request.get('password')

        usernamePattern = re.compile(r'^[0-9A-Za-z]{6,16}$')
        passwordPattern = re.compile(r'^(?=.*?[0-9])(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[^0-9A-Za-z]).{8,32}$')

        if not bool(usernamePattern.match(username)):
            raise ValueError('Username can be between 6 and 16 characters and can only contain letters or numbers')
        elif not bool(passwordPattern.match(password)):
            raise ValueError('A strong password requires at least one uppercase letter, at least one lowercase letter, and at least one special character.')


    def handle(self):
       self.validate()
       
       #Check wether user exists or not
       #Return success or error json object to client


