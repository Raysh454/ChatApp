### JSON Request and Response Examples:


#### Authenticate
```json
{
    "type": "AUTHENTICATE",
    "username": "your_username",
    "password": "your_password"
}
```
#### Register
```json
{
    "type": "REGISTER",
    "username": "new_username",
    "password": "new_password"
}
```
#### Message
```json
{
    "type": "MESSAGE",
    "session_id": "sender_session_id",
    "reciever": "BROADCAST",  #or a specific username, default is BROADCAST which just prints in console rn
    "message": "your_message"
}
```
#### Logout
```json
{
    "type": "LOGOUT",
    "session_id": "sender_session_id"
}
```
#### Success (Authentication)
```json
{
    "type": "SUCCESS",
    "msg": "Authentication successful",
    "session_id": "generated_session_id"
}
```
#### Error (Authentication)
```json
{
    "type": "ERROR",
    "msg": "Invalid username or password"
}
```
#### Message Broadcast
```json
{
    "type": "MESSAGE",
    "sender": "sender_username",
    "message": "broadcast_message_content"
}
```
#### Success (Registration)
```json
{
    "type": "SUCCESS",
    "msg": "User created"
}
```
#### Error (Registration)
```json
{
    "type": "ERROR",
    "msg": "Username exists"
}
```
#### Error (Unknown Request Type)
```json
{
    "type": "ERROR",
    "msg": "Unknown request type"
}
```

#### User list
```json
{
    "type": "USER_LIST",
    "users": {
        "Username": 0
    },
}
```
