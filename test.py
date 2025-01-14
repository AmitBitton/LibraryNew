
import time
import pandas as pd
from Library import Library
from Book import Book
from FileManager import FileManager
from LogManager import LogManager

# Test code
library = Library()
test_book = Book("Test Book", "Test Author", "No", 1, "Fiction", 2024)

# Print the contents of CSV files before operations
print("\nBefore adding book:")
books = FileManager.read_from_csv('books.csv')
print("Books in CSV:", [f"{b.title} by {b.author}" for b in books])

# Add book
library.add_book(test_book)
time.sleep(7)

# Print after adding
print("\nAfter adding book:")
books = FileManager.read_from_csv('books.csv')
print("Books in CSV:", [f"{b.title} by {b.author}" for b in books])
# Try borrowing
library.borrow_book("Test Person", "123-456-7890", "test@test.com", test_book)
library.borrow_book("Test Person", "123-456-7890", "test@test.com", test_book)



# Print after borrowing
print("\nAfter borrowing:")
books = FileManager.read_from_csv('books.csv')
print("Books in CSV:", [f"{b.title} by {b.author}" for b in books])
print("before return")
library.return_book(test_book)
time.sleep(7)
print("after")
library.borrow_book("Test Person", "123-456-7890", "test@test.com", test_book)
