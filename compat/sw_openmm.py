# -*- coding: utf-8 -*-
"""
DEPRECATED: Module sw_openmm has been refactored.

This module is maintained for backward compatibility only.
Please use the refactored module instead:

    from modules.simulation_engine import (
        BuildSimulation, AmberSimulation, ANISimulation, AcrylateReact,
        TopologyML, PositionsML, DataWriter, DcdWriter, get_rmsd
    )

This shim file imports all classes from the refactored simulation_engine module to maintain
backward compatibility with existing code.

Deprecated class usage:
    from modules.sw_openmm import BuildSimulation  # Use simulation_engine instead

Updated on: 2025-04-04
Original created on: Wed Mar 13 13:50:12 2024
@author: danie (refactoring contributions)
"""

import warnings

# Issue deprecation warning
warnings.warn(
    "The 'sw_openmm' module is deprecated and will be removed in a future version. "
    "Please import from 'simulation_engine' instead: "
    "from modules.simulation_engine import BuildSimulation, AmberSimulation, ANISimulation",
    DeprecationWarning,
    stacklevel=2
)

# Import all public classes from refactored module
from modules.simulation_engine import (
    TopologyML,
    PositionsML,
    DcdWriter,
    DataWriter,
    BuildSimulation,
    GromacsSimulation,
    AmberSimulation,
    ANISimulation,
    AcrylateReact,
    get_rmsd,
    __all__
)

# For backward compatibility - maintain old names
__all__ = [
    "TopologyML", "PositionsML", "DcdWriter", "DataWriter",
    "BuildSimulation", "GromacsSimulation", "AmberSimulation",
    "ANISimulation", "AcrylateReact", "get_rmsd"
]
