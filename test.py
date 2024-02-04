import unittest
import socket
import json

class TestServerHandlers(unittest.TestCase):
    def recieve(self, client_sock):
        try:
            data = client_sock.recv(1024).decode('utf-8')
            if not data:
                return

            try:
                request = json.loads(data)
                print(request)
                if 'session_id' in request:
                    return request['session_id']

            except json.JSONDecodeError as json_error:
                print(f'Error decoding JSON: {json_error}')
                print(f'Received data: {data}')

        except Exception as e:
            print(f'Error: {e}')

    def setUp(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(10.0)
        self.client_socket.connect(('127.0.0.1', 9999))

    def tearDown(self):
       pass 

    def test_register_handler(self):
        # Define your test data for the 'REGISTER' handler
        register_data = {
            'type': 'REGISTER',
            'username': 'TestUser',
            'password': 'Te$tPassw0rd'
        }

        # Send the data to the server
        self.client_socket.send(json.dumps(register_data).encode('utf-8'))

        self.recieve(self.client_socket)

    def test_authenticate_handler(self):
        # Define your test data for the 'AUTHENTICATE' handler
        authenticate_data = {
            'type': 'AUTHENTICATE',
            'username': 'TestUser',
            'password': 'Te$tPassw0rd'
        }

        # Send the data to the server
        self.client_socket.send(json.dumps(authenticate_data).encode('utf-8'))

        return self.recieve(self.client_socket)


    def test_messages_handler(self):
        # Define your test data for the 'MESSAGE' handler
        session_id = self.test_authenticate_handler()
        messages_data = {
            'type': 'MESSAGE',
            'session_id': session_id,
            'reciever': 'anotherUser',
            'message': 'Hello, this is a test message.'

        }

        # Send the data to the server
        self.client_socket.send(json.dumps(messages_data).encode('utf-8'))

        self.recieve(self.client_socket)


    def test_logout_handler(self):
        # Define your test data for the 'LOGOUT' handler
        session_id = self.test_authenticate_handler()

        logout_data = {
            'type': 'LOGOUT',
            'session_id':session_id
        }

        # Send the data to the server
        self.client_socket.send(json.dumps(logout_data).encode('utf-8'))

        self.recieve(self.client_socket)

if __name__ == '__main__':
    # Create a test suite and specify the order of test execution
    suite = unittest.TestSuite()
    suite.addTest(TestServerHandlers('test_register_handler'))
    suite.addTest(TestServerHandlers('test_authenticate_handler'))
    suite.addTest(TestServerHandlers('test_messages_handler'))
    suite.addTest(TestServerHandlers('test_logout_handler'))

    # Run the test suite
    unittest.TextTestRunner().run(suite)
