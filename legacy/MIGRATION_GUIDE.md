# Legacy Functions - Migration Guide

This folder contains deprecated functions that are no longer actively maintained. While they are preserved for backward compatibility, **you should migrate to the new implementations as soon as possible**.

## Deprecation Timeline

- **v1.1**: Functions moved to `/legacy/` with deprecation warnings
- **v2.0**: Functions available with explicit warnings at import time
- **v3.0**: Functions will be removed entirely

##Function Migration Map

### Array Generation Functions

#### Old: `gen_3_3_array()` or `gen_2_2_array()`

```python
# OLD (deprecated)
from modules.sw_build_systems import BuildAmberSystems
builder = BuildAmberSystems(directories)
builder.gen_3_3_array(directories, molecule_name)

# NEW (recommended)
from modules.system_builder import BuildAmberSystems
builder = BuildAmberSystems(directories)
builder.gen_3_3_array(molecule_name)
```

#### Old: `build_3_3_polymer_array_old()`

This function had known issues with box dimensions and polymer conformation. Use the improved version instead:

```python
# OLD (deprecated)
builder.build_3_3_polymer_array_old(directories, mol_name, num_units)

# NEW (recommended)
builder.gen_3_3_array(mol_name)
```

### Utility Functions

#### Old: `max_pairwise_distance()`

```python
# OLD (deprecated)
from modules.sw_build_systems import BuildAmberSystems
max_dist = builder.max_pairwise_distance(mol)

# NEW (recommended)
from modules.system_builder import BuildSystems
builder = BuildSystems(directories)
max_dist = builder.max_pairwise_distance(mol)
```

#### Old: `parametrized_mols_avail()`

```python
# OLD (deprecated)
from modules.sw_directories import PolySimManage
manager = PolySimManage(...)
manager.parametrized_mols_avail()

# NEW (recommended)
from modules.filepath_manager import PolySimManage
manager = PolySimManage(...)
avail_mols = manager.mol2_avail()  # Returns list instead of just printing
```

### Analysis Functions

#### Old: `Analysis` class and related functions

```python
# OLD (deprecated)
from modules.sw_analysis import Analysis
analysis = Analysis()

# NEW (recommended)
from modules.trajectory_analyzer import Analysis
analysis = Analysis()
```

The new `Analysis` class from `trajectory_analyzer` is fully refactored with better documentation, type hints, and improved functionality. All methods work the same way but with cleaner code.

## Common Migration Patterns

### Pattern 1: Import Shim Compatibility

If you're updating existing code that uses old imports, you can gradually migrate:

```python
# This still works in v1.x but will be removed in v3.0
from modules.sw_build_systems import BuildAmberSystems

# Update to this for future compatibility
from modules.system_builder import BuildAmberSystems
```

### Pattern 2: Handling Deprecation Warnings

If you import deprecated functions, you'll see deprecation warnings. To suppress them during transition:

```python
import warnings

# Temporarily suppress warnings while migrating
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    from legacy.deprecated_functions import gen_3_3_array
```

## What Changed?

### Improvements in New Code

1. **Better Documentation**: Comprehensive docstrings with examples
2. **Type Hints**: Full type annotations for better IDE support
3. **Error Handling**: More specific error messages
4. **Naming**: Consistent snake_case function names (PEP 8)
5. **Performance**: Optimized implementations in some cases
6. **Maintainability**: Cleaner, more readable code

### Known Issues in Old Code

- **Array functions**: Known to generate boxes that are too large
- **Polymer conformation**: Some polymers generated with unrealistic geometry
- **Type hints**: No type annotations (harder to debug)
- **Documentation**: Minimal docstrings
- **Error handling**: Generic exception messages

## Getting Help

If you encounter issues migrating code:

1. Check the docstrings in the new modules:
   ```python
   from modules.system_builder import BuildAmberSystems
   help(BuildAmberSystems.gen_3_3_array)
   ```

2. Review the tutorials which use the new API

3. Check REFACTORING.md in the root directory for overall project changes

## Staying Current

To stay up to date with the project:

1. Update your imports when upgrading versions
2. Review the CHANGELOG.md for breaking changes
3. Run your code with `-W default` to see all deprecation warnings
4. Plan migration before v3.0 when deprecated code is removed

---

**Questions?** Check the main project README or open an issue on GitHub.
