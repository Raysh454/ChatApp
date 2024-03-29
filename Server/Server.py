import socket
import threading
import json
import traceback

from . import Database
from . import Register
from . import Authenticate
from . import Messages
from . import Logout

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = {}
        self.usernames = {}
        self.lock = threading.Lock()
       
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen()
        except Exception as e:
            print(f'Error Listening to port {port} : {e}')
            return
         
        print(f'Server listeneing on {host}:{port}')

    def start(self):
        while True:
            client_sock, addr = self.sock.accept()
            print(f'Handling: {addr}')
            client_handler = threading.Thread(target=self.handle_client, args=(client_sock,))
            client_handler.start()

    def handle_client(self, client_sock):
        database = Database.Database()
        request = {}
        try:
            while True:
                data = client_sock.recv(1024).decode('utf-8')
                if not data:
                    break

                try:
                    request = json.loads(data)
                except json.JSONDecodeError as json_error:
                    print(f'Error decoding JSON: {json_error}')
                    print(f'Received data: {data}')
                    continue

                match request.get('type', ''):
                    case 'AUTHENTICATE':
                        handler = Authenticate.Authenticate(self, database, client_sock, request)
                    case 'REGISTER':
                        handler = Register.Register(self, database, client_sock, request)
                    case 'MESSAGE':
                        handler = Messages.Messages(self, database, client_sock, request)
                    case 'LOGOUT':
                        handler = Logout.Logout(self, database, client_sock, request)
                    case _:
                        print(f'Unkown request type: {request.type}')
                        continue

                handler.handle()

        except Exception as e:
            traceback.print_exc()
            print(f'Error: {e}')
            if self.socketIsValid(client_sock):
                self.sendToClient({
                    'type': "ERROR",
                    'msg': "Something unexpected happened."
                    }, client_sock)
        finally:
            client_sock.close()
            session_id = request.get('session_id', '')
            if session_id:
                username = database.getUsername(session_id)
                database.deleteSession(session_id)
                self.deleteUser(username)
            database.connection.close()


    def broadcastMessage(self, json_obj, exclude=[]):
        for username, (_, socket) in self.users.items():
            if username not in exclude:
                self.sendToClient(json_obj, socket)
            

    def sendToClient(self, json_obj, client):
        if self.socketIsValid(client):
            json_string = json.dumps(json_obj)
            client.send(json_string.encode('utf-8'))

    def socketIsValid(self, sock):
        try:
            # Check if the socket is still connected
            sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
            return True
        except socket.error:
            return False

    def addUser(self, username, session_id, sock):
        with self.lock:
            self.users[username] = (session_id, sock)
            self.usernames[username] = 0
            self.broadcastMessage({ 'type': 'USER_LIST',
                                    'users': self.usernames
                               })
    
    def deleteUser(self, username):
        if username in self.users:
            with self.lock:
                del self.users[username]
                del self.usernames[username]
        self.broadcastMessage({ 'type': 'USER_LIST',
                                'users': self.usernames
                               })
