class Observer:
    def update(self, notification):
        pass



class LibraryUsers(Observer) :
    def __init__(self,username):
        self.username = username
        self.notifications = []

    def update(self, notification):
        self.notifications.append(notification)
        print(f"New notification for Librarian {self.username} : {notification}")