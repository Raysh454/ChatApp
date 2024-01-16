import socket
import threading
import json

from . import Database
from . import Register
from . import Authenticate
from . import Messages

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.users = {}
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
            self.clients[addr[0]] = client_sock
            client_handler = threading.Thread(target=self.handle_client, args=(client_sock,))
            client_handler.start()

    def handle_client(self, client_sock):
            try:
                database = Database.Database()
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
                        case 'AUTHENTICATION':
                            handler = Authenticate.Authenticate(self, database, client_sock, request)
                        case 'REGISTER':
                            handler = Register.Register(self, database, client_sock, request)
                        case 'MESSAGE':
                            handler = Messages.Messages(self, database, client_sock, request)
                        case _:
                            print(f'Unkown request type: {request.type}')
                            continue

                    handler.handle()

            except Exception as e:
                print(f'Error: {e}')
                if self.socketIsValid(client_sock):
                    self.sendToClient({
                        'type': "ERROR",
                        'msg': "Something unexpected happened."
                        }, client_sock)
            finally:
                addr = client_sock.getpeername()
                print(f'Connection from {addr} closed')
                client_sock.close()
                del self.clients[addr[0]]


    def broadcastMessage(self, json_obj):
        for _, socket in self.users:
            self.sendToClient(json_obj, socket)
            

    def sendToClient(self, json_obj, client):
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
    
    def deleteUser(self, username):
        if username in self.users:
            with self.lock:
                del self.users[username]
