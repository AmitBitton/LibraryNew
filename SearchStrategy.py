from abc import ABC, abstractmethod
from typing import List, Tuple

from FileManager import FileManager
from LogManager import LogManager
from Book import Book

log_manager = LogManager()
class SearchStrategy(ABC):

    #@abstractmethod
    # def search(self, books: List[Book],query : str)  :
    #    pass

    def search(self, file_path : str ,query : str)  :
       pass


class SearchByTitle(SearchStrategy):
    @log_manager.log_action(lambda query:f"Search book '{query}' by name completed")
    def search(self, file_path : str ,query : str) ->Tuple[List[Book], bool]:
        if not query.strip():
            print("Warning: Empty query provided for title search.")
            return [], False
        books = FileManager.read_from_csv(file_path)
        if books is None:
            return [], False
        results = [book for book in books if query.lower() in book.title.lower()]
        return results, bool(results)


class SearchByAuthor(SearchStrategy):
    @log_manager.log_action(lambda query:f"Search book '{query}' by author name completed")
    def search(self, file_path : str ,query : str) -> Tuple[List[Book], bool]:
        books = FileManager.read_from_csv(file_path)
        if books is None:
            return [], False
        results= [book for book in books if query.lower() in book.author.lower()]
        return results,bool(results)


class SearchByGenre(SearchStrategy):
    def search(self, file_path : str ,query : str) -> Tuple[List[Book], bool]:
        books = FileManager.read_from_csv(file_path)
        if books is None:
            return [], False
        results = [book for book in books if query.lower() in book.genre.lower()]
        return results, bool(results)


class SearchByYear(SearchStrategy):
    def search(self, file_path : str ,query : str) -> Tuple[List[Book], bool]:
        if not query.isdigit():
            raise ValueError("Year must be numeric")
        books = FileManager.read_from_csv(file_path)
        if books is None:
            return [], False
        results = [book for book in books if query == str(book.year)]
        return results, bool(results)








