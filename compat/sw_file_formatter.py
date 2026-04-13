"""
Backward compatibility module for sw_file_formatter.

This module maintains backward compatibility with code that imports from
the old sw_file_formatter module. All functionality has been refactored
into the input_generator module with improved organization and documentation.

For new code, import directly from input_generator:
    from modules.input_generator import DFTInputGenerator

For legacy code, this module provides the same exports:
    from modules.sw_file_formatter import DFT_input_generator

Deprecated:
    This module is maintained for backward compatibility only.
    New code should import from modules.input_generator instead.
"""

from modules.input_generator import DFTInputGenerator, DFT_input_generator

__all__ = [
    'DFT_input_generator',
    'DFTInputGenerator',
]
