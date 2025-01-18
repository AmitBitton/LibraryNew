import time
from math import lgamma

from Book import Book
from BookCollection import BookCollection
from FileManager import FileManager
from LogManager import LogManager
from Notifications import Notifications

class Library:
    _instance = None


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Library, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):  # Prevent reinitialization
            self._log_manager = LogManager()  # Instance-specific LogManager
            self._collection = BookCollection()  # Instance-specific collection
            self._paths = {
                "books": "books.csv",
                "available": "available_books.csv",
                "loaned": "loaned_books.csv",
            }
            self.notification_manager = Notifications()
            self.notification_manager.add_users_from_file('users.csv')
            self._collection.update_available_and_loaned_books()
            FileManager.save_books_to_file(self._collection.books(), 'books_update.csv')
            self.initialized = True  # Mark as initialized




    def get_collection(self):
        return self._collection  # Getter method

    @LogManager.log_action( lambda *args, **kwargs:"book borrowed")
    def borrow_book(self, name: str, phone_number: str, email: str, book: Book):
        try:
            for existing_book in self._collection.books():
                if book.equals(existing_book):
                    if not existing_book.is_loaned:
                        if existing_book.borrow_copy():
                            FileManager.update_book_info(self._paths, existing_book)
                            FileManager.save_books_to_file(self._collection.books(), 'books_update.csv')
                            print(f"The book {book.title} loaned to {name} successfully.")
                            self.notification_manager.notify_observers(f"The book {book.title} loaned to {name} successfully.")
                            return True
                    else:
                        existing_book.add_to_waiting_list(name, phone_number, email)
                        FileManager.save_books_to_file(self._collection.books(),'books_update.csv')
                        print(f"The book {book.title} can't be loaned to {name}. added {name} to waiting list.")
                        self.notification_manager.notify_observers(f"The book {book.title} can't be loaned to {name}. added {name} to waiting list.")
                        return False
            print(f"Book {book.title} not found in the collection.")
            return False

        except Exception as e:
            print(f"Error borrowing book: {str(e)}")
            return False


    @LogManager.log_action(lambda *args, **kwargs:"book returned")
    def return_book(self,  title: str, genre: str, year: int, author: str = None):
        try:
            book = self._collection.find_book(title,genre,author,year)
            if book is None:
                print(f"Book '{title}' ({year}) not found in collection.")
                return False

                # Check if book has any borrowed copies before attempting return
                # First check if any copies are borrowed
            if not any(status == "Yes" for status in book.borrowed_copies_status().values()):
                print(f"No borrowed copies of '{title}' by {author} to return.")
                return False

            if book.return_copy():
                print(f"The book {title} has been successfully returned and is now available.")
                FileManager.update_book_info(self._paths, book)
                FileManager.save_books_to_file(self._collection.books(), 'books_update.csv')
                self.notification_manager.notify_observers(
                f"The book {title} has been successfully returned and is now available."
            )
                self._collection.load_books()  # Reload updated books
                book = self._collection.find_book(title, genre, author, year)
            # Check waiting list
                next_client = book.remove_from_waiting_list()
                if next_client:
                    self.notification_manager.notify_observers(
                        f"Notify the client {next_client} that the book is now available."
                    )
                    self.borrow_book(next_client["name"], next_client["phone"], next_client["email"], book)

                    FileManager.update_book_info(self._paths, self._collection.find_book(title,genre,author,year))
                    FileManager.save_books_to_file(self._collection.books(), 'books_update.csv')
                return True

            else:
                print(f"Failed to return book '{title}' by {author}.")
                return False
        except (FileNotFoundError,ValueError) as e:
            print(f"Error returning book: {str(e)}")
            return False # Re-raise for the decorator to handle logging


    @LogManager.log_action( lambda *args, **kwargs:"book added")
    def add_book(self, book: Book):
        try:
            for existing_book in BookCollection.books(self._collection):
                if book.equals(existing_book):
                    existing_book.update_copies(book.copies+existing_book.copies)
                    FileManager.update_book_info(self._paths, existing_book)
                    FileManager.save_books_to_file(self._collection.books(), 'books_update.csv')
                    print(f"Updated copies of existing book {book.title}.")
                    self.notification_manager.notify_observers(f"Updated copies of existing book {book.title}.")
                    return True
            BookCollection.add_book(self._collection, book.title, book.author, book.genre, book.year, book.copies,
                                    book.is_loaned)
            FileManager.update_book_info(self._paths, book)
            FileManager.save_books_to_file(self._collection.books(), 'books_update.csv')
            print(f"Added new book {book.title} to library.")
            self.notification_manager.notify_observers(f"Added new book {book.title} to library.")
            return True
        except Exception as e:
            print(f"Error adding book: {str(e)}")
            return False



    @LogManager.log_action(lambda *args, **kwargs:"book removed")
    def remove_book(self,book:Book):
        try:
            for existing_book in BookCollection.books(self._collection):
                print(f"Checking: {existing_book.title} by {existing_book.author} | Copies: {existing_book.copies}")
                # DEBUGGING COMPARISON
                print(f"Comparing: '{book.title}' == '{existing_book.title}' -> {book.title == existing_book.title}")
                print(
                    f"Comparing: '{book.author}' == '{existing_book.author}' -> {book.author == existing_book.author}")
                print(f"Comparing: '{book.genre}' == '{existing_book.genre}' -> {book.genre == existing_book.genre}")
                print(f"Comparing: '{book.year}' == '{existing_book.year}' -> {book.year == existing_book.year}")
                if book.equals(existing_book):
                    print(f"✅ Match Found! Attempting to remove {existing_book.title}")

                    if BookCollection.remove_book(self._collection,existing_book):
                        print(f"The book '{book.title}' has been successfully removed from the library.")
                        self.notification_manager.notify_observers(f"The book '{book.title}' has been successfully removed from the library.")
                    FileManager.update_book_info(self._paths, existing_book)
                    FileManager.save_books_to_file(self._collection.books(), 'books_update.csv')
                    return True
            print(f"The book '{book.title}' does not exist in the library.")
            return False
        except Exception as e:
            print(f"Error removing book: {str(e)}")
            return False # Re-raise for the decorator to handle logging



