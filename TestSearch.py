import unittest
from typing import List
from SearchStrategy import SearchByTitle, SearchByAuthor, SearchByGenre, SearchByYear
from Book import Book
from FileManager import FileManager


class TestSearchStrategies(unittest.TestCase):

    def setUp(self):
        """Set up a small collection of books to use in search tests."""
        self.test_books = [
            Book("The Great Gatsby", "F. Scott Fitzgerald", 2, "Classic", 1925, "No"),
            Book("To Kill a Mockingbird", "Harper Lee", 3, "Fiction", 1960, "No"),
            Book("1984", "George Orwell", 4, "Dystopian", 1949, "Yes"),
            Book("Pride and Prejudice", "Jane Austen", 1, "Romance", 1813, "No"),
            Book("The Hobbit", "J.R.R. Tolkien", 5, "Fantasy", 1937, "No"),
        ]
        self.file_path = "test_books.csv"
        FileManager.write_to_csv(self.file_path, self.test_books)

    def test_search_by_title(self):
        """Test searching books by title."""
        strategy = SearchByTitle()

        # ✅ Search for an exact title
        results, found = strategy.search(self.file_path, "The Great Gatsby")
        self.assertTrue(found)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "The Great Gatsby")

        # ✅ Search with lowercase input (case-insensitivity check)
        results, found = strategy.search(self.file_path, "to kill a mockingbird")
        self.assertTrue(found)
        self.assertEqual(len(results), 1)

        # ❌ Search for a nonexistent title
        results, found = strategy.search(self.file_path, "Fake Book")
        self.assertFalse(found)
        self.assertEqual(len(results), 0)

    def test_search_by_author(self):
        """Test searching books by author name."""
        strategy = SearchByAuthor()

        # ✅ Search for a known author
        results, found = strategy.search(self.file_path, "Jane Austen")
        self.assertTrue(found)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Jane Austen")

        # ✅ Partial author search
        results, found = strategy.search(self.file_path, "Orwell")
        self.assertTrue(found)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "1984")

        # ❌ Search for a nonexistent author
        results, found = strategy.search(self.file_path, "Unknown Author")
        self.assertFalse(found)
        self.assertEqual(len(results), 0)

    def test_search_by_genre(self):
        """Test searching books by genre."""
        strategy = SearchByGenre()

        # ✅ Search for a known genre
        results, found = strategy.search(self.file_path, "Fiction")
        self.assertTrue(found)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].genre, "Fiction")

        # ✅ Search for a partial genre (e.g., "Dyst")
        results, found = strategy.search(self.file_path, "Dyst")
        self.assertTrue(found)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "1984")

        # ❌ Search for a genre not present
        results, found = strategy.search(self.file_path, "Amit")
        self.assertFalse(found)
        self.assertEqual(len(results), 0)

    def test_search_by_year(self):
        """Test searching books by publication year."""
        strategy = SearchByYear()

        # ✅ Search for a valid year
        results, found = strategy.search(self.file_path, "1925")
        self.assertTrue(found)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].year, 1925)

        # ❌ Search for a year that doesn't exist
        results, found = strategy.search(self.file_path, "2000")
        self.assertFalse(found)
        self.assertEqual(len(results), 0)

        # ❌ Ensure non-numeric input raises an error
        with self.assertRaises(ValueError):
            strategy.search(self.file_path, "year")


    def tearDown(self):
        """Cleanup test files after testing."""
        import os
        if os.path.exists(self.file_path):
            os.remove(self.file_path)


if __name__ == "__main__":
    unittest.main()
