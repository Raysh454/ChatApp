import socket
import json
import threading
from PyQt6.QtCore import QObject, pyqtSignal

class Client(QObject):
    response_received = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.host = ''
        self.port = 0
        self.username = ''
        self.session_id = ''
        self.connected = False
        self.receive_thread = threading.Thread(target=self.receiveMessages, daemon=True)
        

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.connected = True
            print(f"Connection established to {self.host}:{self.port}")
            return True
            
        except Exception as e:
            print(f"Error connecting to server:\n{e}")
            return False

    def disconnectSock(self):
        if self.connected:
            self.sock.close()
            self.connected = False
            print("Disconnected from the server")
    
    def sendMessage(self, message, receiver='BROADCAST'):
        if self.connected:
            message_obj = {
                'type' : 'MESSAGE',
                'session_id' : self.session_id,
                'receiver' : receiver,
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
            response = self.receiveMessages(True, 105)
            
            if response and response.get('session_id', ''):
                self.session_id = response['session_id']
                self.username = username
                self.password = password
                return (True, response.get('msg', ''))
            if response:
                return (False, response.get('msg', ''))
        return(False, 'Server unreachable')
    
    def register(self, username, password):
        if self.connected:
            registration_obj = {
                'type' : 'REGISTER',
                'username' : username,
                'password' : password
            }
            self.sock.send(json.dumps(registration_obj).encode('utf-8'))
            response = self.receiveMessages(True)
            if response and response.get('type', '') == 'SUCCESS':
                return (True, response.get('msg', ''))
            if response:
                return (False, response.get('msg', ''))
        return (False, 'Server unreachabe')
    
    def logout(self):
        if self.connected and self.session_id:
            logout_obj = {
                'type' : 'LOGOUT',
                'session_id' : self.session_id
            }
            self.sock.send(json.dumps(logout_obj).encode('utf-8'))

    
    def receiveMessages(self, runOnce=False, size=1024):
        while self.connected or runOnce:
            try:
                data = self.sock.recv(size).decode('utf-8')
                if not data:
                    break
                print(f"Recieved message {data}")

                try:
                    response = json.loads(data)
                except json.JSONDecodeError as json_error:
                    print(f'Error decoding JSON: {json_error}')
                    print(f'Received data: {data}')
                    continue
                
                if runOnce:
                    return response

                self.response_received.emit(response)
            except Exception as e:
                print(f"Error while recieving messages.\n{e}")
                self.disconnect()
                break
