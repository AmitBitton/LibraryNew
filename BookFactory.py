from abc import abstractmethod
from Book import Book
from GenreType import GenreType


class BookFactory:

    @abstractmethod
    def create_book(self, title: str, author: str, is_loaned: str, copies: int, year: int) -> 'Book':
        if GenreType == GenreType.ADVENTURE:
            return Book(title,author,is_loaned,copies,GenreType.ADVENTURE,year)
        if GenreType == GenreType.EPIC_POETRY:
            return Book(title,author,is_loaned,copies,GenreType.EPIC_POETRY,year)
        if GenreType == GenreType.SCIENCE_FICTION:
            return Book(title,author,is_loaned,copies,GenreType.SCIENCE_FICTION,year)
        if GenreType == GenreType.PSYCHOLOGICAL_DRAMA:
            return Book(title,author,is_loaned,copies,GenreType.PSYCHOLOGICAL_DRAMA,year)
        if GenreType == GenreType.CLASSIC:
            return Book(title,author,is_loaned,copies,GenreType.CLASSIC,year)
        if GenreType == GenreType.DYSTOPIAN:
            return Book(title,author,is_loaned,copies,GenreType.DYSTOPIAN,year)
        if GenreType == GenreType.FANTASY:
            return Book(title,author,is_loaned,copies,GenreType.FANTASY,year)
        if GenreType == GenreType.FICTION:
            return Book(title,author,is_loaned,copies,GenreType.FICTION,year)
        if GenreType == GenreType.ROMANCE:
            return Book(title,author,is_loaned,copies,GenreType.ROMANCE,year)
        if GenreType == GenreType.TRAGEDY:
            return Book(title,author,is_loaned,copies,GenreType.TRAGEDY,year)
        if GenreType == GenreType.EPIC_POETRY:
            return Book(title,author,is_loaned,copies,GenreType.EPIC_POETRY,year)
        if GenreType == GenreType.EPIC_POETRY:
            return Book(title,author,is_loaned,copies,GenreType.EPIC_POETRY,year)
        if GenreType == GenreType.EPIC_POETRY:
            return Book(title,author,is_loaned,copies,GenreType.EPIC_POETRY,year)
        if GenreType == GenreType.EPIC_POETRY:
            return Book(title, author, is_loaned, copies, GenreType.EPIC_POETRY, year)


class AdventureBookFactory(Book):
    def __init__(self, title, author, is_loaned, copies, genre, year):
        super().__init__(title, author, is_loaned, copies, GenreType.ADVENTURE, year)

class EpicPoetryBookFactory(Book):
    def __init__(self, title, author, is_loaned, copies, genre, year):
        super().__init__(title, author, is_loaned, copies, GenreType.EPIC_POETRY, year)

