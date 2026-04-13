"""
Backward compatibility module for sw_directories.

This module maintains backward compatibility with code that imports from
the old sw_directories module. All functionality has been refactored into
the filepath_manager module with improved organization, type hints, and
documentation.

For new code, import directly from filepath_manager:
    from modules.filepath_manager import PolySimManage, PolyDataDirs

For legacy code, this module provides the same exports:
    from modules.sw_directories import PolySimManage, PolyDataDirs

Deprecated:
    This module is maintained for backward compatibility only.
    New code should import from modules.filepath_manager instead.
"""

# Import all public classes and functions from the refactored module
from modules.filepath_manager import (
    PolySimManage,
    PolyDataDirs,
    BioOilDirs,
    ComplexModelDirs,
    DFTManager,
    DEFAULT_PACKMOL_PATH,
    DEFAULT_MAX_DFT_JOBS,
    DEFAULT_DFT_NPROCS,
    DEPRECATED_DIR_NAME,
)

__all__ = [
    'PolySimManage',
    'PolyDataDirs',
    'BioOilDirs',
    'ComplexModelDirs',
    'DFTManager',
    'complex_model_dirs',  # Legacy alias for ComplexModelDirs
    'DFT_manager',  # Legacy alias for DFTManager
]

# Aliases for backward compatibility with old naming conventions
complex_model_dirs = ComplexModelDirs
DFT_manager = DFTManager
