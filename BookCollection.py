from typing import Optional, List
from Book import Book
from BookNotFoundError import BookNotFoundError
from FileManager import FileManager
from SearchStrategy import SearchStrategy


class BookCollection:

    def __init__(self):
        self._books = FileManager.load_books_from_file()

    def save_books(self):
        FileManager.save_books_to_file(self.books())

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
        new_book = Book(title, author,copies, genre, year, is_loaned)
        self._books.append(new_book)

    def remove_book(self, book: Book):
        print(f"\n🛠 DEBUG: Attempting to remove {book.title} by {book.author}")
        for existing_book in self._books:
            print(
                f"🔍 Checking existing book: {existing_book.title} | {existing_book.author} | Copies: {existing_book.copies}")

            if existing_book.equals(book):
                print(f"✅ Match Found! Removing book: {existing_book.title}")

                unborrowed_keys = [key for key, status in existing_book.borrowed_copies_status().items() if status == "No"]
                for key in unborrowed_keys:
                    existing_book.borrowed_copies_status().pop(key)
                #for i in range(1, book.copies + 1):
                   # if book.borrowed_copies_status()[i] =="No":
                       # book.borrowed_copies_status().pop(i)
                book.update_copies(len(book.borrowed_copies_status()))
                print(f"📉 Updated copies: {book.copies}")

                if book.copies == 0:
                    print(f"🚮 Removing book: {book.title} from collection")

                    self._books.remove(book)
                    return True
                return False
        print(f"❌ ERROR: Book '{book.title}' not found in collection.")

        raise BookNotFoundError(f"Can not remove the book:'{book.title}' by {book.author} not found in the collection.")

    def load_books(self):
        """Reloads books from the file to ensure the latest data is reflected."""
        self._books = FileManager.load_books_from_file()

    def search_book(self,strategy :SearchStrategy , query :str = None):
        result = strategy.search("books.csv",query)
        return BookIterator(result)

    def find_book(self, title :str, genre = None, author = None , year = None) :
        """Helper method to find a book in the collection"""
        for book in self._books:
            if book.title == title and  (genre is None or book.genre == genre) and (author is None or book.author == author) and (year is None or book.year == year):
                return book
        return None

    def __iter__(self):
        return BookIterator(self._books)

    def books(self) -> list[Book]:
        return self._books

    def get_10_popular_books(self):
        sorted_books= sorted(self.books(), key=lambda book:book.popularity_counter,reverse=True)
        return sorted_books[:10]

    def get_all_genres(self):
        """Returns a list of unique genres from all books."""
        return list(set(book.genre for book in self._books))

    def get_books_by_genre(self, genre):
        """Returns books that belong to the selected genre."""
        return [book for book in self._books if book.genre.lower() == genre.lower()]


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
