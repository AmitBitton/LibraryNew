import logging
from functools import wraps
from typing import Callable, Optional


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
    def log_action(action_name: Callable[..., str]):
        """Decorator to log actions with dynamic query handling."""

        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                log_manager = LogManager()  # Create a LogManager instance
                query = kwargs.get("query") or (args[1] if len(args) > 1 else None)
                action_str = action_name(query) if query else action_name()

                result = func(self, *args, **kwargs)

                # Handle tuple return types (List[Book], bool)
                if isinstance(result, tuple) and isinstance(result[1], bool):
                    success = result[1]
                else:
                    success = bool(result)  # For cases where only list is returned

                if success:
                    log_manager.log_success(action_str)
                else:
                    log_manager.log_fail(action_str)

                return result

            return wrapper

        return decorator








