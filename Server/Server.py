import socket
import threading
import json

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.sock.bind((self.host, self.port))
        self.sock.listen()
         
        print(f'Server listeneing on {host}:{port}')

    def start(self):
        while True:
            client_sock, addr = self.sock.accept()
            self.clients[addr] = client_sock
            client_handler = threading.Thread(target=self.handle_client, args=(client_sock,))
            client_handler.start()

    def handle_client(self, client_sock):
        while True:
            try:
                data = client_sock.recv(1024).decode('utf-8')
                if not data:
                    break

                request = json.loads(data)

                match request.get('type', ''):
                    case 'AUTHENTICATION':
                        Authenticate(self, request)
                    case 'REGISTER':
                        Register(self, request)
                    case 'MESSAGE':
                        Message(self, request)
                    case _:
                        print(f'Unkown request type: {request.type}')
                        continue
            except Exception as e:
                print(f'Error: {e}')    
            finally:
                addr = client_sock.getpeername()
                print(f'Connection from {addr} closed')
                del self.clients[addr]
