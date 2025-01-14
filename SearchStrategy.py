from abc import ABC, abstractmethod
from typing import List
from LogManager import LogManager
from Book import Book


class Strategy(ABC):

    @abstractmethod
    def search(self, books: List[Book],query : str) -> List[Book] :
       pass


class SearchByTitle(Strategy):
    @LogManager.log_action(log_manager= LogManager, action_name= lambda books, query:f"Search book '{query}' by name completed ")
    def search(self, books: List[Book],query : str) -> List[Book]:
        if not query.strip():
            print("Warning: Empty query provided for title search.")



        return [book for book in books if query.lower() in book.title.lower()]


class SearchByAuthor(Strategy):
    @LogManager.log_action(log_manager= LogManager, action_name= lambda books, query:f"Search book '{query}' by author name completed ")
    def search(self, books: List[Book],query : str) -> List[Book]:
        return [book for book in books if query.lower() in book.author.lower()]


class SearchByGenre(Strategy):
    def search(self, books: List[Book],query : str) -> List[Book]:
        return [book for book in books if query.lower() in book.genre.lower()]


class SearchByYear(Strategy):
    def search(self, books: List[Book],query : str) -> List[Book]:
        if not query.isdigit():
            raise ValueError("Year must be numeric")
        year= int(query)
        return [book for book in books if book.year == year]



class SearchStrategy:

    def __init__(self, strategy :Strategy):
        self._strategy = strategy

    def set_Stratgy(self, strategy : Strategy):
        self._strategy=strategy

    def execute_search(self, books: List[Book], query: str) -> List[Book]:
        return self._strategy.search(books, query)



