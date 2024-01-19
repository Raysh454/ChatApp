import sys
from ..Client import Client
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton

class chatApp(QWidget):
    def __init__(self, host, port, parent=None):
        super().__init__(parent)

        self.client = Client(host, port)
        self.client.connect()

        self.makeUI()

    def makeUI(self):
        layout = QVBoxLayout()

        self.messageDisplay = QTextEdit(self)
        self.messageDisplay.setReadOnly(True)
        layout.addWidget(self.messageDisplay)

        self.inputBox = QLineEdit(self)
        layout.addWidget(self.inputBox)

        sendButton = QPushButton('Send', self)
        sendButton.clicked.connect(self.sendMessage)
        layout.addWidget(sendButton)

        self.client.response_received.connect(self.handleResponse)

    def sendMessage(self):
        message = self.inputBox.text()
        self.inputBox.clear()
        self.client.sendMessage(message) # not finished!!!!! check sendMessage() in Client.py for more info
    
    def handle_response(self, response):
        if response['type'] == 'MESSAGE':
            sender = response['sender']
            message = response['message']
            self.messageDisplay.append(str(sender) + ": " + str(message))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = chatApp()
    window.show()
    sys.exit(app.exec())