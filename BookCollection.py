from typing import Optional, List
from Book import Book
from BookNotFoundError import BookNotFoundError
from FileManager import FileManager
from SearchStrategy import SearchStrategy


class BookCollection:

    def __init__(self):
        self._books = FileManager.read_from_csv("books.csv")
        self.update_available_and_loaned_books()


    def update_available_and_loaned_books(self):
        """Separate books into available and loaned books and write to respective CSV files."""
        available_books = [book for book in self._books if not book.is_loaned]
        loaned_books = [book for book in self._books if book.is_loaned]

        FileManager.write_to_csv("available_books.csv", available_books)
        FileManager.write_to_csv("loaned_books.csv", loaned_books)

    def add_book(self, title, author, genre, year, copies, is_loaned="No"):
        for existing_book in self._books:
            if (existing_book.title == title and
                    existing_book.author == author and
                    existing_book.genre == genre and
                    existing_book.year == year):
                existing_book.update_copies(copies)
                return
        # add and update copy in book file and available book file
        new_book = Book(title, author, is_loaned, copies, genre, year)
        self._books.append(new_book)

    def remove_book(self, book: Book):
        for existing_book in self._books:
            if existing_book.equals(book):
                unborrowed_keys = [key for key, status in existing_book.borrowed_copies_status().items() if status == "No"]
                for key in unborrowed_keys:
                    existing_book.borrowed_copies_status().pop(key)
                #for i in range(1, book.copies + 1):
                   # if book.borrowed_copies_status()[i] =="No":
                       # book.borrowed_copies_status().pop(i)
                book.update_copies(len(book.borrowed_copies_status()))
                if book.copies == 0:
                    self._books.remove(book)
                    return True
                return False
        raise BookNotFoundError(f"Can not remove the book:'{book.title}' by {book.author} not found in the collection.")

    def search_book(self,strategy :SearchStrategy , query :str = None):
        result = strategy.search(self._books,query)
        return BookIterator(result)

    def __iter__(self):
        return BookIterator(self._books)

    def books(self):
        return self._books

    def get_10_popular_books(self):
        sorted_books= sorted(self.books(), key=lambda book:book._popularity_counter,reverse=True)
        return sorted_books[:10]

class BookIterator:
    def __init__(self, books: List[Book]):
        self._book_collection = books
        self._index = 0

    def __iter__(self):
        return self

    def has_next(self) -> bool:
        return self._index < len(self._book_collection)

    def __next__ (self):
        if self._index < len(self._book_collection):
            book = self._book_collection[self._index]
            self._index += 1
            return book
        else:
            raise StopIteration  # Standard way to end iteration

    def current(self) -> Optional['Book']:
        if 0 <= self._index < len(self._book_collection):
            return self._book_collection[self._index]
        return None

    def reset(self) -> None:
        self._index = 0
