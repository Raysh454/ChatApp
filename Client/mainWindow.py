import sys
from .Client import Client
from .UserList import UserList
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QMainWindow, QHBoxLayout, QStackedWidget, QLabel
from PyQt6.QtCore import QSize, QTimer, Qt
from PyQt6.QtGui import QIcon, QShortcut, QTextCharFormat, QColor, QTextCursor
import platform

# This code makes it so windows doesn't use Pythonw.exe's icon in taskbar
if platform.system() == "Windows":
    from ctypes import windll
    myappid = u'mycompany.myproduct.subproduct.version'  # stupid windows
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class chatApp(QMainWindow):
    def __init__(self, host, port):
        super().__init__()

        self.setWindowTitle("Chat Application")
        self.setMinimumSize(QSize(300, 400))
        self.setWindowIcon(QIcon('ChatApp/Icons/chat.png'))

        self.client = Client(host, port)
        self.client.connect()

        self.userList = UserList()

        self.stackedWidget = QStackedWidget(self)
        self.makeMenuUI()
        self.makeLoginUI()
        self.makeRegisterUI()
        self.makeChatUI()

        self.setCentralWidget(self.stackedWidget)

    def makeMenuUI(self):
        layout = QVBoxLayout()
        self.loginMenuButton = QPushButton("Login", self)
        self.loginMenuButton.clicked.connect(self.showLoginUI)
        layout.addWidget(self.loginMenuButton)

        self.registerMenuButton = QPushButton("Register", self)
        self.registerMenuButton.clicked.connect(self.showRegisterUI)
        layout.addWidget(self.registerMenuButton)

        # Center the widgets horizontally and vertically
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        menuWidget = QWidget()
        menuWidget.setLayout(layout)
        self.stackedWidget.addWidget(menuWidget)

    def makeLoginUI(self):
        layout = QVBoxLayout()

        # Username
        usernameLayout = QHBoxLayout()
        usernameText = QLabel("Username:")
        usernameText.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.loginUsernameField = QLineEdit(self)
        usernameLayout.addWidget(usernameText)
        usernameLayout.addWidget(self.loginUsernameField)
        layout.addLayout(usernameLayout)

        # Add some spacing
        layout.addSpacing(10)

        # Password
        passwordLayout = QHBoxLayout()
        passwordText = QLabel("Password:")
        passwordText.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        passwordLayout.addWidget(passwordText)

        self.loginPasswordField = QLineEdit(self)
        self.loginPasswordField.setEchoMode(QLineEdit.EchoMode.Password)
        passwordLayout.addWidget(self.loginPasswordField)
        layout.addLayout(passwordLayout)

        # Add some spacing
        layout.addSpacing(10)

        # Login Button
        self.loginButton = QPushButton("Login", self)
        self.loginButton.clicked.connect(self.handleLogin)

        # Center the login button horizontally
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.loginButton)
        buttonLayout.addStretch(1)
        layout.addLayout(buttonLayout)

        # Set layout spacing and alignment
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        loginWidget = QWidget()
        loginWidget.setLayout(layout)
        self.stackedWidget.addWidget(loginWidget)

    def makeRegisterUI(self):
        layout = QVBoxLayout()

        # Username
        usernameLayout = QHBoxLayout()
        usernameText = QLabel("Username:")
        usernameText.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.registerUsernameField = QLineEdit(self)
        usernameLayout.addWidget(usernameText)
        usernameLayout.addWidget(self.registerUsernameField)
        layout.addLayout(usernameLayout)

        # Add some spacing
        layout.addSpacing(10)

        # Password
        passwordLayout = QHBoxLayout()
        passwordText = QLabel("Password:")
        passwordText.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        passwordLayout.addWidget(passwordText)

        self.registerPasswordField = QLineEdit(self)
        self.registerPasswordField.setEchoMode(QLineEdit.EchoMode.Password)
        passwordLayout.addWidget(self.registerPasswordField)
        layout.addLayout(passwordLayout)

        # Add some spacing
        layout.addSpacing(10)

        # Register Button
        self.registerButton = QPushButton("Register", self)
        self.registerButton.clicked.connect(self.handleRegister)

        # Center the register button horizontally
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.registerButton)
        buttonLayout.addStretch(1)
        layout.addLayout(buttonLayout)

        # Set layout spacing and alignment
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        registerWidget = QWidget()
        registerWidget.setLayout(layout)
        self.stackedWidget.addWidget(registerWidget)

    def showLoginUI(self):
        self.stackedWidget.setCurrentIndex(1)  # Index of the login widget

    def showRegisterUI(self):
        self.stackedWidget.setCurrentIndex(2)  # Index of the register widget

    def handleLogin(self):
        if self.client.authenticate(self.loginUsernameField.text(), self.loginPasswordField.text()):
            self.client.receive_thread.start()  #Start receiving messages
            self.stackedWidget.setCurrentIndex(3)  # sends you to the chat UI
        else:
            print("Login Failed:", self.loginUsernameField.text(), self.loginPasswordField.text())

    def handleRegister(self):
        if self.client.register(self.registerUsernameField.text(), self.registerPasswordField.text()):
            self.stackedWidget.setCurrentIndex(0)  # sends you back to the shadow realm ; main menu
        else:
            print("Registration Failed:", self.registerUsernameField.text(), self.registerPasswordField.text())

    def makeChatUI(self):
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
        
        self.client.response_received.connect(self.handle_response)

        layoutH.setSpacing(10)
        layoutH.setContentsMargins(0, 10, 0, 0)
        layoutHWidget = QWidget()
        layoutHWidget.setLayout(layoutH)

        layout.addWidget(layoutHWidget)
        widget = QWidget()
        widget.setLayout(layout)

        self.stackedWidget.addWidget(widget)  # Add this line to set the chat UI in the stacked widget

        QTimer.singleShot(0, self.inputBox.setFocus)

        self.inputBox.returnPressed.connect(self.sendMessage)
        shortcut = QShortcut(Qt.Key.Key_Return, self.inputBox)
        shortcut.activated.connect(self.sendMessage)

    def sendMessage(self):
        message = self.inputBox.text()
        self.inputBox.clear()
        self.client.sendMessage(message)
        self.appendColoredMessage(self.client.username, message, "blue")
    
    def appendColoredMessage(self, username, message, color):
        cursor = self.messageDisplay.textCursor()
        if username != '':
            # Set the color for the username
            username_format = QTextCharFormat()
            username_format.setForeground(QColor(color))
            cursor.insertText(f"{username}: ", username_format)

            # Set the color for the message
            message_format = QTextCharFormat()
            message_format.setForeground(QColor("black"))
            cursor.insertText(f"{message}\n", message_format)

            # Move the cursor to the end to show the new message
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.messageDisplay.setTextCursor(cursor)
            self.messageDisplay.ensureCursorVisible()
        else:
            message_format = QTextCharFormat()
            message_format.setForeground(QColor("black"))
            cursor.insertText(f"{message}\n", message_format)

            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.messageDisplay.setTextCursor(cursor)
            self.messageDisplay.ensureCursorVisible()
    
    def handle_response(self, response):
        if response['type'] == 'USER_LIST':
            updated_users = list(response['users'].keys())
            changes = self.userList.whatChanged(updated_users)

            if changes['op'] == 'add':
                self.userList.add(changes['names'])
                print(f"User {changes['names']} joined the server.")
                #self.messageDisplay.append(f"User {changes['names']} joined the server.")
                self.appendColoredMessage('', f"User {changes['names']} joined the server.", 'black')
            elif changes['op'] == 'rem':
                self.userList.rem(changes['names'])
                print(f"User {changes['names']} left the server.")
                #self.messageDisplay.append(f"User {changes['names']} left the server.")
                self.appendColoredMessage('', f"User {changes['names']} left the server.", 'black')

            print("Updated User List:", self.userList.returnList())
        
        if response['type'] == 'MESSAGE':
            sender = response['sender']
            message = response['message']

            if sender != self.client.username:
                self.appendColoredMessage(sender, message, "green")
            else:
                self.appendColoredMessage(sender, message, "blue")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = chatApp('127.0.0.1', 9999)
    window.show()
    sys.exit(app.exec())
