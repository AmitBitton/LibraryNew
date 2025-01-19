import csv

from Observer import LibraryUsers, Observer
from User import User
class Notifications:

    def __init__(self):
        self._observers = []
        self._notifications = []

    def get_notifications_list(self):
        return self._notifications

    def add_users_from_file(self, users_file):
        try:
            with open(users_file, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if "username" in row:  # Ensure username column exists

                        # Create a LibraryUsers object for each user
                        librarian = LibraryUsers(row["username"])
                        self._observers.append(librarian)
                        print(f"Added librarian: {row['username']}")  # Debugging line
                    else:
                        print(f"Skipping row due to missing 'username': {row}")  # Debugging

            print(f"Final observer count: {len(self._observers)}")  # Debugging
           # print(f"All users loaded and added as observers from {users_file}.")
        except FileNotFoundError:
            print(f"Error: The file {users_file} was not found.")
        except Exception as e:
            print(f"An error occurred while loading users: {e}")

    def register_observer(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, notification: str):
        self._notifications.append(notification)
        print(f"Notifying observers: {len(self._observers)} total.")  # Debugging
        if not self._observers:
            print("Warning: No observers registered!")

        for observer in self._observers:
            observer.update(notification)
            print(f"Sent to: {observer.username}")  # Debugging

    def get_user_notifications(self, username):
        """Return notifications for a specific user"""
        for observer in self._observers:
            if observer.username == username:
                return observer.notifications  #  Fetch specific user's notifications
        return []