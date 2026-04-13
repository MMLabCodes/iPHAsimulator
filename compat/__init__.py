"""
iPHAsimulator - Backward Compatibility Package

The modules in this folder maintain compatibility with v1.0 code that used
'sw_' prefixed module names. In v1.1, all modules were renamed to descriptive names.

Module mapping (old → new):
    sw_basic_functions  → molecule_builder
    sw_directories      → filepath_manager
    sw_build_systems    → system_builder
    sw_openmm           → simulation_engine
    sw_analysis         → trajectory_analyzer
    sw_charge_benchmarking → charge_calculator
    sw_orca             → quantum_calculator
    sw_file_formatter   → input_generator
    sw_custom_decorators → decorators
    sw_complex_fluid_models → complex_fluid_models_refactored

For new code, use the descriptive names from modules/:
    from modules.molecule_builder import vol_from_smiles   # recommended
    from compat.sw_basic_functions import vol_from_smiles  # still works

Deprecation timeline:
    v1.1: Shims available in compat/
    v2.0: Shims work but issue DeprecationWarnings
    v3.0: Shims removed; use descriptive names only
"""

# This __init__.py allows compat/ modules to be imported
# while maintaining backward compatibility

__all__ = [
    'sw_basic_functions',
    'sw_directories',
    'sw_build_systems',
    'sw_openmm',
    'sw_analysis',
    'sw_charge_benchmarking',
    'sw_orca',
    'sw_file_formatter',
    'sw_custom_decorators',
    'sw_complex_fluid_models',
    'sw_depreceated',
]
