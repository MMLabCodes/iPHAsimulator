# iPHAsimulator - Examples

This directory contains runnable examples demonstrating the key capabilities of **iPHAsimulator**, a Python toolkit for simulating polyhydroxyalkanoate (PHA) systems using molecular dynamics.

## Quick Start Examples

All examples can be run from the command line:

```bash
python 01_hello_pdb.py
python 02_smiles_to_structure.py
python 03_molecular_properties.py
python 04_build_polymer_system.py
python 05_analyze_trajectory.py
```

## Example Overview

### 1. Hello PDB (01_hello_pdb.py)
**Difficulty**: Beginner
**Time**: 2 minutes
**Purpose**: Load and inspect a PDB file

Learn how to:
- Load molecular structures from PDB files
- Extract basic molecular information
- Display atom counts and residue information
- Calculate molecular weight

### 2. SMILES to Structure (02_smiles_to_structure.py)
**Difficulty**: Beginner
**Time**: 5 minutes
**Purpose**: Convert SMILES strings to 3D structures

Learn how to:
- Create molecules from SMILES notation
- Generate 3D coordinates
- Calculate molecular volume
- Analyze molecular properties (heteroatoms, rings)

### 3. Molecular Properties (03_molecular_properties.py)
**Difficulty**: Beginner
**Time**: 5 minutes
**Purpose**: Analyze molecular structure properties

Learn how to:
- Detect molecular features (heteroatoms, rings)
- Calculate molecular weights
- Count elemental composition
- Process multiple molecules

### 4. Build Polymer System (04_build_polymer_system.py)
**Difficulty**: Intermediate
**Time**: 10-15 minutes
**Purpose**: Build a polymer system with solvation

Learn how to:
- Create polymer structures from monomers
- Generate 3D molecular systems
- Solvate molecules in water
- Prepare for MD simulations

### 5. Analyze Trajectory (05_analyze_trajectory.py)
**Difficulty**: Intermediate
**Time**: 10 minutes
**Purpose**: Analyze MD simulation outputs

Learn how to:
- Load MD trajectories
- Calculate radius of gyration
- Track molecular properties over time
- Generate analysis plots

## Requirements

All examples require the iPHAsimulator environment:

```bash
# Create and activate environment
conda create --name iphAsimulator -c conda-forge
conda activate iphAsimulator
conda install -c conda-forge ambertools openmm rdkit openbabel
```

See main `README.md` for detailed setup instructions.

## What is a PHA?

Polyhydroxyalkanoates (PHAs) are biodegradable polymers synthesized by bacteria. They're important for:
- Sustainable materials
- Bio-based plastics
- Biomedical applications
- Waste reduction

This toolkit helps researchers simulate and understand PHA behavior at the molecular level.

## Common Tasks

### Task 1: Analyze an Existing Structure
```python
from modules.molecule_builder import smiles_to_pdb, calculate_molecular_weight

# Convert SMILES to PDB
smiles = "CC(C)CC1=CC=C(C=C1)C(C)C"  # Ibuprofen-like structure
smiles_to_pdb(smiles, "my_molecule.pdb")

# Analyze
weight, elements = calculate_molecular_weight("my_molecule.pdb")
print(f"Molecular weight: {weight:.2f} g/mol")
print(f"Composition: {elements}")
```

### Task 2: Build a System for Simulation
```python
from modules.system_builder import BuildAmberSystems
from modules.filepath_manager import PolySimManage

# Set up directories
dirs = PolySimManage("/path/to/project")

# Build system
builder = BuildAmberSystems(dirs)
builder.gen_3_3_array("my_polymer")
```

### Task 3: Run MD Simulation
```python
from modules.simulation_engine import BuildSimulation

# Create simulation
sim = BuildSimulation(...)
energy = sim.minimize(200)  # 200 steps minimization
sim.anneal_NVT(300, 400, 50000)  # Anneal from 300-400K
sim.run_npt(300, 10000)  # NPT at 300K
```

## Example Data

Examples use simple test structures. For real research:
- Use structures from PDB (protein database)
- Use literature-based parameters
- Validate against experimental data
- Document your workflow in a Jupyter notebook

## Jupyter Notebooks

For more comprehensive tutorials, see the root directory Jupyter notebooks:
- `Tutorial_1_filepath_manager.ipynb` - File management
- `Tutorial_2_Parameterizing_Small_Molecules_and_Polymers.ipynb` - Parameterization
- `Tutorial_3_Solvating_Small_Molecules_and_Polymers.ipynb` - Solvation
- `Tutorial_4_Building_Systems_with_Polymers.ipynb` - System building
- `Tutorial_5_Running_Openmm_Simulations.ipynb` - MD simulations
- `Tutorial_9_Stress_strain_simulations.ipynb` - Stress-strain simulations

## Questions?

1. Check the example code comments
2. Read module docstrings: `help(module_name.function_name)`
3. See main README.md for project documentation
4. Open an issue on GitHub

---

**Happy simulating!** 🧬
