import sqlite3
import secrets

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("test.db")
        self.cursor = self.connection.cursor()

        # Create a 'users' table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                session_id TEXT
            )
        ''')
        self.connection.commit()

    def sessionIsValid(self, sessionID):
        # Check if the sessionID is valid
        self.cursor.execute('SELECT * FROM users WHERE session_id = ?', (sessionID,))
        user = self.cursor.fetchone()
        return user is not None

    def createUser(self, username, password):
        # Insert the new user into the 'users' table using parameterized query
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.connection.commit()

    def isAnUser(self, username):
        # Check if the user already exists using parameterized query
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = self.cursor.fetchone()
        return user is not None

    def loginIsValid(self, username, password): 
        # Check the database for the username/password combination
        self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = self.cursor.fetchone()
        return user is not None

    def deleteSession(self, sessionID):
        # Delete a session associated with a user using parameterized query
        if self.sessionIsValid(sessionID):
            self.cursor.execute('UPDATE users SET session_id = NULL WHERE session_id = ?', (sessionID,))
            self.connection.commit()
            return True
        return False

    def assignSession(self, username):
        # Assign a session ID to a user using parameterized query
        session_id = secrets.token_hex(16)
        self.cursor.execute('UPDATE users SET session_id = ? WHERE username = ?', (session_id, username))
        self.connection.commit()
        return session_id

    def getSession(self, username):
        self.cursor.execute('SELECT session_id FROM users where username = ?', (username,))
        session_id = self.cursor.fetchone()
        return session_id

    def getUsername(self, session_id):
        self.cursor.execute('SELECT username FROM users where session_id = ?', (session_id,))
        username = self.cursor.fetchone()
        if username: return username[0]
