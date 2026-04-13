"""
Backward compatibility module for molecular structure utilities.

This module provides backward compatibility for code using the old sw_basic_functions
module name. All functions have been moved to the new molecule_builder module.

DEPRECATION NOTICE:
    This module is maintained for backward compatibility only. New code should
    import from `molecule_builder` instead:

    from modules.molecule_builder import vol_from_smiles, has_heteroatoms

    This shim will be maintained through v2.0, then removed in v3.0.
"""

# Import all functions from the new module for backward compatibility
from modules.molecule_builder import (
    vol_from_smiles,
    vol_from_mol,
    vol_from_pdb,
    estimated_volume,
    volume_model,
    has_heteroatoms,
    has_rings,
    pdb_to_mol,
    smiles_to_pdb,
    clean_mol_name,
    remove_conect_master_lines,
    write_output,
    get_homo_lumo_from_xyz,
    get_element_from_pdb_line,
    count_elements_in_pdb,
    calculate_molecular_weight,
    ATOMIC_WEIGHTS,
    VDW_RADII,
)

# Maintain old function name for backward compatibility
SmilesToPDB = smiles_to_pdb

__all__ = [
    'vol_from_smiles',
    'vol_from_mol',
    'vol_from_pdb',
    'estimated_volume',
    'volume_model',
    'has_heteroatoms',
    'has_rings',
    'pdb_to_mol',
    'smiles_to_pdb',
    'SmilesToPDB',  # old name for backward compat
    'clean_mol_name',
    'remove_conect_master_lines',
    'write_output',
    'get_homo_lumo_from_xyz',
    'get_element_from_pdb_line',
    'count_elements_in_pdb',
    'calculate_molecular_weight',
    'ATOMIC_WEIGHTS',
    'VDW_RADII',
]