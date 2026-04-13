"""
Backward compatibility module for sw_orca.

This module maintains backward compatibility with code that imports from
the old sw_orca module. All functionality has been refactored into the
quantum_calculator module with improved organization and type hints.

For new code, import directly from quantum_calculator:
    from modules.quantum_calculator import OrcaMolecule, csv_to_orca_molecules

For legacy code, this module provides the same exports:
    from modules.sw_orca import orca_molecule, csv_to_orca_class

Deprecated:
    This module is maintained for backward compatibility only.
    New code should import from modules.quantum_calculator instead.
"""

from modules.quantum_calculator import (
    OrcaMolecule,
    csv_to_orca_molecules,
    orca_molecule,
    csv_to_orca_class,
)

__all__ = [
    'orca_molecule',
    'csv_to_orca_class',
    'OrcaMolecule',
    'csv_to_orca_molecules',
]
