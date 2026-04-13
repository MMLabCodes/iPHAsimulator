# Backward Compatibility Support

This folder contains the old `sw_*.py` module names for backward compatibility with existing code.

## What is this folder?

In the refactoring to **SatisPHAction Simulator v1.1**, all core modules were renamed with descriptive names:
- `sw_basic_functions.py` → `molecule_builder.py`
- `sw_directories.py` → `filepath_manager.py`
- `sw_build_systems.py` → `system_builder.py`
- (and 8 more...)

The old `sw_` prefixed modules are preserved here as import shims for migration.

## How to use

### For backward compatibility (existing code)
Your old imports continue to work:
```python
from modules.sw_basic_functions import vol_from_smiles
from modules.sw_build_systems import BuildAmberSystems
```

These will look in this `/compat/` folder and forward to the new modules.

### For new code (recommended)
Use the new descriptive names:
```python
from modules.molecule_builder import vol_from_smiles
from modules.system_builder import BuildAmberSystems
```

## Migration timeline

| Version | Status | Action |
|---------|--------|--------|
| v1.1 | Active | Old imports work, shims in /compat/ |
| v2.0 | Deprecated | Old imports still work with warnings |
| v3.0 | Removed | Only new names available |

## Setup

For the shims to work, ensure `/compat/` is in your Python path, or use:

```python
import sys
sys.path.insert(0, '/path/to/compat')
```

## Migration guide

See `/legacy/MIGRATION_GUIDE.md` for detailed instructions on updating your code to use new module names.

## What's in this folder

- **sw_basic_functions.py** → imports from `molecule_builder`
- **sw_directories.py** → imports from `filepath_manager`
- **sw_build_systems.py** → imports from `system_builder`
- **sw_openmm.py** → imports from `simulation_engine`
- **sw_analysis.py** → imports from `trajectory_analyzer`
- **sw_charge_benchmarking.py** → imports from `charge_calculator`
- **sw_orca.py** → imports from `quantum_calculator`
- **sw_file_formatter.py** → imports from `input_generator`
- **sw_custom_decorators.py** → imports from `decorators`
- **sw_complex_fluid_models.py** → imports from `complex_fluid_models`
- **sw_depreceated.py** → imports from `legacy/deprecated_functions`

## Troubleshooting

If imports from this folder fail:
1. Ensure the main `/modules/` folder is in your Python path
2. Check that the new descriptive modules exist in `/modules/`
3. See `/legacy/MIGRATION_GUIDE.md` for detailed help

---

**Note**: This folder will be removed in v3.0. Please migrate to new module names when possible.
