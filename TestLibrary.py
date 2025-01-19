import unittest

from BookCollection import BookCollection
from Library import Library
from Book import Book
from FileManager import FileManager


class TestLibrary(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup a fresh instance of Library before running tests."""
        cls.library = Library()
        cls.library._collection.load_books()  # Ensure books are loaded before tests

    def setUp(self):
        """Ensure fresh setup before each test."""
        self.library._collection.load_books()

    def test_add_new_book(self):
        """Test adding a new book to the library."""
        book = Book("New Book", "Test Author", 1, "Fiction", 2023, "No")
        result = self.library.add_book(book)
        self.assertTrue(result)

        # Verify book is added
        found_book = self.library.get_collection().find_book("New Book", "Fiction", "Test Author", 2023)
        self.assertIsNotNone(found_book)
        self.assertEqual(found_book.copies, 1)

    def test_add_duplicate_book(self):
        """Test adding a duplicate book increases copies."""
        book = Book("Duplicate Book", "Test Author", 1, "Fiction", 2023, "No")
        self.library.add_book(book)

        # Add the same book again
        result = self.library.add_book(book)
        self.assertTrue(result)

        # Verify book copies increased
        found_book = self.library.get_collection().find_book("Duplicate Book", "Fiction", "Test Author", 2023)
        self.assertIsNotNone(found_book)
        self.assertGreaterEqual(found_book.copies, 2)

    def test_remove_existing_book(self):
        """Test removing a book from the library."""
        book = Book("Book to Remove", "Test Author", 1, "Fiction", 2023, "No")
        self.library.add_book(book)
        result = self.library.remove_book(book)
        self.assertTrue(result)

        # Verify book is removed
        found_book = self.library.get_collection().find_book("Book to Remove", "Fiction", "Test Author", 2023)
        self.assertIsNone(found_book)

    def test_remove_non_existing_book(self):
        """Test removing a book that does not exist in the library."""
        book = Book("Nonexistent Book", "Unknown Author", 1, "Fantasy", 2025, "No")
        result = self.library.remove_book(book)
        self.assertFalse(result)

    def test_borrow_available_book(self):
        """Test borrowing a book that is available."""
        book = Book("Borrowable Book", "Test Author", 2, "Mystery", 2022, "No")
        self.library.add_book(book)

        result = self.library.borrow_book("Alice", "123456789", "alice@mail.com", book)
        self.assertTrue(result)



    def test_borrow_unavailable_book(self):
        """Test borrowing a book that is already loaned out."""
        book = Book("Loaned Book", "Test Author", 1, "Sci-Fi", 2021, "No")
        self.library.add_book(book)
        self.library.borrow_book("Bob", "987654321", "bob@mail.com", book)

        result = self.library.borrow_book("Charlie", "555444333", "charlie@mail.com", book)
        self.assertFalse(result)

        # Verify book is still loaned and Charlie is in the waiting list
        found_book = self.library.get_collection().find_book("Loaned Book", "Sci-Fi", "Test Author", 2021)
        self.assertTrue(found_book.is_loaned)
        self.assertGreaterEqual(len(found_book.get_waiting_list()), 1)

    def test_return_book(self):
        """Test returning a borrowed book."""
        book = Book("Returnable Book", "Test Author", 1, "Adventure", 2020, "No")
        self.library.add_book(book)
        self.library.borrow_book("David", "444555666", "david@mail.com", book)

        result = self.library.return_book(book.title, book.genre, book.year, book.author)
        self.assertTrue(result)

        # Verify book is available again
        found_book = self.library.get_collection().find_book("Returnable Book", "Adventure", "Test Author", 2020)
        self.assertFalse(found_book.is_loaned)

    def test_return_nonexistent_book(self):
        """Test returning a book that does not exist in the library."""
        result = self.library.return_book("Fake Book", "Fantasy", 2030, "Unknown Author")
        self.assertFalse(result)

    def test_return_book_with_waiting_list(self):
        """Test returning a book when someone is in the waiting list."""
        book = Book("Waitlist Book", "Test Author", 1, "Thriller", 2019, "No")
        self.library.add_book(book)
        self.library.borrow_book("Eve", "777888999", "eve@mail.com", book)

        # Another user tries to borrow the book (gets added to the waitlist)
        self.library.borrow_book("Frank", "666777888", "frank@mail.com", book)

        # Return the book
        result = self.library.return_book(book.title, book.genre, book.year, book.author)
        self.assertTrue(result)

        # Verify the book was automatically borrowed by Frank
        found_book = self.library.get_collection().find_book("Waitlist Book", "Thriller", "Test Author", 2019)
        self.assertTrue(found_book.is_loaned)

    def test_get_collection(self):
        """Test that get_collection() returns the BookCollection instance."""
        collection = self.library.get_collection()
        self.assertIsInstance(collection, BookCollection)

    def test_add_book_with_negative_year(self):
        """Test adding a book with a negative year (historical books)."""
        book = Book("The Odyssey", "Homer", 1, "Epic Poetry", -800, "No")
        result = self.library.add_book(book)
        self.assertTrue(result)

        # Verify book is added
        found_book = self.library.get_collection().find_book("The Odyssey", "Epic Poetry", "Homer", -800)
        self.assertIsNotNone(found_book)

    def test_add_book_with_zero_copies(self):
        """Test adding a book with zero copies should not be allowed."""
        book = Book("Zero Copies Book", "Author", 0, "Fiction", 2022, "No")
        result = self.library.add_book(book)
        self.assertFalse(result)

        # Verify book is not added
        found_book = self.library.get_collection().find_book("Zero Copies Book", "Fiction", "Author", 2022)
        self.assertIsNone(found_book)

    def test_return_unborrowed_book(self):
        """Test returning a book that was never borrowed."""
        book = Book("Unborrowed Book", "Test Author", 1, "Drama", 2015, "No")
        self.library.add_book(book)

        result = self.library.return_book(book.title, book.genre, book.year, book.author)
        self.assertFalse(result)

    def test_borrow_and_return_multiple_times(self):
        """Test borrowing and returning a book multiple times."""
        book = Book("Repeat Borrow", "Author", 1, "Comedy", 2022, "No")
        self.library.add_book(book)

        for _ in range(3):
            self.library.borrow_book("User", "111222333", "user@mail.com", book)
            self.assertTrue(self.library.return_book(book.title, book.genre, book.year, book.author))

    def test_add_long_title_book(self):
        """Test adding a book with an extremely long title."""
        long_title = "A" * 255
        book = Book(long_title, "Author", 1, "Biography", 2000, "No")
        result = self.library.add_book(book)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
