# Contributing to SatisPHAction Simulator

Thank you for considering contributing to the SatisPHAction Simulator! We welcome contributions from everyone, whether you're fixing bugs, adding features, improving documentation, or suggesting improvements.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please treat all members of the community with respect and professionalism.

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork locally
git clone https://github.com/YOUR_USERNAME/polymersimulator.git
cd polymersimulator
git remote add upstream https://github.com/MMLabCodes/polymersimulator.git
```

### 2. Set Up Development Environment

```bash
# Create a development environment
conda create --name satisfaction-dev python=3.11
conda activate satisfaction-dev

# Install dependencies
conda install -c conda-forge ambertools openmm rdkit openbabel
pip install -r requirements.txt

# For development (includes documentation tools)
pip install sphinx pytest black flake8
```

### 3. Create a Feature Branch

```bash
# Create a new branch for your work
git checkout -b feature/your-feature-name

# Or for bug fixes:
git checkout -b bugfix/your-bug-name
```

## Development Workflow

### Code Style

We follow **PEP 8** with the following standards enforced across the project:

- **Module names**: `snake_case` (e.g., `molecule_builder.py`)
- **Class names**: `CamelCase` (e.g., `BuildAmberSystems`)
- **Function names**: `snake_case` (e.g., `smiles_to_pdb()`)
- **Constants**: `UPPER_CASE` (e.g., `MAX_RETRIES`)
- **Private methods/functions**: Prefix with `_` (e.g., `_internal_helper()`)

### Documentation Standards

All public functions and classes must have docstrings in **Google style**:

```python
def smiles_to_pdb(smiles: str, output_file: str) -> str:
    """Convert SMILES string to 3D PDB structure.

    Args:
        smiles: SMILES string representation of molecule
        output_file: Path where PDB file will be written

    Returns:
        Path to the generated PDB file

    Raises:
        ValueError: If SMILES string is invalid
        IOError: If file cannot be written

    Example:
        >>> pdb_path = smiles_to_pdb("CC(C)C", "isobutane.pdb")
        >>> print(pdb_path)
        'isobutane.pdb'
    """
```

### Type Hints

Add type hints to all **public API functions**. Internal helper functions can omit type hints if they're simple.

```python
from typing import List, Optional, Tuple

def calculate_properties(
    molecules: List[str],
    method: str = "GAFF2",
    verbose: bool = False
) -> Tuple[List[float], List[dict]]:
    """Calculate molecular properties."""
    ...
```

### Imports

- Use explicit imports (no wildcard imports)
- Group imports: standard library, third-party, local modules
- One import per line for clarity

```python
import os
import sys
from typing import List, Optional

import numpy as np
import pandas as pd
from rdkit import Chem

from modules.filepath_manager import PolySimManage
from modules.molecule_builder import smiles_to_pdb
```

## Making Changes

### 1. Before You Start

- Check if an issue exists for your feature or bug
- Comment on the issue to let others know you're working on it
- Discuss major changes in an issue first

### 2. Make Your Changes

- Keep commits atomic and focused on a single feature/fix
- Write clear commit messages:
  ```
  Add feature: Implement quantum chemistry integration

  - Added OrcaMolecule dataclass for QM outputs
  - Implemented csv_to_orca_molecules() function
  - Added comprehensive docstrings and type hints

  Closes #42
  ```

### 3. Update Documentation

- Add/update docstrings for modified functions
- Update relevant `.md` files if behavior changes
- Update CHANGELOG.md with your changes under "Unreleased"

### 4. Test Your Changes

While we don't have automated tests yet, please:

- Run your code manually to ensure it works
- Test with different input scenarios
- Check for any import errors: `python -c "import modules.your_module"`
- Verify backward compatibility if modifying existing code

### 5. Keep Your Branch Updated

```bash
# Fetch latest changes from main repo
git fetch upstream

# Rebase your branch (preferred) or merge
git rebase upstream/main
# or
git merge upstream/main
```

## Module Organization

The project uses a modular structure with descriptive names:

```
/modules/
├── molecule_builder.py         # Molecular structure utilities
├── filepath_manager.py         # File/directory management
├── system_builder.py           # MD system construction
├── simulation_engine.py        # OpenMM simulations
├── trajectory_analyzer.py      # Trajectory analysis
├── charge_calculator.py        # Multi-method charge calculations
├── quantum_calculator.py       # Quantum chemistry integration
├── input_generator.py          # Input file generation
├── complex_fluid_models.py     # Complex mixture modeling
├── decorators.py              # Utility decorators
└── ...

/compat/
└── sw_*.py                     # Backward-compatible shims (do not modify!)

/legacy/
├── deprecated_functions.py     # Archived deprecated code
└── MIGRATION_GUIDE.md         # Migration instructions
```

### Adding New Modules

When adding a new module:

1. Create the file in `/modules/` with a descriptive name
2. Add comprehensive module-level docstring
3. Add entry to `modules/__init__.py`
4. Update `ARCHITECTURE.md` to document the new module
5. Add examples if the module is part of the public API

### Modifying Existing Modules

- Maintain backward compatibility with the `/compat/` shim layer
- Update docstrings and type hints
- Test with both old import paths (via compat) and new paths
- Document any breaking changes clearly

## Submitting Changes

### 1. Push Your Branch

```bash
git push origin feature/your-feature-name
```

### 2. Open a Pull Request

On GitHub:
1. Compare your branch against `main`
2. Write a clear title and description
3. Link related issues with `Closes #42`
4. Wait for review feedback

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Other

## Related Issues
Closes #42

## Changes Made
- Change 1
- Change 2

## Testing
How this was tested:
- [ ] Manual testing
- [ ] Updated existing tests
- [ ] Added new tests

## Checklist
- [ ] Code follows PEP 8 style guide
- [ ] Docstrings added (Google style)
- [ ] Type hints added (public APIs)
- [ ] Documentation updated
- [ ] No import errors
- [ ] Backward compatible (or documented as breaking)
- [ ] No hardcoded paths or credentials
```

## Review Process

1. Maintainers will review your PR within a few days
2. Feedback will be provided as comments
3. Address feedback by pushing additional commits
4. After approval, your PR will be merged

## Common Contributions

### Fixing a Bug

1. Create an issue describing the bug
2. Create a branch: `bugfix/description-of-bug`
3. Fix the bug and add a test case if possible
4. Submit PR with link to the issue

### Adding a Feature

1. Discuss in an issue first (especially large features)
2. Create a branch: `feature/description-of-feature`
3. Implement with full documentation
4. Add example usage if appropriate
5. Update CHANGELOG.md

### Improving Documentation

1. Create a branch: `docs/description-of-change`
2. Make documentation updates
3. Verify markdown renders correctly
4. Submit PR

### Adding Examples

1. Create files in `/examples/` directory
2. Include docstrings explaining what the example demonstrates
3. Ensure examples are runnable and include output comments
4. Update `/examples/README.md` with the new example

## Questions?

- **Documentation**: Check [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- **Setup Issues**: See [README.md](README.md) installation section
- **Module Help**: Check docstrings: `python -c "import modules.X; help(modules.X)"`
- **GitHub Issues**: Open an [issue](https://github.com/MMLabCodes/polymersimulator/issues)

## Recognition

All contributors are recognized in:
- Git commit history
- GitHub contributors page
- Project CHANGELOG.md (for significant contributions)

Thank you for contributing to SatisPHAction Simulator! 🧬

---

For detailed technical information, see:
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design overview
- [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) - Recent improvements
- [modules/](modules/) - Source code with comprehensive docstrings
