"""
SatisPHAction Simulator - Core Modules

This package contains all core functionality for the SatisPHAction Simulator.

DESCRIPTIVE MODULE NAMES (v1.1+):
    ✓ molecule_builder - Molecular structure utilities
    ✓ filepath_manager - File and directory management
    ✓ system_builder - Prepare systems for MD simulations
    ✓ simulation_engine - OpenMM simulation wrapper
    ✓ trajectory_analyzer - Post-process MD results
    ✓ charge_calculator - Multi-method charge calculations
    ✓ quantum_calculator - Quantum chemistry integration
    ✓ input_generator - Generate simulation input files
    ✓ decorators - Utility decorators
    ✓ complex_fluid_models - Complex mixture modeling

BACKWARD COMPATIBILITY:
    Old imports still work:
        from modules.sw_basic_functions import vol_from_smiles

    New recommended imports:
        from modules.molecule_builder import vol_from_smiles

    For compat imports:
        from compat.sw_basic_functions import vol_from_smiles

MIGRATION:
    See /legacy/MIGRATION_GUIDE.md for detailed instructions.
    See /compat/README.md for backward compatibility details.

QUICK START:
    >>> from modules.molecule_builder import vol_from_smiles
    >>> volume = vol_from_smiles("CC(C)C")

DOCUMENTATION:
    See ARCHITECTURE.md for system design overview.
    See /examples/ for quick example scripts.
    See /tutorials/ for comprehensive guides.
"""
