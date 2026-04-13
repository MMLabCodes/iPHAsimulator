# -*- coding: utf-8 -*-
"""
DEPRECATED: Module sw_analysis has been refactored.

This module is maintained for backward compatibility only.
Please use the refactored module instead:

    from modules.trajectory_analyzer import (
        Analysis, Universe, poly_Universe, bio_oil_Universe,
        master_poly_anal, master_bio_oil_anal, initialise_poly_analysis
    )

This shim file imports all classes from the refactored trajectory_analyzer module to maintain
backward compatibility with existing code.

Deprecated class usage:
    from modules.sw_analysis import Analysis  # Use trajectory_analyzer instead
    from modules.sw_analysis import Universe  # Use trajectory_analyzer instead

Updated on: 2025-04-04
Original created on: Tue Jun  4 11:13:57 2024
@author: danie (refactoring contributions)
"""

import warnings

# Issue deprecation warning
warnings.warn(
    "The 'sw_analysis' module is deprecated and will be removed in a future version. "
    "Please import from 'trajectory_analyzer' instead: "
    "from modules.trajectory_analyzer import Analysis, Universe, poly_Universe",
    DeprecationWarning,
    stacklevel=2
)

# Import all public classes from refactored module
from modules.trajectory_analyzer import (
    initialise,
    master_bio_oil_anal,
    master_poly_anal,
    Universe,
    poly_Universe,
    bio_oil_Universe,
    Analysis,
    universe_coord_extraction,
    initialise_poly_analysis,
    __all__
)

# For backward compatibility - maintain old names
__all__ = [
    "initialise", "master_bio_oil_anal", "master_poly_anal",
    "Universe", "poly_Universe", "bio_oil_Universe", "Analysis",
    "universe_coord_extraction", "initialise_poly_analysis"
]
