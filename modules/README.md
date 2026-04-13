# Module Guide

This directory contains all core functionality modules for the SatisPHAction Simulator.

## Module Organization

### Core Modules (Descriptive Names)

#### 1. **molecule_builder.py** - Molecular Structure Utilities
- **Purpose**: Low-level molecular operations and structure manipulation
- **Key Functions**:
  - `smiles_to_pdb()` - Convert SMILES strings to 3D PDB structures
  - `vol_from_smiles()` - Calculate molecular volume from SMILES
  - `has_heteroatoms()` - Detect non-carbon atoms
  - `has_rings()` - Detect ring structures
- **Dependencies**: RDKit, Open Babel
- **Difficulty**: Beginner
- **Example**: See `/examples/02_smiles_to_structure.py`

#### 2. **filepath_manager.py** - File and Directory Management
- **Purpose**: Centralized file and directory management for simulation workflows
- **Key Classes**:
  - `PolySimManage` - Main directory manager (34 methods)
  - `PolyDataDirs` - Polymer-specific data management
  - `BioOilDirs` - Bio-oil specific directories
  - `DFTManager` - DFT quantum chemistry workflows
- **Key Features**:
  - Directory initialization and organization
  - CSV-based residue code database
  - File discovery and management
- **Difficulty**: Intermediate
- **Example**: See `Tutorial_1_filepath_manager.ipynb`

#### 3. **system_builder.py** - Prepare Systems for MD Simulations
- **Purpose**: Build complete molecular systems ready for simulations
- **Key Classes**:
  - `BuildSystems` - Basic system construction
  - `BuildAmberSystems` - AMBER forcefield-specific building
- **Key Operations**:
  - SMILES → 3D structure → AMBER parameters
  - Polymer chain building
  - System parameterization
  - Packmol integration
- **Dependencies**: RDKit, AmberTools, Packmol, ParmED
- **Difficulty**: Intermediate/Advanced
- **Example**: See `Tutorial_4_Building_Systems_with_Polymers.ipynb`

#### 4. **simulation_engine.py** - Run MD Simulations
- **Purpose**: Execute molecular dynamics simulations with OpenMM
- **Key Classes**:
  - `BuildSimulation` - Core simulation engine
  - `AmberSimulation` - AMBER forcefield simulations
  - `ANISimulation` - Machine learning forcefield (ANI)
- **Capabilities**:
  - Energy minimization
  - Multiple ensemble types (NVT, NPT, aNPT)
  - Simulated annealing
  - Stress-strain simulations
  - Reactive MD support
- **Dependencies**: OpenMM, ParmED, NumPy
- **Difficulty**: Advanced
- **Example**: See `Tutorial_5_Running_Openmm_Simulations.ipynb`

#### 5. **trajectory_analyzer.py** - Post-Process MD Results
- **Purpose**: Analyze molecular dynamics trajectories
- **Key Classes**:
  - `Analysis` - Core analysis methods (static class)
  - `Universe` - Base trajectory class
  - `poly_Universe` - Polymer-specific analysis
  - `bio_oil_Universe` - Bio-oil/mixture analysis
- **Analysis Capabilities**:
  - Radius of gyration (ROG)
  - End-to-end distance
  - Persistence length
  - Free volume calculations
  - Glass transition temperature (Tg)
  - Diffusion coefficients
- **Dependencies**: MDAnalysis, SciPy, Matplotlib, Seaborn
- **Difficulty**: Intermediate/Advanced
- **Examples**: See `Tutorial_10_Analysis_module.ipynb` and `Tutorial_11_Analysis_module_2.ipynb`

#### 6. **charge_calculator.py** - Multi-Method Charge Calculations
- **Purpose**: Calculate partial atomic charges using various methods
- **Key Classes**:
  - `ChargeCalculator` - Main charge computation class
- **Supported Methods**: GAFF, GAFF2, NAGL, MBIS, MULLIKEN
- **Dependencies**: RDKit, OpenFF, ParmED
- **Difficulty**: Advanced
- **Use Case**: Charge parameterization for non-standard molecules

#### 7. **quantum_calculator.py** - Quantum Chemistry Integration
- **Purpose**: Handle quantum chemistry calculations and outputs
- **Key Classes**:
  - `OrcaMolecule` - Data class for ORCA outputs
- **Key Functions**:
  - `csv_to_orca_molecules()` - Parse ORCA results
- **Dependencies**: ORCA (external tool)
- **Difficulty**: Advanced
- **Use Case**: Integration with ab initio quantum chemistry

#### 8. **input_generator.py** - Generate External Tool Input Files
- **Purpose**: Create input files for external simulation/QM software
- **Key Classes**:
  - `DFTInputGenerator` - ORCA DFT input file generation
- **Dependencies**: NumPy, Pandas
- **Difficulty**: Advanced
- **Use Case**: Quantum mechanical property calculations

#### 9. **decorators.py** - Utility Function Decorators
- **Purpose**: Reusable decorators for common operations
- **Key Classes**:
  - `CustomDecorators` - Collection of utility decorators
- **Common Uses**:
  - Function timing
  - Logging and error handling
  - Input validation
- **Difficulty**: Beginner
- **Use Case**: Code enhancement and debugging

#### 10. **complex_fluid_models.py** - Complex Mixture Modeling
- **Purpose**: Model complex fluid systems (bio-oil, polymers, mixtures)
- **Key Classes**:
  - `ComplexFluidModel` - Base model
  - `ComplexFluidModels` - Multiple model support
  - `ComplexFluidModelBuilder` - Model construction
- **Model Types**: 5 different complexity levels
- **Dependencies**: Packmol, AMBER
- **Difficulty**: Advanced
- **Use Case**: System modeling for complex fluids

#### 11. **config.py** - Configuration Management
- **Purpose**: Centralized configuration for paths and external tools
- **Key Functions**:
  - `get_packmol_path()` - Get packmol executable path
  - `get_config()` - Access full configuration
  - `set_config_value()` - Override configuration at runtime
- **Configuration via Environment Variables**:
  - `PACKMOL_PATH` - Packmol executable
  - `AMBER_HOME` - AmberTools installation
  - `ORCA_PATH` - ORCA quantum chemistry
  - `SATISFACTION_CONFIG` - Configuration file path
- **Difficulty**: Beginner
- **Purpose**: Makes code portable across different systems

### Backward Compatibility Shims

Files in `/compat/` directory provide backward compatibility with old module names:

- `sw_basic_functions.py` → imports from `molecule_builder.py`
- `sw_directories.py` → imports from `filepath_manager.py`
- `sw_build_systems.py` → imports from `system_builder.py`
- `sw_openmm.py` → imports from `simulation_engine.py`
- `sw_analysis.py` → imports from `trajectory_analyzer.py`
- (and others...)

**Note**: New code should use descriptive names. Old names will be deprecated in v2.0.

### Deprecated Code

Archived deprecated functions are in `/legacy/deprecated_functions.py`. See `legacy/MIGRATION_GUIDE.md` for migration paths.

## Getting Started

### Beginner Path (1-2 hours)
1. Read this file to understand module purposes
2. Run `/examples/01_hello_pdb.py` - Load and inspect PDB files
3. Run `/examples/02_smiles_to_structure.py` - Convert SMILES to structures
4. Follow `Tutorial_1_filepath_manager.ipynb` - Understand directory structure

### Intermediate Path (1 day)
1. Complete Beginner Path
2. Run `/examples/03_molecular_properties.py` - Analyze molecular features
3. Follow `Tutorial_2_Parameterizing_Small_Molecules_and_Polymers.ipynb`
4. Follow `Tutorial_3_Solvating_Small_Molecules_and_Polymers.ipynb`

### Advanced Path (Multiple days)
1. Complete Intermediate Path
2. Follow `Tutorial_4_Building_Systems_with_Polymers.ipynb`
3. Follow `Tutorial_5_Running_Openmm_Simulations.ipynb`
4. Follow `Tutorial_10_Analysis_module.ipynb` and `Tutorial_11_Analysis_module_2.ipynb`

## Using Modules in Your Code

### Import Examples

```python
# Modern approach (recommended)
from modules.molecule_builder import smiles_to_pdb
from modules.system_builder import BuildAmberSystems
from modules.simulation_engine import AmberSimulation
from modules.trajectory_analyzer import Analysis

# Backward compatible (still works, but deprecated)
from modules.sw_basic_functions import smiles_to_pdb  # Old name
from compat.sw_basic_functions import smiles_to_pdb   # Compat module
```

### Typical Workflow

```python
from modules.filepath_manager import PolySimManage
from modules.molecule_builder import smiles_to_pdb
from modules.system_builder import BuildAmberSystems
from modules.simulation_engine import AmberSimulation
from modules.trajectory_analyzer import Analysis
import os

# 1. Initialize directory manager
manager = PolySimManage(os.getcwd())

# 2. Create molecule from SMILES
smiles_to_pdb("CC(C)C", "isobutane.pdb")

# 3. Build system
builder = BuildAmberSystems(manager)
pdb_file = builder.smiles_to_pdb_gen_res_code("CC(C)C", "isobutane")

# 4. Run simulation
sim = AmberSimulation(manager, topology_file, coords_file)
sim.minimize_energy()
sim.basic_NVT(total_steps=100000, temp=298.15)

# 5. Analyze results
analysis = Analysis()
rog_values = analysis.calculate_roi(trajectory)
```

## Common Tasks

### Task 1: Convert SMILES to Structure
```python
from modules.molecule_builder import smiles_to_pdb

smiles_to_pdb("CC(C)CC1=CC=C(C=C1)C(C)C", "ibuprofen.pdb")
# Creates a 3D PDB file from SMILES notation
```

### Task 2: Calculate Molecular Properties
```python
from modules.molecule_builder import vol_from_smiles, has_heteroatoms

volume = vol_from_smiles("CC(C)C")
has_hetero = has_heteroatoms("c1ccccc1O")  # Check for OH group
```

### Task 3: Build and Run Simulation
```python
from modules.system_builder import BuildAmberSystems
from modules.simulation_engine import AmberSimulation

builder = BuildAmberSystems(manager)
builder.gen_3_3_array("my_polymer")  # Build 3x3x3 polymer array

sim = AmberSimulation(...)
sim.minimize_energy()
sim.basic_NVT(100000, 298.15)
```

### Task 4: Analyze Trajectory
```python
from modules.trajectory_analyzer import Analysis

analysis = Analysis()
rog = analysis.plot_ROG(universe, polymer_atoms)
```

## Configuration

See `modules/config.py` for setting up paths to external tools like Packmol, AMBER, and ORCA.

Set environment variables before running code:

```bash
export PACKMOL_PATH="/path/to/packmol"
export AMBER_HOME="/path/to/ambertools"
export NAGLMBIS_DIR="/path/to/naglmbis"
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'modules'"
- Ensure you're running from the project root directory
- Check that the Python path includes the project root

### "AttributeError: module has no attribute..."
- Check the module docstring for available functions: `help(module_name)`
- Ensure you're using the correct import statement
- See examples for correct usage patterns

### External Tool Issues
- Packmol not found: Set `PACKMOL_PATH` environment variable
- AmberTools not found: Set `AMBER_HOME` and add to PATH
- ORCA not found: Set `ORCA_PATH` environment variable

## API Reference

For detailed API documentation, consult:
1. Module docstrings: `python -c "from modules import molecule_builder; help(molecule_builder)"`
2. Function help: `python -c "from modules.molecule_builder import smiles_to_pdb; help(smiles_to_pdb)"`
3. Main ARCHITECTURE.md file
4. Tutorial Jupyter notebooks

## Contributing

If you develop new modules or improvements:
1. Follow PEP 8 naming conventions
2. Add comprehensive Google-style docstrings
3. Add type hints to public API functions
4. Create examples in `/examples/` if appropriate
5. See CONTRIBUTING.md for detailed guidelines

---

**Last Updated**: April 4, 2026
**Version**: 1.1
**Status**: Production Ready (Core modules), Beta (Advanced features)
