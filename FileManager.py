import csv
from typing import List, Dict
from Book import Book
import os

class FileManager:

    def __init__(self):
        pass

    @staticmethod
    def ensure_file_exists(path: str):
        """Ensure the CSV file exists with headers"""
        if not os.path.exists(path):
            with open(path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "author", "is_loaned", "copies", "genre", "year"])


    @staticmethod
    def read_from_csv(path:str) -> List[Book]:
        books= []
        try:
            with open(path,"r") as file:
                reader= csv.reader(file)
                next(reader)
                for row in reader:
                    books.append(Book.from_csv_row(row))
        except FileNotFoundError:
            print(f"File {path} not found.")
        except Exception as e:
            print(f"Error reading file {path}: {e}")
        return books

    @staticmethod
    def write_to_csv(path:str,books:List[Book]):
        try:
            with open(path,"w",newline="") as file:
                writer= csv.writer(file)
                writer.writerow(["title", "author", "is_loaned", "copies", "genre", "year"])
                for book in books:
                    writer.writerow(book.to_csv_row())
        except Exception as e:
            print(f"Error writing to file {path}: {e}")

    @staticmethod
    def append_to_csv(path:str,book:Book):
        FileManager.ensure_file_exists(path)
        try:
                # First check if book already exists
            books = FileManager.read_from_csv(path)
            for existing_book in books:
                if existing_book.equals(book):
                    return  # Book already exists
            with open(path,"a",newline="") as file:
             #   reader = csv.reader(file)
              #  for row in reader:
              #      if book.to_csv_row() == row:
               #         return
                writer= csv.writer(file)
                writer.writerow(book.to_csv_row())
        except Exception as e:
            print(f"Error appending to file {path}: {e}")

    @staticmethod
    def update_book_info(paths: Dict[str, str], book_to_update: Book):
        # Read books from the main books file
        books = FileManager.read_from_csv(paths["books"])
        updated = False

        # Try to find the book and update it
        for i, book in enumerate(books):
            if book.equals(book_to_update):  # Using equals method to compare
                books[i] = book_to_update  # Replace the existing book
                updated = True
                break

        # If book wasn't found in the main list, append it
        if not updated:
            books.append(book_to_update)
            updated = True

        # Write updated books list back to the file
        FileManager.write_to_csv(paths["books"], books)

        # Handle available and loaned books
        if book_to_update.is_loaned:
            # Remove from available and add to loaned
            available_books = FileManager.read_from_csv(paths["available"])
            available_books = [book for book in available_books if not book.equals(book_to_update)]
            FileManager.write_to_csv(paths["available"], available_books)

            loaned_books = FileManager.read_from_csv(paths["loaned"])
            if not any(book.equals(book_to_update) for book in loaned_books):
                FileManager.append_to_csv(paths["loaned"], book_to_update)
        else:
            # Remove from loaned and add to available
            loaned_books = FileManager.read_from_csv(paths["loaned"])
            loaned_books = [book for book in loaned_books if not book.equals(book_to_update)]
            FileManager.write_to_csv(paths["loaned"], loaned_books)

            available_books = FileManager.read_from_csv(paths["available"])
            if not any(book.equals(book_to_update) for book in available_books):
                FileManager.append_to_csv(paths["available"], book_to_update)

        if updated:
            print(f"Updated book '{book_to_update.title}' successfully.")
        else:
            print(f"No matching book found to update.")

    @staticmethod
    def delete_row(path:str,book_to_delete: Book):
        books = FileManager.read_from_csv(path)
        filtered_books = [book for book in books if not book.equals(book_to_delete)]
        if len(filtered_books) < len(books):
            FileManager.write_to_csv(path,filtered_books)
            print(f"Deleted row successfully from {path}.")
        else:
            print("No matching row found to delete.")