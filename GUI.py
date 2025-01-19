import re
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from Book import Book
from FileManager import FileManager
from Library import Library
from LogManager import LogManager
from Notifications import Notifications
from SearchStrategy import log_manager, SearchByTitle, SearchByAuthor, SearchByGenre, SearchByYear
from UserManager import UserManager


class LibraryApp:
    def __init__(self,window):
        self.window = window
        self.window.title("Library Management System")
        self.user_manager = UserManager()
        self.log_manager = LogManager()
        self.library = Library()
        self.notifications = Notifications()
        self.current_user = None
        self.init_welcome_screen()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def init_welcome_screen(self):
        self.clear_window()

        tk.Label(self.window, text="Welcome to the Library system!", font=("Arial", 16)).grid(row=0, column=0, columnspan=2,                                                                               pady=20)
        tk.Button(self.window, text="Login", command=self.login_screen).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(self.window, text="Register", command=self.register_screen).grid(row=2, column=0, columnspan=2,pady=10)

    def logout(self):
        """Logs out the current user and returns to the welcome screen."""
        self.log_manager.log_success("log out")
        self.current_user = None
        self.init_welcome_screen()

    def login_screen(self):
        self.clear_window()

        tk.Label(self.window, text="Login", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.window, text="Username:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        username_entry = tk.Entry(self.window)
        username_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Password:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        password_entry = tk.Entry(self.window, show="*")
        password_entry.grid(row=2, column=1, padx=5, pady=5)

        def login():
            username = username_entry.get()
            password = password_entry.get()

            if self.user_manager.authenticate_user(username,password):
                log_manager.log_success("logged in")
                self.current_user = username
                messagebox.showinfo("Success", "Logged in successfully!")
                self.init_main_menu()
            else:
                log_manager.log_fail("logged in")
                messagebox.showerror("Login failed", "Incorrect username or password")

        tk.Button(self.window, text="Login", command=login).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.window, text="Back", command=self.init_welcome_screen).grid(row=4, column=0, columnspan=2)

    def register_screen(self):
        self.clear_window()

        tk.Label(self.window, text="Register", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.window, text="Username:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        username_entry = tk.Entry(self.window)
        username_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Password:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        password_entry = tk.Entry(self.window, show="*")
        password_entry.grid(row=2, column=1, padx=5, pady=5)

        def register():
            username = username_entry.get()
            password = password_entry.get()

            if username and password:
                if self.user_manager.register_user(username, password):
                    self.log_manager.log_success("registered")
                    messagebox.showinfo("Success", "Registered successfully!")
                    self.init_welcome_screen()
                else:
                    self.log_manager.log_fail("registered")
                    messagebox.showerror("Error", "Username already exists")
            else:
                messagebox.showerror("Error", "Please fill out all fields")

        tk.Button(self.window, text="Register", command=register).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.window, text="Back", command=self.init_welcome_screen).grid(row=4, column=0, columnspan=2)

    def init_main_menu(self):
        self.clear_window()

        tk.Label(self.window, text=f"Welcome, {self.current_user}", font=("Arial", 16)).grid(row=0, column=0,columnspan=2, pady=10)
        tk.Button(self.window, text="Library Manage", command=self.show_library_manage).grid(row=1, column=0,columnspan=2, pady=5)
        tk.Button(self.window, text="Show My Notifications", command=self.show_notifications_screen).grid(row=2, column=0,columnspan=2, pady=5)
        tk.Button(self.window, text="Log Out", command=self.logout).grid(row=3, column=0, columnspan=2,pady=20)


    def show_library_manage(self):
        self.clear_window()
        tk.Button(self.window, text="Add Book", command=self.add_book_screen).grid(row=1, column=0, columnspan=2,pady=5)
        tk.Button(self.window, text="Remove Book", command=self.remove_book_screen).grid(row=2, column=0, columnspan=2,pady=5)
        tk.Button(self.window, text="Search Book", command=self.search_book_screen).grid(row=3, column=0, columnspan=2,pady=5)
        tk.Button(self.window, text="View Books", command=self.view_books_screen).grid(row=4, column=0, columnspan=2,pady=5)
        tk.Button(self.window, text="Lend Book", command=self.lend_book_screen).grid(row=5, column=0, columnspan=2,pady=5)
        tk.Button(self.window, text="Return Book", command=self.return_book_screen).grid(row=6, column=0, columnspan=2,pady=5)
        tk.Button(self.window, text="Popular Books", command=self.show_popular_books).grid(row=7, column=0, columnspan=2,pady=20)
        tk.Button(self.window, text="Back" , command= self.init_main_menu).grid(row=8, column=0, columnspan=2,pady=20)

    def show_notifications_screen(self):
        self.clear_window()
        tk.Label(self.window, text=f"{self.current_user}'s Notifications", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        user_notifications = self.library.notification_manager.get_user_notifications(self.current_user)

        print(f"Retrieving notifications for {self.current_user}: {user_notifications}")

        if user_notifications:
            for i, notification in enumerate(user_notifications, start=1):
                tk.Label(self.window, text=notification).grid(row=i, column=0, columnspan=2, pady=5)
        else:
            tk.Label(self.window, text="No new notifications at this time").grid(row=1, column=0, columnspan=2, pady=10)

        tk.Button(self.window, text="Back", command=self.init_main_menu).grid(row=len(user_notifications) + 2, column=0,columnspan=2, pady=20)



    def add_book_screen(self):
        self.clear_window()
        tk.Label(self.window, text="Add Book", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.window, text="Title").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        title_entry = tk.Entry(self.window)
        title_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Author").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        author_entry = tk.Entry(self.window)
        author_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Genre").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        genre_entry = tk.Entry(self.window)
        genre_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Year").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        year_entry = tk.Entry(self.window)
        year_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Copies").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        copies_entry = tk.Entry(self.window)
        copies_entry.grid(row=5, column=1, padx=5, pady=5)

        def add_book():
            title = title_entry.get()
            author = author_entry.get()
            genre = genre_entry.get()
            year = year_entry.get()
            copies = copies_entry.get()

            # Validation
            if not title or not author or not genre or not year or not copies:
                messagebox.showerror("Error", "All fields are required!")
                return
            # if not year.isdigit() or not copies.isdigit():
            #     messagebox.showerror("Error", "Year and Copies must be numeric!")
            #     return
            if not re.match(r"^-?\d+$", year):  # Allows negative years
                messagebox.showerror("Error", "Year must be a number!")
                return

            if not copies.isdigit() or int(copies) <= 0:  # Ensures copies are positive
                messagebox.showerror("Error", "Copies must be a positive number!")
                return
            try:
                # Create the book object and add it to the library
                book = Book(title, author, int(copies),genre,int(year),"No")
                self.library.add_book(book)
                messagebox.showinfo("Success", "Book added successfully!")
                self.show_library_manage()  # Redirect back to the main menu
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        tk.Button(self.window, text="Add Book", command=add_book).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(self.window, text="Back", command=self.init_main_menu).grid(row=7, column=0, columnspan=2,pady=10)

    def remove_book_screen(self):
        self.clear_window()
        tk.Label(self.window, text="Remove Book", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.window, text="Title").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        title_entry = tk.Entry(self.window)
        title_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Author").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        author_entry = tk.Entry(self.window)
        author_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Genre").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        genre_entry = tk.Entry(self.window)
        genre_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Year").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        year_entry = tk.Entry(self.window)
        year_entry.grid(row=4, column=1, padx=5, pady=5)


        def remove_book():
            title = title_entry.get()
            author = author_entry.get()
            genre = genre_entry.get()
            year = year_entry.get()

            if not title or not author or not genre or not year:
                messagebox.showerror("Error", "All fields are required!")
                return
            if not re.match(r"^-?\d+$", year):  # Allows negative years
                messagebox.showerror("Error", "Year must be a valid number (can be negative)!")
                return
            try:
                # Create a temporary book object to match the criteria
                book_to_remove = Book(title, author,  0, genre, int(year),"No")
                print(f"\n🔍 DEBUG: Trying to remove book -> {book_to_remove}\n")

                # ✅ Check if book exists before attempting removal
                existing_books = self.library.get_collection().books()
                found_books = [book for book in existing_books if book.equals(book_to_remove)]

                if not found_books:
                    messagebox.showwarning("Book Not Found", f"Book '{title}' ({year}) not found in the collection.")
                    return

                # ✅ Remove the book
                self.library.remove_book(found_books[0])
                FileManager.save_books_to_file(self.library.get_collection().books(), "books_update.csv")

                messagebox.showinfo("Success", f"Book '{title}' by {author} removed successfully!")
                self.show_library_manage()  # Redirect back to main menu

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        tk.Button(self.window, text="Remove Book", command=remove_book).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(self.window, text="Back", command=self.init_main_menu).grid(row=7, column=0, columnspan=2, pady=10)

    # def search_book_screen(self):
    #     self.clear_window()
    #     tk.Label(self.window, text="Search Book", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
    #
    #     # Search Entry
    #     search_entry = tk.Entry(self.window)
    #     search_entry.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
    #
    #     # Dropdown for search criteria
    #     search_criteria = tk.StringVar()
    #     search_criteria.set("Title")  # Default selection
    #
    #     criteria_dropdown = ttk.Combobox(self.window, textvariable=search_criteria, state="readonly",
    #                                      values=["Title", "Author", "Genre", "Year"])
    #     criteria_dropdown.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
    #
    #     # Frame for displaying search results
    #     results_frame = tk.Frame(self.window)
    #     results_frame.grid(row=3, column=0, columnspan=2, pady=10)  # Added more padding for better spacing
    #
    #     def dynamic_search(event=None):
    #         """Perform search dynamically and highlight search term."""
    #         query = search_entry.get().strip()
    #         if not query:
    #             for widget in results_frame.winfo_children():
    #                 widget.destroy()
    #             return
    #
    #         # Select search strategy
    #         strategy_map = {
    #             "Title": SearchByTitle(),
    #             "Author": SearchByAuthor(),
    #             "Genre": SearchByGenre(),
    #             "Year": SearchByYear()
    #         }
    #         strategy = strategy_map.get(search_criteria.get())
    #         if not strategy:
    #             return
    #
    #         # Perform search using BookIterator
    #         search_results = self.library.get_collection().search_book(strategy, query)
    #
    #         # Clear previous results
    #         for widget in results_frame.winfo_children():
    #             widget.destroy()
    #
    #         # Display results
    #         if not search_results.has_next():
    #             tk.Label(results_frame, text="No books found.", font=("Arial", 12, "italic")).grid(row=0, column=0,
    #                                                                                                padx=5, pady=5)
    #         else:
    #             row_index = 0
    #             while search_results.has_next():
    #                 book = search_results.__next__()  # ✅ Forces `__str__()` conversion
    #                 formatted_text = str(book).replace(query, f"**{query}**")  # Bold the query
    #
    #                 # Using `tk.Text` for text formatting (instead of `tk.Label`)
    #                 text_widget = tk.Text(results_frame, height=2, width=70, wrap="word", font=("Arial", 12))
    #                 text_widget.insert("insert", book)  # Insert full book text
    #                 start_idx = str(book).lower().find(query.lower())  # Find the position of the search term
    #                 if start_idx != -1:
    #                     end_idx = start_idx + len(query)
    #                     text_widget.tag_add("highlight", f"1.{start_idx}", f"1.{end_idx}")  # Apply highlight tag
    #                     text_widget.tag_config("highlight", font=("Arial", 12, "bold"))  # Bold the search term
    #
    #                 text_widget.config(state="disabled", relief="flat",
    #                                    bg=self.window.cget("bg"))  # Make text read-only
    #                 text_widget.grid(row=row_index, column=0, padx=10, pady=5)  # Add spacing
    #
    #                 row_index += 1
    #
    #     # Bind search entry to update results dynamically
    #     search_entry.bind("<KeyRelease>", dynamic_search)
    #
    #     # Back Button
    #     tk.Button(self.window, text="Back", command=self.init_main_menu).grid(row=4, column=0, columnspan=2, pady=10)

    def search_book_screen(self):
        """Displays the search book screen with dynamic search functionality in a structured table."""
        self.clear_window()
        tk.Label(self.window, text="Search Book", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        # Search Entry
        search_entry = tk.Entry(self.window, width=40)
        search_entry.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        # Dropdown for search criteria
        search_criteria = tk.StringVar()
        search_criteria.set("Title")  # Default selection

        criteria_dropdown = ttk.Combobox(self.window, textvariable=search_criteria, state="readonly",
                                         values=["Title", "Author", "Genre", "Year"])
        criteria_dropdown.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

        # Results Frame with Scrollbar
        results_frame = tk.Frame(self.window)
        results_frame.grid(row=3, column=0, columnspan=2, pady=10)

        # Scrollbar for table
        scrollbar = tk.Scrollbar(results_frame, orient="vertical")

        # Table (Treeview)
        columns = ("Title", "Author", "Genre", "Year", "Copies", "Loaned")
        results_table = ttk.Treeview(results_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)

        # Set column headings
        for col in columns:
            results_table.heading(col, text=col, anchor="w")
            results_table.column(col, width=150, anchor="w")  # Adjust width

        # Scrollbar Configuration
        scrollbar.config(command=results_table.yview)
        scrollbar.pack(side="right", fill="y")

        # Place Table
        results_table.pack(side="left", fill="both", expand=True)

        def case_insensitive_replace(text, query, replacement):
            """Replace query inside text, case-insensitive, but keep original case."""
            pattern = re.compile(re.escape(query), re.IGNORECASE)

            def match_case(m):
                return f"{replacement[0]}{m.group(0)}{replacement[1]}"  # Keep original match's case

            return pattern.sub(match_case, text)

        def dynamic_search(event=None):
            """Perform search dynamically and highlight search term."""
            query = search_entry.get().strip()
            if not query:
                results_table.delete(*results_table.get_children())  # Clear results
                return

            # Select search strategy
            strategy_map = {
                "Title": SearchByTitle(),
                "Author": SearchByAuthor(),
                "Genre": SearchByGenre(),
                "Year": SearchByYear()
            }
            strategy = strategy_map.get(search_criteria.get())
            if not strategy:
                return

            # Perform search
            search_results, has_results = self.library.get_collection().search_book(strategy, query)

            # Clear previous results
            results_table.delete(*results_table.get_children())

            if not has_results:
                results_table.insert("", "end", values=("No books found", "", "", "", "", ""))
                return

            # Display results in the table
            for book in search_results:
                if search_criteria.get() == "Title":
                    title = case_insensitive_replace(book.title, query, ("[","]"))
                else:
                    title = book.title

                if search_criteria.get() == "Author":
                    author = case_insensitive_replace(book.author, query, ("[","]"))
                else:
                    author = book.author

                if search_criteria.get() == "Genre":
                    genre = case_insensitive_replace(book.genre, query, ("[","]"))
                else:
                    genre = book.genre

                if search_criteria.get() == "Year":
                    year = case_insensitive_replace(str(book.year), query, ("[","]"))
                else:
                    year = book.year

                copies = book.copies
                loaned = "Yes" if book.is_loaned else "No"

                results_table.insert("", "end", values=(title, author, genre, year, copies, loaned))

        # Bind search entry to update results dynamically
        search_entry.bind("<KeyRelease>", dynamic_search)

        # Back Button
        tk.Button(self.window, text="Back", command=self.init_main_menu).grid(row=4, column=0, columnspan=2, pady=10)

    def view_books_screen(self):
        """Displays the book viewing options in the main window."""
        self.clear_window()

        tk.Label(self.window, text="View Books", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        # Button to view ALL books
        tk.Button(self.window, text="View All Books", command=self.view_all_books).grid(row=1, column=0, padx=5,
                                                                                        pady=10)

        # Button to view loaned books
        tk.Button(self.window, text="View Loaned Books", command=self.view_loaned_books).grid(row=2, column=0, padx=5,
                                                                                              pady=10)

        # Button to view available books
        tk.Button(self.window, text="View Available Books", command=self.view_available_books).grid(row=3, column=0,
                                                                                                    padx=5, pady=10)

        # Button to view books by genre
        tk.Button(self.window, text="View Books by Genre", command=self.view_books_by_genre_screen).grid(row=4,
                                                                                                         column=0,
                                                                                                         pady=10)

        # Back Button
        tk.Button(self.window, text="Back", command=self.init_main_menu).grid(row=5, column=0, columnspan=2, pady=20)

    def view_all_books(self):
        """Displays ALL books inside the main window with full details."""
        all_books = self.library.get_collection().books()  # Fetch all books
        if all_books:
            log_manager.log_success("Displayed all books")
        else:
            log_manager.log_fail("Displayed all books")
        self.show_books_table("All Books in Library", all_books, full_details=True)

    def show_books_table(self, title, books, full_details=False):
        """Displays books in a structured, centered Treeview table inside the main window."""
        self.clear_window()  # Clear the previous screen

        tk.Label(self.window, text=title, font=("Arial", 16)).pack(pady=10)

        # Frame for table and scrollbar
        table_frame = tk.Frame(self.window)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical")

        # Columns based on whether we need full details or not
        columns = ("Title", "Author", "Genre", "Year") if not full_details else (
        "Title", "Author", "Genre", "Year", "Copies", "Loaned")

        books_table = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)

        # Set column headings & adjust text alignment (CENTER)
        for col in columns:
            books_table.heading(col, text=col, anchor="center")  # Center column headers
            books_table.column(col, width=150, anchor="center")  # Center text inside cells

        # Scrollbar Configuration
        scrollbar.config(command=books_table.yview)
        scrollbar.pack(side="right", fill="y")
        books_table.pack(side="left", fill="both", expand=True)

        # Display books in the table
        if not books:
            empty_values = ["No books found"] + [""] * (len(columns) - 1)
            books_table.insert("", "end", values=empty_values)
        else:
            for book in books:
                book_values = (book.title, book.author, book.genre, book.year)

                if full_details:
                    book_values += (book.copies, "Yes" if book.is_loaned else "No")

                books_table.insert("", "end", values=book_values)

        # Back Button to return to the main menu
        tk.Button(self.window, text="Back", command=self.view_books_screen).pack(pady=10)

    def view_books_by_genre_screen(self):
        """Displays books by selected genre in a structured table format with a searchable dropdown."""
        self.clear_window()

        # Title Label
        tk.Label(self.window, text="View Books by Genre", font=("Arial", 16)).pack(pady=10)

        # Dropdown Frame
        dropdown_frame = tk.Frame(self.window)
        dropdown_frame.pack(pady=5)

        tk.Label(dropdown_frame, text="Select Genre:").pack(side="left", padx=5)

        # Fetch all genres
        all_genres = self.library.get_collection().get_all_genres()
        selected_genre = tk.StringVar()
        selected_genre.set(all_genres[0] if all_genres else "No genres found")

        # Create a searchable dropdown
        genre_dropdown = ttk.Combobox(dropdown_frame, textvariable=selected_genre, values=all_genres, state="normal",
                                      width=30)
        genre_dropdown.pack(side="left", padx=5)

        # Table Frame
        table_frame = tk.Frame(self.window)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical")

        # Table (Treeview)
        columns = ("Title", "Author", "Year")
        books_table = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)

        # Set column headings and adjust text alignment (CENTER)
        for col in columns:
            books_table.heading(col, text=col, anchor="center")  # Center column headers
            books_table.column(col, width=200, anchor="center")  # Center text inside cells

        # Scrollbar Configuration
        scrollbar.config(command=books_table.yview)
        scrollbar.pack(side="right", fill="y")
        books_table.pack(side="left", fill="both", expand=True)

        def display_books():
            """Fetch and display books based on selected genre in the table."""
            genre = selected_genre.get()
            books = self.library.get_collection().get_books_by_genre(genre)

            # Clear previous results
            books_table.delete(*books_table.get_children())

            if not books:
                books_table.insert("", "end", values=("No books found", "", ""))
                log_manager.log_fail("Displayed book by category")
            else:
                for book in books:
                    books_table.insert("", "end", values=(book.title, book.author, book.year))
                log_manager.log_success("Displayed book by category")

        def update_dropdown(event=None):
            """Filters the dropdown list based on user input."""
            typed_text = selected_genre.get().lower()
            filtered_genres = [genre for genre in all_genres if typed_text in genre.lower()]

            # Update dropdown values dynamically
            genre_dropdown["values"] = filtered_genres if filtered_genres else all_genres

        # Bind key release for dynamic search filtering
        genre_dropdown.bind("<KeyRelease>", update_dropdown)

        # Bind selection change to auto-update table
        genre_dropdown.bind("<<ComboboxSelected>>", lambda event: display_books())

        # Search Button
        tk.Button(self.window, text="Show Books", command=display_books, width=30).pack(pady=10)

        # Back Button
        tk.Button(self.window, text="Back", command=self.view_books_screen, width=30).pack(pady=10)

    def view_loaned_books(self):
        """Displays loaned books inside the main window (without opening a new one)."""
        loaned_books = FileManager.read_from_csv("loaned_books.csv")
        if loaned_books:
            log_manager.log_success("Displayed borrowed")
        else:
            log_manager.log_fail("Displayed borrowed")
        self.show_books_table("Loaned Books", loaned_books)

    def view_available_books(self):
        """Displays available books inside the main window (without opening a new one)."""
        available_books = FileManager.read_from_csv("available_books.csv")
        if available_books:
            log_manager.log_success("Displayed available")
        else:
            log_manager.log_fail("-	Displayed available ")
        self.show_books_table("Available Books", available_books)


    def lend_book_screen(self):
        self.clear_window()
        tk.Label(self.window, text="Lend Book", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        # Book Title
        tk.Label(self.window, text="Book Title:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        title_entry = tk.Entry(self.window)
        title_entry.grid(row=1, column=1, padx=5, pady=5)

        # Author Name (Optional)
        tk.Label(self.window, text="Author Name:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        author_entry = tk.Entry(self.window)
        author_entry.grid(row=2, column=1, padx=5, pady=5)

        # Book Year
        tk.Label(self.window, text="Book Year:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        year_entry = tk.Entry(self.window)
        year_entry.grid(row=3, column=1, padx=5, pady=5)

        # Book Genre
        tk.Label(self.window, text="Book Genre:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        genre_entry = tk.Entry(self.window)
        genre_entry.grid(row=4, column=1, padx=5, pady=5)

        # Borrower Name
        tk.Label(self.window, text="Borrower Name:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        borrower_entry = tk.Entry(self.window)
        borrower_entry.grid(row=5, column=1, padx=5, pady=5)

        # Phone Number
        tk.Label(self.window, text="Phone Number:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        phone_entry = tk.Entry(self.window)
        phone_entry.grid(row=6, column=1, padx=5, pady=5)

        # Email
        tk.Label(self.window, text="Email:").grid(row=7, column=0, sticky="e", padx=5, pady=5)
        email_entry = tk.Entry(self.window)
        email_entry.grid(row=7, column=1, padx=5, pady=5)

        def lend_book():
            """Handles the lending logic."""
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            year = year_entry.get().strip()
            genre = genre_entry.get().strip()
            borrower = borrower_entry.get().strip()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()

            # Validate fields
            if not title or not author or not year or not genre or not borrower or not phone or not email:
                messagebox.showerror("Error", "Please fill in all required fields.")
                return
            if not re.match(r"^-?\d+$", year):  # Allows negative years
                messagebox.showerror("Error", "Year must be a valid number (can be negative)!")
                return

            try:
                book_to_lend = Book(title, author, 1, genre, int(year),"No")  # Placeholder book object
                borrowed = self.library.borrow_book(borrower, phone, email, book_to_lend)
                if borrowed:
                    messagebox.showinfo("Success", f"Book '{title}' ({year}) loaned successfully to {borrower}!")
                else:
                    messagebox.showwarning("Added to Waiting List",
                                           f"The book '{title}' ({year}) is currently unavailable.\n"
                                           f"{borrower} has been added to the waiting list.")
                self.show_library_manage()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        # Lend Book Button
        tk.Button(self.window, text="Lend Book", command=lend_book).grid(row=8, column=0, columnspan=2, pady=10)

        # Back Button
        tk.Button(self.window, text="Back", command=self.init_main_menu).grid(row=9, column=0, columnspan=2, pady=10)

    def return_book_screen(self):
        self.clear_window()
        tk.Label(self.window, text="Return Book", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        # Book Title
        tk.Label(self.window, text="Book Title:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        title_entry = tk.Entry(self.window)
        title_entry.grid(row=1, column=1, padx=5, pady=5)

        # Author Name (Optional)
        tk.Label(self.window, text="Author Name:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        author_entry = tk.Entry(self.window)
        author_entry.grid(row=2, column=1, padx=5, pady=5)

        # Book Year
        tk.Label(self.window, text="Book Year:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        year_entry = tk.Entry(self.window)
        year_entry.grid(row=3, column=1, padx=5, pady=5)

        # Book Genre
        tk.Label(self.window, text="Book Genre:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        genre_entry = tk.Entry(self.window)
        genre_entry.grid(row=4, column=1, padx=5, pady=5)


        # def return_book():
        #     title = title_entry.get()
        #     author = author_entry.get()
        #     year = year_entry.get()
        #     genre = genre_entry.get()
        #
        #     # Validate input fields
        #     if not all([title, author, year, genre]):
        #         messagebox.showerror("Error", "All fields (Title, Author, Year, and Genre) are required!")
        #         return
        #
        #     if not year.isdigit():
        #         messagebox.showerror("Error", "Year must be a valid number!")
        #         return
        #
        #     year = int(year)
        #
        #     try:
        #         # First find the book
        #         found_book = self.library.get_collection().find_book(title, genre, author, year)
        #
        #         if found_book is None:
        #             messagebox.showerror("Error", f"Book '{title}' ({year}) was not found in the library.")
        #             return
        #
        #         # Check if the book is actually loaned
        #         if not found_book.is_loaned:
        #             messagebox.showerror("Error", f"Book '{title}' ({year}) is not currently borrowed!")
        #             return
        #             # Check if the book is actually loaned
        #         if not any(status == "Yes" for status in found_book.borrowed_copies_status().values()):
        #             raise ValueError(f"No borrowed copies of '{title}' ({year}) to return.")
        #         # Attempt to return the book
        #         self.library.return_book(found_book.title, found_book.genre, found_book.year, found_book.author)
        #         messagebox.showinfo("Success", f"Book '{title}' ({year}) returned successfully!")
        #         self.show_library_manage()
        #
        #     except Exception as e:
        #         messagebox.showerror("Error", f"Failed to return book: {str(e)}")
        #         raise
        #     # Return Button
        def return_book():
            # Get form data
            title = title_entry.get()
            author = author_entry.get()
            year = year_entry.get()
            genre = genre_entry.get()

            if not title:
                messagebox.showerror("Error", "Title is required.")
                return

            year = int(year) if year else None

            # Return the book

            if self.library.return_book(title=title, author=author, year=year,genre=genre):
                messagebox.showinfo("Success", f"Book '{title}' returned successfully!")
            else:
                messagebox.showerror("Error", f"Failed to return book")
            self.show_library_manage()

        tk.Button(self.window, text="Return Book", command=return_book).grid(row=5, column=0, columnspan=2, pady=10)

        # Back Button
        tk.Button(self.window, text="Back", command=self.init_main_menu).grid(row=6, column=0, columnspan=2, pady=10)

    def show_popular_books(self):
        self.clear_window()
        tk.Label(self.window, text="Popular Books", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        # Retrieve the 10 most popular books
        popular_books = self.library.get_collection().get_10_popular_books()

        if not popular_books:
            tk.Label(self.window, text="No popular books found.", font=("Arial", 12)).grid(row=1, column=0,
                                                                                           columnspan=2, pady=10)
        else:
            results_frame = tk.Frame(self.window)
            results_frame.grid(row=1, column=0, columnspan=2, pady=10)

            for i, book in enumerate(popular_books, start=1):
                waiting_list_count = len(book.get_waiting_list()) if book.get_waiting_list() else 0
                popularity_score = book.popularity_counter if hasattr(book, "popularity_counter") else 0  # Ensure no AttributeError
                book_text = (f"{i}. {book.title} by {book.author} ({book.year}) - "
                             f"Borrowed {book.borrowed_copies} times, "
                             f"{waiting_list_count} people in waiting list - "
                             f"Total Popularity Counter: {popularity_score}")
                tk.Label(results_frame, text=book_text, font=("Arial", 10), anchor="w", justify="left").grid(row=i,
                                                                                                             column=0,
                                                                                                             padx=5,
                                                                                                             pady=2,
                                                                                                             sticky="w")
        # Back button
        tk.Button(self.window, text="Back", command=self.init_main_menu).grid(row=3, column=0, columnspan=2, pady=10)



if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()