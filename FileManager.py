import csv
from typing import List, Dict, TextIO, Union, IO
from Book import Book
import os



class FileManager:

    def __init__(self):
        pass

    @staticmethod
    def ensure_file_exists(path: str):
        """Ensure the CSV file exists with headers"""
        if not os.path.exists(path):
            with open(path, "w", newline="",encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "author", "is_loaned", "copies", "genre", "year"])


    @staticmethod
    def read_from_csv(path:str):
        books= []
        try:
            with open(path,"r",encoding="utf-8") as file:
                reader= csv.reader(file)
                next(reader)
                for row in reader:
                    books.append(Book.from_csv_row(row))
                return books
        except FileNotFoundError:
            print(f"File {path} not found.")
        except Exception as e:
            print(f"Error reading file {path}: {e}")
        return []

    @staticmethod
    def write_to_csv(path:str,books:List[Book]):
        try:
            with open(path,"w",newline="",encoding="utf-8") as file:
                writer= csv.writer(file)
                writer.writerow(["title", "author", "is_loaned", "copies", "genre", "year"])
                for book in books:
                    if book.copies > 0:
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
            if book.copies != 0:
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
        updated_books = []

        # Try to find the book and update it
        for i, book in enumerate(books):
            if book.equals(book_to_update):  # Using equals method to compare
                print(books[i]," , ", book_to_update)
                print(books[i].to_csv_row()," , ", book_to_update.to_csv_row())
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
            # available_books = FileManager.read_from_csv(paths["available"])
            # available_books = [book for book in available_books if not book.equals(book_to_update)]
            # FileManager.write_to_csv(paths["available"], available_books)
            FileManager.delete_row(paths["available"], book_to_update)

            loaned_books = FileManager.read_from_csv(paths["loaned"])
            existing_loaned = next((b for b in loaned_books if b.equals(book_to_update)), None)

            if existing_loaned:
                #Update existing loaned book
                loaned_books = [b if not b.equals(book_to_update) else book_to_update for b in loaned_books]
            else:
                # Add new loaned book
                loaned_books.append(book_to_update)

            FileManager.write_to_csv(paths["loaned"], loaned_books)
        else:
            # Remove from loaned and add to available
            # loaned_books = FileManager.read_from_csv(paths["loaned"])
            # loaned_books = [book for book in loaned_books if not book.equals(book_to_update)]
            # FileManager.write_to_csv(paths["loaned"], loaned_books)
            FileManager.delete_row(paths["loaned"], book_to_update)

            available_books = FileManager.read_from_csv(paths["available"])
            existing_available = next((b for b in available_books if b.equals(book_to_update)), None)

            if existing_available:
                # Update existing available book
                available_books = [b if not b.equals(book_to_update) else book_to_update for b in available_books]
            else:
                # Add new available book
                available_books.append(book_to_update)

            FileManager.write_to_csv(paths["available"], available_books)

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


    @staticmethod
    def load_books_from_file(file_path="books_update.csv"):
        books = []
        try:
            file_to_load = file_path if os.path.exists(file_path) else "Books.csv"

            with open(file_to_load, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    waiting_list = eval(row["waiting_list"]) if "waiting_list" in row and row["waiting_list"] else []
                    borrowed_copies = eval(row["borrowed_copies"]) if "borrowed_copies" in row and row["borrowed_copies"] else {}

                    book = Book(
                        title=row["title"],
                        author=row["author"],
                        year=int(row["year"]),
                        copies=int(row["copies"]),
                        genre=row["genre"],
                        is_loaned=row.get("is_loaned", "No"),
                        borrowed_copies=borrowed_copies,
                        waiting_list=waiting_list,
                        popularity_counter=int(row.get("popularity_counter", 0)),
                    )
                    books.append(book)

            print(f"Books loaded successfully from {file_to_load}.")
        except FileNotFoundError:
            print(f"File {file_path} not found. Returning an empty list.")
        except Exception as e:
            print(f"Error loading books: {e}")

        return books

    @staticmethod
    def save_books_to_file(books: list[Book], file_path="books_update.csv") -> None:
        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                fieldnames = ["title", "author", "year", "copies", "genre", "is_loaned", "popularity_counter", "waiting_list", "borrowed_copies"]

                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for book in books:
                    writer.writerow({
                        "title": book.title,
                        "author": book.author,
                        "year": book.year,
                        "copies": book.copies,
                        "genre": book.genre,
                        "is_loaned": "Yes" if book.is_loaned else "No",
                        "borrowed_copies": str(book.borrowed_copies_status()),
                        "waiting_list": book.get_waiting_list(),
                        "popularity_counter": book.popularity_counter,
                    })

            print(f"Books saved successfully to {file_path}.")
        except Exception as e:
            print(f"Error saving books: {e}")