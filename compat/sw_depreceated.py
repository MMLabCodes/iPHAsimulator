"""
Backward compatibility module for deprecated functions.

This module provides backward compatibility for code using deprecated functions
that have been moved to the /legacy/ folder. All functions have been archived but
are still accessible through this shim for backward compatibility.

DEPRECATION NOTICE:
    All functions in this module are deprecated and will be removed in v3.0.
    Please see /legacy/MIGRATION_GUIDE.md for migration instructions.

    To use deprecated functions:
    from legacy.deprecated_functions import gen_3_3_array

    For new code, import from the new modules instead:
    from modules.system_builder import BuildAmberSystems
    from modules.trajectory_analyzer import Analysis
"""

import warnings

# Issue deprecation warning when this module is imported
warnings.warn(
    "modules.sw_depreceated is deprecated. All functions have been moved to /legacy/deprecated_functions.py. "
    "See /legacy/MIGRATION_GUIDE.md for migration instructions. "
    "This module will be removed in v3.0.",
    DeprecationWarning,
    stacklevel=2
)

# Import all deprecated functions from the new location
from legacy.deprecated_functions import (
    build_3_3_polymer_array_old,
    gen_3_3_array,
    gen_2_2_array,
    parametrized_mols_avail,
    max_pairwise_distance,
    DeprecatedAnalysis,
)

# Maintain backward compatibility with __all__
__all__ = [
    'build_3_3_polymer_array_old',
    'gen_3_3_array',
    'gen_2_2_array',
    'parametrized_mols_avail',
    'max_pairwise_distance',
    'DeprecatedAnalysis',
    'Analysis',  # Deprecated analysis class alias
]

# For backward compatibility with old code that imported Analysis from here
Analysis = DeprecatedAnalysis
