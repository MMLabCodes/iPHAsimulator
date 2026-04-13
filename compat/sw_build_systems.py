# -*- coding: utf-8 -*-
"""
DEPRECATED: Module sw_build_systems has been refactored.

This module is maintained for backward compatibility only.
Please use the refactored module instead:

    from modules.system_builder import BuildSystems, BuildAmberSystems, PrepPackmolForAmber

This shim file imports all classes from the refactored system_builder module to maintain
backward compatibility with existing code.

Deprecated class usage:
    from modules.sw_build_systems import BuildSystems  # Use system_builder instead

Updated on: 2025-04-04
Original created on: Tue Mar 19 10:00:30 2024
@author: danie (refactoring contributions)
"""

import warnings

# Issue deprecation warning
warnings.warn(
    "The 'sw_build_systems' module is deprecated and will be removed in a future version. "
    "Please import from 'system_builder' instead: "
    "from modules.system_builder import BuildSystems, BuildAmberSystems, PrepPackmolForAmber",
    DeprecationWarning,
    stacklevel=2
)

# Import all public classes from refactored module
from modules.system_builder import (
    BuildSystems,
    BuildAmberSystems,
    PrepPackmolForAmber,
    FORBIDDEN_RESIDUE_CODES,
    __all__
)

# For backward compatibility - maintain old names
__all__ = ["BuildSystems", "BuildAmberSystems", "PrepPackmolForAmber"]
