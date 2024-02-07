class User:
    def __init__(self, username):
        self.username = username
        self.next = None

class UserList:
    def __init__(self):
        self.head = None
    
    def add(self, username):
        newUser = User(username)
        if self.head is None:
            self.head = newUser
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = newUser

    def rem(self, username):
        current = self.head

        if current is not None and current.username == username:
            self.head = current.next
            return

        prev = None
        while current is not None and current.username != username:
            prev = current
            current = current.next

        if current is not None:
            prev.next = current.next
    
    def whatChanged(self, list_of_users):
        current = self.head
        current_usernames = set()

        while current is not None:
            current_usernames.add(current.username)
            current = current.next

        new_usernames = set(list_of_users)

        added_username = new_usernames - current_usernames
        removed_username = current_usernames - new_usernames

        if added_username: return {'op': 'add', 'names': list(added_username)[0]}
        if removed_username: return {'op': 'rem', 'names': list(removed_username)[0]}
    
    def printList(self):
        current = self.head
        user_list = []

        while current is not None:
            user_list.append(current.username)
            current = current.next

        print(user_list, end='')
    
    def returnList(self):
        current = self.head
        user_list = []

        while current is not None:
            user_list.append(current.username)
            current = current.next
        return user_list

if __name__ == "__main__":
    user_list = UserList()
    user_list.add("user1")
    user_list.add("user2")
    user_list.add("user3")

    new_usernames = ["user1", "user2"]

    changes = user_list.whatChanged(new_usernames)
    print(changes)
