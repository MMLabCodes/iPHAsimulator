"""
SatisPHAction Simulator - Backward Compatibility Module

The modules in this folder maintain compatibility with v1.0 code that used 'sw_' prefixed module names.

In v1.1, all modules were renamed to descriptive names:
- sw_basic_functions → molecule_builder
- sw_directories → filepath_manager
- sw_build_systems → system_builder
- (etc.)

MIGRATION NOTICE:
   For new code, use the descriptive module names from /modules/.
   See /legacy/MIGRATION_GUIDE.md for migration instructions.

IMPORT COMPATIBILITY:
   Old: from compat.sw_basic_functions import vol_from_smiles
   New: from modules.molecule_builder import vol_from_smiles

DEPRECATION TIMELINE:
   v1.1: Shims available in /compat/
   v2.0: Shims work with deprecation warnings
   v3.0: Shims removed, only descriptive names available
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
