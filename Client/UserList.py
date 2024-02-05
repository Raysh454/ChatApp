class User:
    def __init__(self, username):
        self.username = username
        self.next = None

class UserList:
    def __init__(self):
        self.head = None
    
    def insert(self, username):
        newUser = User(username)
        if self.head is None:
            self.head = newUser
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = newUser
    
    def whatChanged(self, list_of_users):
        current = self.head
        current_usernames = set()

        while current is not None:
            current_usernames.add(current.username)
            current = current.next

        new_usernames = set(list_of_users)

        changes = []

        added_usernames = new_usernames - current_usernames
        for username in added_usernames:
            changes.append({"operation": "add", "username": username})

        removed_usernames = current_usernames - new_usernames
        for username in removed_usernames:
            changes.append({"operation": "rem", "username": username})

        return changes
if __name__ == "__main__":
    user_list = UserList()
    user_list.insert("user1")
    user_list.insert("user2")
    user_list.insert("user3")

    new_usernames = ["user1", "user2", "user3", "user4", "user5"]

    changes = user_list.whatChanged(new_usernames)
    print(changes)