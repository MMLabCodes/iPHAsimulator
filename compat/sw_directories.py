"""
iPHAsimulator - Backward Compatibility Shim for sw_directories.

This module maintains backward compatibility for code that imports from
the old 'sw_directories' module name. All functionality is now in
modules.filepath_manager.

For new code, use:
    from modules.filepath_manager import PolySimManage

For legacy code, this module still works:
    from compat.sw_directories import PolySimManage
"""

# Import all public classes and functions from the refactored module
from modules.filepath_manager import (
    PolySimManage,
    PolyDataDirs,
    BioOilDirs,
    ComplexModelDirs,
    DFTManager,
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
