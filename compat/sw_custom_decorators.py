"""
Backward compatibility module for sw_custom_decorators.

This module maintains backward compatibility with code that imports from
the old sw_custom_decorators module. All functionality has been refactored
into the decorators module with improved documentation and type hints.

For new code, import directly from decorators:
    from modules.decorators import CustomDecorators

For legacy code, this module provides the same exports:
    from modules.sw_custom_decorators import CustomDecorators

Deprecated:
    This module is maintained for backward compatibility only.
    New code should import from modules.decorators instead.
"""

from modules.decorators import CustomDecorators

__all__ = [
    'CustomDecorators',
]
