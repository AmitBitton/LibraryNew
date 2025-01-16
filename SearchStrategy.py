from abc import ABC, abstractmethod
from typing import List
from LogManager import LogManager
from Book import Book

log_manager = LogManager()
class SearchStrategy(ABC):

    #@abstractmethod
    def search(self, books: List[Book],query : str) -> List[Book] :
       pass


class SearchByTitle(SearchStrategy):
    @log_manager.log_action(lambda query:f"Search book '{query}' by name completed ")
    def search(self, books: List[Book],query : str) -> List[Book]:
        if not query.strip():
            print("Warning: Empty query provided for title search.")



        return [book for book in books if query.lower() in book.title.lower()]


class SearchByAuthor(SearchStrategy):
    @log_manager.log_action(lambda query:f"Search book '{query}' by author name completed ")
    def search(self, books: List[Book],query : str) -> List[Book]:
        return [book for book in books if query.lower() in book.author.lower()]


class SearchByGenre(SearchStrategy):
    def search(self, books: List[Book],query : str) -> List[Book]:
        return [book for book in books if query.lower() in book.genre.lower()]


class SearchByYear(SearchStrategy):
    def search(self, books: List[Book],query : str) -> List[Book]:
        if not query.isdigit():
            raise ValueError("Year must be numeric")
        return [book for book in books if query in str(book.year)]



#class SearchStrategy:

    #def __init__(self, strategy :SearchStrategy):
      #  self._strategy = strategy

    #def set_Stratgy(self, strategy : SearchStrategy):
      #  self._strategy=strategy

    #def execute_search(self, books: List[Book], query: str) -> List[Book]:
      #  return self._strategy.search(books, query)



