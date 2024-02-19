class User:
    def __init__(self, username):
        self.username = username
        self.next: User | None = None

class UserList:
    def __init__(self):
        self.head = None
   
    def addList(self, usernames):
        for username in usernames:
            self.add(username)

    def add(self, username):
        newUser = User(username)
        if self.head is None:
            self.head = newUser
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = newUser

    def removeList(self, usernames):
        for username in usernames:
            self.remove(username)

    def remove(self, username):
        current = self.head

        if current and current.username == username:
            self.head = current.next
            return

        prev = None
        while current and current.username != username:
            prev = current
            current = current.next

        if current and prev:
            prev.next = current.next
    
    def whatChanged(self, list_of_users):
        current = self.head
        current_usernames = set()

        while current:
            current_usernames.add(current.username)
            current = current.next

        new_usernames = set(list_of_users)

        added_username = new_usernames - current_usernames
        removed_username = current_usernames - new_usernames

        if added_username: return {'op': 'add', 'names': list(added_username)}
        if removed_username: return {'op': 'rem', 'names': list(removed_username)}
    
    def printList(self):
        current = self.head
        user_list = []

        while current:
            user_list.append(current.username)
            current = current.next

        print(user_list, end='')
    
    def returnList(self):
        current = self.head
        user_list = []

        while current:
            user_list.append(current.username)
            current = current.next
        return user_list

if __name__ == "__main__":
    user_list = UserList()
    user_list.add("user1")
    user_list.add("user2")
    user_list.add("user3")

    new_usernames = ["user1"]

    changes = user_list.whatChanged(new_usernames)
    print(changes)
