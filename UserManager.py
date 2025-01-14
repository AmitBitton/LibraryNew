from typing import Dict, Optional
from User import User
import csv
class UserManager:

    def __init__(self,file_path= 'users.csv'):
        self.__file_path=file_path
        self.__users: Dict[str, User] = {}
        self.__load_users()


    #Load users from CSV file
    def __load_users(self):
        try:
            with open(self.__file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    user = User(row['username'], '')
                    user.password_hash = row['password_hash']  # Set the hash directly
                    self.__users[user.username] = user
            print("Users loaded successfully from the file.")
        except FileNotFoundError:
            # Create new file with headers if it doesn't exist
            with open(self.__file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['username', 'password_hash'])
            print("No users file found. Created a new file.")
        except Exception as e:
            print(f"Error loading users: {e}")


    #Save users to CSV file
    def __save_users(self):
        try:
            with open(self.__file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['username', 'password_hash'])
                for user in self.__users.values():
                    writer.writerow([user.username, user.password_hash])
            print("Users saved successfully to the file.")
            return True
        except Exception as e:
            print(f"Failed to save users: {str(e)}")
            return False

    #register a new user to the library system
    def register_user(self, username: str, password: str) -> bool:
        if username in self.__users:
            print(f"Registration failed: Username {username} already exists")
            return False

        #create new user for the librarian
        new_user = User(username, password)
        self.__users[username] = new_user
        if self.__save_users():
            print(f"User '{username}' registered successfully.")
            return True
        print(f"Registration failed for user '{username}'.")
        return False


    #Authenticate a user
    def authenticate_user(self, username: str, password: str) -> bool:
        user = self.__users.get(username)
        if user and user.verify_password(password):
            print(f"User '{username}' authenticated successfully.")
            return True
        print(f"Authentication failed for user '{username}'.")
        return False


#Get user by username
    def get_user(self, username: str) -> Optional[User]:
        user = self.__users.get(username)
        if user:
            print(f"User '{username}' found.")
        else:
            print(f"User '{username}' not found.")
        return user



# Add this debug method to UserManager
    def debug_print_users(self):
        print("Current users in memory:")
        for username, user in self.__users.items():
         print(f"Username: {username}, Hash: {user.password_hash}")

    # Add this to test the specific login case
    def test_authentication(username: str, password: str):
        user = User(username, password)
        print(f"Test hash for '{password}': {user.password_hash}")


