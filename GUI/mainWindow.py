import sys
from ..Client import Client
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QMainWindow, QHBoxLayout
from PyQt6.QtCore import QSize, QTimer, Qt
from PyQt6.QtGui import QIcon, QShortcut
import ctypes

# This code makes it so windows doesn't use Pythonw.exe's icon in taskbar
myappid = u'mycompany.myproduct.subproduct.version' # stupid windows
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class chatApp(QMainWindow):
    def __init__(self): # add host and port to init when done testing gui
        super().__init__()
        
        self.setWindowTitle("Chat Application")
        self.setMinimumSize(QSize(720,480))
        self.setWindowIcon(QIcon('ChatApp/Icons/chat.png'))

        #self.client = Client(host, port)
        #self.client.connect()

        self.makeUI()

    def makeUI(self):
        layout = QVBoxLayout()
        layoutH = QHBoxLayout()
        self.messageDisplay = QTextEdit(self)
        self.messageDisplay.setReadOnly(True)
        layout.addWidget(self.messageDisplay)

        self.inputBox = QLineEdit(self)
        layoutH.addWidget(self.inputBox)

        sendButton = QPushButton('Send', self)
        sendButton.clicked.connect(self.sendMessage)
        layoutH.addWidget(sendButton)
        

        #self.client.response_received.connect(self.handleResponse)

        layoutH.setSpacing(10)
        layoutH.setContentsMargins(0, 10, 0, 0)
        layoutHWidget = QWidget()
        layoutHWidget.setLayout(layoutH)

        layout.addWidget(layoutHWidget)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        QTimer.singleShot(0, self.inputBox.setFocus)

        self.inputBox.returnPressed.connect(self.sendMessage)
        shortcut = QShortcut(Qt.Key.Key_Return, self.inputBox)
        shortcut.activated.connect(self.sendMessage)

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