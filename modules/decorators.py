"""
Custom decorators for controlling method behavior and state.

This module provides utility decorators for managing method calls, including
tracking method invocation chains and modifying behavior based on call context.

Example:
    Using the call_from_method decorator::

        from modules.decorators import CustomDecorators

        class MyClass:
            @CustomDecorators.call_from_method
            def my_method(self):
                if self.called_from_another_method:
                    print("Called from another method")
                return "result"

        obj = MyClass()
        result = obj.my_method()
"""

from typing import Callable, Any
from functools import wraps

__all__ = [
    'CustomDecorators',
]


# ============================================================================
# CustomDecorators Class
# ============================================================================

class CustomDecorators:
    """
    Collection of custom decorators for method behavior control.

    Provides decorators for tracking method calls and modifying behavior
    based on call context.
    """

    @staticmethod
    def call_from_method(method: Callable[..., Any]) -> Callable[..., Any]:
        """
        Decorator to track when a method is called from another method.

        Sets a flag on the instance indicating that the method is being
        called from within another method. This can be used to modify
        behavior based on the call context.

        Args:
            method: The method to decorate.

        Returns:
            Wrapped method that sets/unsets called_from_another_method flag.

        Note:
            Sets the instance attribute 'called_from_another_method' to True
            during execution and False afterward.

        Example:
            >>> class MyClass:
            ...     @CustomDecorators.call_from_method
            ...     def process(self):
            ...         if self.called_from_another_method:
            ...             print("Called from another method")
            ...         return "done"
            ...
            >>> obj = MyClass()
            >>> result = obj.process()
        """
        @wraps(method)
        def wrapper(instance: Any, *args: Any, **kwargs: Any) -> Any:
            """
            Wrapper function that manages the called_from_another_method flag.

            Args:
                instance: The instance on which the method is called.
                *args: Positional arguments to pass to the method.
                **kwargs: Keyword arguments to pass to the method.

            Returns:
                Result of the wrapped method.

            Note:
                Checks for 'from_multiple' keyword argument and prints a message
                if present.
            """
            # Check if the calling method should modify the behavior
            from_multiple: bool = kwargs.get('from_multiple', False)

            # Set the flag indicating that the method is called from another method
            instance.called_from_another_method = True
            result: Any = method(instance, *args, **kwargs)
            instance.called_from_another_method = False

            # If called from multiple, modify behavior accordingly
            if from_multiple:
                print("Behavior modified for multiple universe call.")

            return result

        return wrapper
