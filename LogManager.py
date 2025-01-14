import logging
from functools import wraps
from typing import Callable

from pyexpat.errors import messages


class LogManager:

    def __init__(self, log_file: str = "library_log.txt"):
        self.log_file = log_file
        self._configure_logger()

    def _configure_logger(self):
        self.logger = logging.getLogger("LibraryLogger")
        self.logger.setLevel(logging.INFO)

        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        # Add handler to logger
        if not self.logger.handlers:  # Prevent adding multiple handlers
            self.logger.addHandler(file_handler)

    def log_success(self, action: str):
        message = f"{action} successfully"
        self.logger.info(message)

    def log_fail(self, action: str):
        messages = f"{action} fail"
        self.logger.error(messages)

    @staticmethod
    def log_action(log_manager, action_name: Callable[..., str]):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                try:
                    result = func(self, *args, **kwargs)
                    log_manager.log_success(action_name(*args, **kwargs))
                    return result
                except Exception as e:
                    log_manager.log_fail(action_name(*args, **kwargs))
                    print(f"Error during action '{action_name(*args, **kwargs)}': {e}")  # Print the error message
                    return None

            return wrapper

        return decorator






