
import time
import pandas as pd

from BookCollection import BookCollection
from Library import Library
from Book import Book
from FileManager import FileManager
from LogManager import LogManager
from Notifications import Notifications

# Test code
library = Library()
notifications = Notifications()

collection = BookCollection()
import csv

with open("test.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerow({"name": "Alice", "age": 30})

for existing_book in collection.books():
    print(existing_book.title,existing_book.copies,existing_book.available_copies)
# Add users from the users.csv file
notifications.add_users_from_file("users.csv")
# Notify all users
test_book = Book("Test Book", "Test Author",  1, "Fiction", 2024,"No")
library.add_book(test_book)
library.borrow_book("bob", "986259613","mail@mail@mail.com.mail", test_book)
library.borrow_book("tu", "986259613","mail@mail@mail.com.mail", test_book)

time.sleep(5)
library.return_book(test_book.title,test_book.genre,test_book.year,test_book.author)

