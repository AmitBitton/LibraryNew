# library system project - OOP Project 3

## Overview
This project is a Library Management System written in python.  
The library System allows users (Librarians) to manage the books in the library. they allow to add books, search books, return books, romove books and 
lend books for clients.
The library System include observer notification system that send to the users (Librarians) and logger.
The system is built using object-oriented programming principles and incorporates various design patterns to ensure modularity and
maintainabilit.


## main features

### Book Managment
+ Users can add, remove, update, and search for books in the library.
+ Each book has details like title, author, genre, year, copies, and popularity counter.
+ Books are stored and retrieved from CSV files for persistence.

### Advanced Search System
Books can be searched using different criteria:
+ By Title
+ By Author
+ By Genre
+ By Year
  
Implements the Strategy Design Pattern, allowing flexible search functionality.
The search support Partial searches.

### User Authentication & Management
+ Users can register, login, and authenticate with secure password hashing.

### Borrowing & Returning Books
+ Users can borrow books if copies are available, else, they added to waiting list.
+ The popularity counter increases each time a book is borrowed or client add to waiting list.

### Notification System
+ Uses the Observer Design Pattern to notify librarians about book updates.
+ Notifications are sent when books are borrowed, returned, removed or added.

### Logging System
+ Implements the Decorator Design Pattern to automatically log actions.
+ Keeps track of all major operations for auditing (according to the assignment requirements).

### File Management & Persistence
+ All book and user data is stored in CSV files for easy access and tracking.
+ Implements functions for reading, writing, updating, and deleting book records.
  
Files Used in the System:
+ books.csv

Stores the entire book collection in the library.

+ available_books.csv

Stores only books that have available copies (not fully borrowed).

+ loaned_books.csv

Stores books that are currently loaned out to users.

+ books_update.csv

Includes title, author, year, copies, genre, is_loaned, popularity_counter, waiting_list, and borrowed_copies.
This file is used to track all book data comprehensively and ensure accuracy.

### Design Patterns Used
This project follows several design patterns to improve maintainability:
+ Observer Pattern → Notifies librarians about updates (Observer, Subject, Notifications).
+ Strategy Pattern → Allows different search methods (SearchStrategy).
+ Decorator Pattern → Automates logging of actions (LogManager).
+ Iterator Pattern → Implements iteration over search results with the BaseBookIterator in BookCollection (BookIterator in BookCollection) 
+ Singlton Pattern → Ensures only one instance of the Library is created.




## Wrotten by Amit Bitton and Lihi Cohen




