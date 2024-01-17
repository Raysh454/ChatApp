import socket
import json
import threading

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = ''
        self.session_id = ''
        self.connected = False
        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)

    def connect(self):
        try:
            self.sock.connect((self.host, self.port))
            self.connected = True
            self.receive_thread.start()
            print(f"Connection established to {self.host}:{self.port}")
        except Exception as e:
            print(f"Error connecting to server:\n{e}")

    def disconnect(self):
        if self.connected:
            self.sock.close()
            self.connected = False
            print("Disconnected from the server")
    
    def sendMessage(self, message, reciever='BROADCAST'):
        if self.connected:
            message_obj = {
                'type' : 'MESSAGE',
                'session_id' : self.session_id,
                'reciever' : reciever,
                'message' : message
            }
            self.sock.send(json.dumps(message_obj).encode('utf-8'))
    
    def authenticate(self, username, password):
        if self.connected:
            authentication_obj = {
                'type' : 'AUTHENTICATE',
                'username' : username,
                'password' : password
            }
            self.sock.send(json.dumps(authentication_obj).encode('utf-8'))
    
    def register(self, username, password):
        if self.connected:
            registration_obj = {
                'type' : 'REGISTER',
                'username' : username,
                'password' : password
            }
            self.sock.send(json.dumps(registration_obj).encode('utf-8'))
    
    def logout(self):
        if self.connected and self.session_id:
            logout_obj = {
                'type' : 'LOGOUT',
                'session_id' : self.session_id
            }
            self.sock.send(json.dumps(logout_obj).encode('utf-8'))
    
    def receive_messages(self):
        while self.connected:
            try:
                data = self.sock.recv(1024).decode('utf-8')
                if not data:
                    break
                response = json.loads(data)
                self.handle_response(response)
            except Exception as e:
                print(f"Error while recieving messages.\n{e}")
                break
    
    def handle_response(self, response): # !!!clearly unfinished!!!
        print(response)
        print()
