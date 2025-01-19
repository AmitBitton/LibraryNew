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
+ The search support Partial searches.

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






