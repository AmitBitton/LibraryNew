class Book:
    # book constructor
    def __init__(self, title: str, author: str, is_loaned: str, copies: int, genre: str, year: int ):
        self._title = title
        self._author = author
        self._copies = copies
        self._genre = genre
        self._year = year
        self._waiting_list = []
        self._popularity_counter = 0
        if is_loaned == "Yes":
            self._borrowed_copies_status = {i: "Yes" for i in range(1, copies + 1)}
        else:
            self._borrowed_copies_status = {i: "No" for i in range(1, copies + 1)}

    @property
    def available_copies(self):
        return sum(1 for status in self._borrowed_copies_status.values() if status == "No")

    @property
    def borrowed_copies(self):
        return sum(1 for status in self._borrowed_copies_status.values() if status == "Yes")

    def add_to_waiting_list(self, name: str, phone_number: str, email: str):
        self._waiting_list.append({"name": name, "phone": phone_number, "email": email})
        self._popularity_counter += 1
        print(f"{name} added to the waiting list for the book: '{self.title}' by '{self._author} .")

    def remove_from_waiting_list(self):
        if self._waiting_list:
            return self._waiting_list.pop(0)
        return None

    def get_waiting_list(self):
        return self._waiting_list if self._waiting_list is not None else []

    def update_copies(self, num):
        if num >= self._copies:
            for i in range(self._copies + 1, num + 1):
                self._borrowed_copies_status[i] = "No"
            self._copies = num
        else:
            if num >= self.borrowed_copies:
                self._copies = num
                for j in range(1, self._copies + 1):
                    if self._borrowed_copies_status[j] == "No":
                        self._borrowed_copies_status.pop(j)
                        break
            print(f"The number of new copies must be greater than the {self.borrowed_copies} borrowed copies")

    def borrow_copy(self):
        if self.available_copies > 0:
            for key, value in self._borrowed_copies_status.items():
                if value == "No":
                    self._borrowed_copies_status[key] = "Yes"
                    self._popularity_counter += 1
                    return True
        return False

    def return_copy(self):
        for key, value in self._borrowed_copies_status.items():
            if value == "Yes":
                self._borrowed_copies_status[key] = "No"
                return True
        return False

    def to_csv_row(self) -> list:
        return [self._title, self._author, "Yes" if self.is_loaned else "No", self._copies, self._genre, self._year]

    @staticmethod
    def from_csv_row(row: list):
        return Book(
            title=row[0],
            author=row[1],
            is_loaned=row[2],
            copies=int(row[3]),
            genre=row[4],
            year=int(row[5])
        )

    @property
    def popularity_counter(self):
        return self._popularity_counter

    def __str__(self):
        return f"'{self._title}' by {self._author}'({self._year})-{self._genre}:{self._copies} total copies"

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def is_loaned(self):
        return sum(1 for status in self._borrowed_copies_status.values() if status == "No") == 0

    @property
    def copies(self):
        return self._copies

    @property
    def genre(self):
        return self._genre

    @property
    def year(self):
        return self._year

    def equals(self, other):
        if not isinstance(other, Book):
            return False
        return (self.title.lower() == other.title.lower() and
                self.author.lower() == other.author.lower())

    def update_book(self, other):
        if isinstance(other, Book):
            self._genre = other.genre
            self._year = other.year
            # Only update copies if the new number is larger
            if other.copies > self.copies:
                self.update_copies(other.copies - self.copies)
            # Update borrowed status while preserving existing loans
            for i in range(1, self.copies + 1):
                if i in other._borrowed_copies_status:
                    if other._borrowed_copies_status[i] == "Yes":
                        self._borrowed_copies_status[i] = "Yes"

    def borrowed_copies_status(self):
        return self._borrowed_copies_status
