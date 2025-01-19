import unittest
import os
from FileManager import FileManager
from Book import Book

class TestFileManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a temporary CSV file for testing."""
        cls.test_file = "test_books.csv"
        FileManager.ensure_file_exists(cls.test_file)

    def setUp(self):
        """Run before every test case."""
        self.book1 = Book("Test Book", "Test Author", 2, "Fiction", 2023, "No")
        self.book2 = Book("Another Book", "Another Author", 3, "Mystery", 2019, "No")
        FileManager.write_to_csv(self.test_file, [self.book1, self.book2])

    def test_read_from_csv(self):
        """Test reading books from a CSV file."""
        books = FileManager.read_from_csv(self.test_file)
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0].title, "Test Book")
        self.assertEqual(books[1].author, "Another Author")

    def test_append_to_csv(self):
        """Test appending a new book to the CSV file."""
        new_book = Book("New Book", "New Author", 1, "Adventure", 2025, "No")
        FileManager.append_to_csv(self.test_file, new_book)

        books = FileManager.read_from_csv(self.test_file)
        self.assertEqual(len(books), 3)
        self.assertEqual(books[2].title, "New Book")

    def test_update_book_info(self):
        """Test updating book information."""
        updated_book = Book("Test Book", "Test Author", 5, "Fiction", 2023, "No")

        paths = {
            "books": self.test_file,
            "loaned": "test_loaned.csv",
            "available": "test_available.csv"
        }

        FileManager.update_book_info(paths, updated_book)

        books = FileManager.read_from_csv(self.test_file)
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0].copies, 5)  # heck if copies were updated

    def test_delete_row(self):
        """Test deleting a book from the CSV file."""
        FileManager.delete_row(self.test_file, self.book1)

        books = FileManager.read_from_csv(self.test_file)
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Another Book")  # Only second book should remain

    def test_ensure_file_exists(self):
        """Test ensuring a file exists (should create if not found)."""
        temp_file = "temp_test_file.csv"
        FileManager.ensure_file_exists(temp_file)
        self.assertTrue(os.path.exists(temp_file))
        os.remove(temp_file)  # Cleanup

    def test_load_books_from_file(self):
        """Test loading books from a file."""
        books = FileManager.load_books_from_file(self.test_file)
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0].title, "Test Book")

    def test_save_books_to_file(self):
        """Test saving books to a file."""
        new_books = [Book("Save Test", "Author", 1, "Sci-Fi", 2022, "No")]
        FileManager.save_books_to_file(new_books, self.test_file)

        books = FileManager.load_books_from_file(self.test_file)
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Save Test")

    @classmethod
    def tearDownClass(cls):
        """Clean up the test file after all tests."""
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)

if __name__ == '__main__':
    unittest.main()
