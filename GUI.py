import tkinter as tk
from tkinter import ttk, messagebox
from UserManager import UserManager
from Library import Library
from Book import Book
from LogManager import LogManager


class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("800x600")
        self.current_frame = None
        self.user_manager = UserManager()
        self.library = Library()
        self.log_manager = LogManager()
        self.switch_frame(LoginFrame)

    def switch_frame(self, frame_class):
        """Destroy the current frame and replace it with a new one."""
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self)
        self.current_frame.pack(fill="both", expand=True)



class LoginFrame(tk.Frame):

    def __init__(self, master : LibraryApp):
        super().__init__(master)
        tk.Label(self, text="Login", font=("Arial", 20)).pack(pady=20)

        tk.Label(self, text="Username:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=10)
        tk.Button(self, text="Register", command=lambda: master.switch_frame(RegisterFrame)).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.master.user_manager.authenticate_user(username, password):
            messagebox.showinfo("Success", "Logged in successfully!")
            self.master.switch_frame(MainMenuFrame)
        else:
            messagebox.showerror("Error", "Invalid credentials")


class RegisterFrame(tk.Frame):
    def __init__(self, master:'LibraryApp'):
        super().__init__(master)
        tk.Label(self, text="Register", font=("Arial", 20)).pack(pady=20)

        tk.Label(self, text="Username:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Register", command=self.register).pack(pady=10)
        tk.Button(self, text="Back to Login", command=lambda: master.switch_frame(LoginFrame)).pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.master.user_manager.register_user(username, password):
            messagebox.showinfo("Success", "Registration successful!")
            self.master.switch_frame(LoginFrame)
        else:
            messagebox.showerror("Error", "Username already exists")


class MainMenuFrame(tk.Frame):
    def __init__(self, master:'LibraryApp'):
        super().__init__(master)
        tk.Label(self, text="Main Menu", font=("Arial", 20)).pack(pady=20)

        buttons = [
            "Add Book", "Remove Book", "Search Book", "View Books",
            "Lend Book", "Return Book", "Popular Books", "Logout"
        ]

        for button_text in buttons:
            tk.Button(self, text=button_text, width=20, command=lambda bt=button_text: self.handle_action(bt)).pack(pady=5)

    def handle_action(self, action):
        if action == "Add Book":
            self.master.switch_frame(AddBookFrame)
        elif action == "Remove Book":
            self.master.switch_frame(RemoveBookFrame)
        elif action == "Search Book":
            self.master.switch_frame(SearchBookFrame)
        elif action == "View Books":
            self.master.switch_frame(ViewBooksFrame)
        elif action == "Lend Book":
            self.master.switch_frame(LendBookFrame)
        elif action == "Return Book":
            self.master.switch_frame(ReturnBookFrame)
        elif action == "Popular Books":
            self.master.switch_frame(PopularBooksFrame)
        elif action == "Logout":
            self.master.switch_frame(LoginFrame)


class AddBookFrame(tk.Frame):
    def __init__(self, master :'LibraryApp'):
        super().__init__(master)
        tk.Label(self, text="Add Book", font=("Arial", 20)).pack(pady=20)
        # TODO: Add input fields for title, author, genre, year, and copies
        # TODO: Call Library.add_book() and LogManager.log_action()


class RemoveBookFrame(tk.Frame):
    def __init__(self, master :'LibraryApp'):
        super().__init__(master)
        tk.Label(self, text="Remove Book", font=("Arial", 20)).pack(pady=20)
        # TODO: Add input fields to identify the book to remove
        # TODO: Call Library.remove_book() and LogManager.log_action()


class SearchBookFrame(tk.Frame):
    def __init__(self, master :'LibraryApp'):
        super().__init__(master)
        tk.Label(self, text="Search Book", font=("Arial", 20)).pack(pady=20)
        # TODO: Add dropdown for search type (title, author, genre, year)
        # TODO: Call Library.search_book() with the appropriate SearchStrategy


class ViewBooksFrame(tk.Frame):
    def __init__(self, master :'LibraryApp'):
        super().__init__(master)
        tk.Label(self, text="View Books", font=("Arial", 20)).pack(pady=20)
        # TODO: Display all books in a table using ttk.Treeview


class LendBookFrame(tk.Frame):
    def __init__(self, master :'LibraryApp'):
        super().__init__(master)
        tk.Label(self, text="Lend Book", font=("Arial", 20)).pack(pady=20)
        # TODO: Add input fields to identify the book and user details
        # TODO: Call Library.borrow_book() and LogManager.log_action()


class ReturnBookFrame(tk.Frame):
    def __init__(self, master :'LibraryApp'):
        super().__init__(master)
        tk.Label(self, text="Return Book", font=("Arial", 20)).pack(pady=20)
        # TODO: Add input fields to identify the book to return
        # TODO: Call Library.return_book() and LogManager.log_action()


class PopularBooksFrame(tk.Frame):
    def __init__(self, master :'LibraryApp'):
        super().__init__(master)
        tk.Label(self, text="Popular Books", font=("Arial", 20)).pack(pady=20)
        # TODO: Display the top 10 books based on popularity using Library.get_10_popular_books()


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
