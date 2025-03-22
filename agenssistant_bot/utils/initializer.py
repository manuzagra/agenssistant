from abc import ABC, abstractmethod
from functools import wraps
from inspect import iscoroutinefunction

from telegram import Update
from telegram.ext import ContextTypes


class Initializer(ABC):
    """Base class for initializers."""

    @abstractmethod
    def is_initialized(self, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """This method checks if the context is initialized.

        Args:
            context (ContextTypes.DEFAULT_TYPE): context of the bot.

        Returns:
            bool: True if the context is initialized, otherwise False.
        """
        pass

    @abstractmethod
    def __call__(self, context: ContextTypes.DEFAULT_TYPE) -> None:
        """This method initializes the context.

        Args:
            context (ContextTypes.DEFAULT_TYPE): context of the bot.
        """
        pass


def ensure_initialized(initializer=None):
    """Decorator factory to ensure the user is initialized before executing the handler."""
    if issubclass(initializer, Initializer):
        raise TypeError("The initializer must be a subclass of Initializer.")

    def decorator(func):
        @wraps(func)
        def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            if not initializer.is_initialized(context):
                initializer(context)
            return func(update, context)

        @wraps(func)
        async def wrapper_async(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            if not initializer.is_initialized(context):
                initializer(context)
            return await func(update, context)

        return wrapper_async if iscoroutinefunction(func) else wrapper

    return decorator


class EnsureInitialized:
    """Class to ensure the user is initialized before executing the handler."""

    def __init__(self, initializer=None):
        if not isinstance(initializer, Initializer):
            raise TypeError("The initializer must be a subclass of Initializer.")
        self.initializer = initializer

    def _do_init(self, context: ContextTypes.DEFAULT_TYPE):
        if not self.initializer.is_initialized(context):
            self.initializer(context)

    def __call__(self, func):
        @wraps(func)
        def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            self._do_init(context)
            return func(update, context)

        @wraps(func)
        async def wrapper_async(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            self._do_init(context)
            return await func(update, context)

        return wrapper_async if iscoroutinefunction(func) else wrapper
