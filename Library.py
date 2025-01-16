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
            self.initialized = True  # Mark as initialized


    def _find_book(self, book: Book) -> Book | None:
        """Helper method to find a book in the collection"""
        for existing_book in self._collection.books():
            if book.equals(existing_book):
                return existing_book
        return None

    def get_collection(self):
        return self._collection  # Getter method

    @LogManager.log_action( lambda *args, **kwargs:"book borrowed")
    def borrow_book(self, name: str, phone_number: str, email: str, book: Book):
        for existing_book in BookCollection.books(self._collection):
            if book.equals(existing_book):
                if not existing_book.is_loaned:
                    if existing_book.borrow_copy():
                        if existing_book.is_loaned:
                            FileManager.update_book_info(self._paths, existing_book)
                            print(f"The book {book.title} loaned to {name} successfully.")
                            self.notification_manager.notify_observers(f"The book {book.title} loaned to {name} successfully.")
                            return True
                else:
                    existing_book.add_to_waiting_list(name, phone_number, email)
                    print(f"The book {book.title} can't be loaned to {name}. added {name} to waiting list.")
                    self.notification_manager.notify_observers(f"The book {book.title} can't be loaned to {name}. added {name} to waiting list.")
                    raise ValueError(f"Failed to loan book {book.title} to {name}.")
        raise ValueError(f"Book {book.title} not found in the collection.")


    @LogManager.log_action(lambda *args, **kwargs:"book returned")
    def return_book(self, book: Book):
        try:
            for existing_book in BookCollection.books(self._collection):
                if book.equals(existing_book):
                    if existing_book.return_copy():
                        print(f"The book {book.title} has been successfully returned.")
                        self.notification_manager.notify_observers(f"The book {book.title} has been successfully returned and is now available.")

                        next_client = existing_book.remove_from_waiting_list()
                        if next_client:
                            self.notification_manager.notify_observers(f"notify the client {next_client} that the book is now available.")
                            time.sleep(1)
                            self.borrow_book(next_client["name"], next_client["phone"], next_client["email"], existing_book)
                        FileManager.update_book_info(self._paths, existing_book)
                        return
            raise ValueError(f"Book '{book.title}' does not exist in the collection.")
        except Exception as e:
            print(f"Error returning book: {str(e)}")
            raise  # Re-raise for the decorator to handle logging



    @LogManager.log_action( lambda *args, **kwargs:"book added")
    def add_book(self, book: Book):
        try:
            for existing_book in BookCollection.books(self._collection):
                if book.equals(existing_book):
                    existing_book.update_copies(book.copies+existing_book.copies)
                    FileManager.update_book_info(self._paths, existing_book)
                    print(f"Updated copies of existing book {book.title}.")
                    self.notification_manager.notify_observers(f"Updated copies of existing book {book.title}.")
                    return
            BookCollection.add_book(self._collection, book.title, book.author, book.genre, book.year, book.copies,
                                    book.is_loaned)
            FileManager.update_book_info(self._paths, book)
            print(f"Added new book {book.title} to library.")
            self.notification_manager.notify_observers(f"Added new book {book.title} to library.")
        except Exception as e:
            print(f"Error adding book: {str(e)}")
            raise



    @LogManager.log_action(lambda *args, **kwargs:"book removed")
    def remove_book(self,book:Book):
        try:
            for existing_book in BookCollection.books(self._collection):
                if book.equals(existing_book):
                    if BookCollection.remove_book(self._collection,existing_book):
                        print(f"The book '{book.title}' has been successfully removed from the library.")
                        self.notification_manager.notify_observers(f"The book '{book.title}' has been successfully removed from the library.")
                    FileManager.update_book_info(self._paths, existing_book)
                    return
            raise ValueError(f"The book '{book.title}' does not exist in the library.")
        except Exception as e:
            print(f"Error removing book: {str(e)}")
            raise  # Re-raise for the decorator to handle logging



