{
    "type": "AUTHENTICATE",
    "username": "your_username",
    "password": "your_password"
},
{
    "type": "REGISTER",
    "username": "new_username",
    "password": "new_password"
},
{
    "type": "MESSAGE",
    "session_id": "sender_session_id",
    "reciever": "BROADCAST", //or a specific username, default is BROADCAST which just prints in console rn
    "message": "your_message"
},
{
    "type": "LOGOUT",
    "session_id": "sender_session_id"
},
{
    "type": "SUCCESS",
    "msg": "Authentication successful",
    "session_id": "generated_session_id"
},
{
    "type": "ERROR",
    "msg": "Invalid username or password"
},
{
    "type": "MESSAGE",
    "sender": "sender_username",
    "message": "broadcast_message_content"
},
{
    "type": "SUCCESS",
    "msg": "User created"
},
{
    "type": "ERROR",
    "msg": "Username exists"
},
{
    "type": "ERROR",
    "msg": "Unknown request type"
}
