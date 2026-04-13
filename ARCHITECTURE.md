# iPHAsimulator — System Architecture

## Overview

iPHAsimulator is a modular Python toolkit for building PHA (polyhydroxyalkanoate) polymer structures and setting up DFT calculations or MD simulations. The architecture is organized around three main functional areas:

```
┌─────────────────────┐
│   User Interface    │
│ (Examples, Scripts) │
└──────────┬──────────┘
           │
┌──────────▼───────────────────────────────┐
│       Public API Layer                   │
│  (Stable interfaces for users)           │
└──────────┬───────────────────────────────┘
           │
┌──────────▼───────────────────────────────────────────┐
│  Functional Modules                                 │
│                                                      │
│  ┌──────────────────┐  ┌─────────────────────────┐  │
│  │ Molecule Level   │  │  System Level           │  │
│  ├──────────────────┤  ├─────────────────────────┤  │
│  │ • molecule_      │  │ • filepath_manager      │  │
│  │   builder        │  │ • system_builder        │  │
│  │ • quantum_       │  │ • simulation_engine     │  │
│  │   calculator     │  │ • trajectory_analyzer   │  │
│  │ • charge_        │  │ • complex_fluid_models  │  │
│  │   calculator     │  │ • input_generator       │  │
│  └──────────────────┘  └─────────────────────────┘  │
└──────────┬───────────────────────────────────────────┘
           │
┌──────────▼────────────────────────┐
│  External Dependencies             │
│ (RDKit, OpenMM, AmberTools, MDAnalysis)
└────────────────────────────────────┘
```

## Module Organization

### Data Flow Layer (Molecule Building)

**`modules/molecule_builder.py`** - Molecular structure utilities
- **Purpose**: Low-level molecular operations
- **Key Classes**: None (functional module)
- **Key Functions**:
  - Volume calculations (vol_from_smiles, vol_from_pdb)
  - Molecular property analysis (has_heteroatoms, has_rings)
  - File I/O (pdb_to_mol, smiles_to_pdb)
- **Dependencies**: RDKit, Open Babel
- **Used By**: system_builder, other modules

**`modules/quantum_calculator.py`** - Quantum chemistry integration
- **Purpose**: Handle quantum chemistry calculations and outputs
- **Key Classes**: OrcaMolecule (dataclass)
- **Key Functions**: csv_to_orca_molecules()
- **Dependencies**: ORCA (external tool)
- **Used By**: Advanced workflows

**`modules/charge_calculator.py`** - Charge calculation
- **Purpose**: Multi-method charge computation
- **Key Classes**: ChargeCalculator
- **Supports**: GAFF, GAFF2, NAGL, MBIS, MULLIKEN
- **Dependencies**: RDKit, OpenFF
- **Used By**: system_builder for parameterization

### File/Directory Management Layer

**`modules/filepath_manager.py`** - Organize project structure
- **Purpose**: Centralized file and directory management
- **Key Classes**:
  - PolySimManage (main class, 34 methods)
  - PolyDataDirs
  - BioOilDirs
  - ComplexModelDirs
  - DFTManager
- **Dependencies**: OS, CSV, JSON
- **Used By**: All other modules
- **Note**: Acts as dependency injection for other classes

### System Building Layer

**`modules/system_builder.py`** - Prepare systems for MD
- **Purpose**: Build complete molecular systems
- **Key Classes**:
  - BuildSystems (basic system construction)
  - BuildAmberSystems (AMBER forcefield)
  - PrepPackmolForAmber (utility)
- **Key Operations**:
  - SMILES → 3D PDB
  - Residue code generation
  - Polymer building
  - Packmol integration
  - AMBER parameterization
- **Dependencies**: RDKit, AmberTools, Packmol
- **Used By**: User scripts, examples

### Simulation Layer

**`modules/simulation_engine.py`** - Run MD simulations
- **Purpose**: Execute molecular dynamics simulations
- **Key Classes**:
  - BuildSimulation (core engine)
  - AmberSimulation (AMBER forcefield)
  - ANISimulation (ANI forcefield)
  - DcdWriter, DataWriter (trajectory output)
  - AcrylateReact (reactive MD)
- **Key Operations**:
  - Energy minimization
  - NVT/NPT/aNPT ensembles
  - Simulated annealing
  - Thermal ramps
  - Stress-strain simulations
- **Dependencies**: OpenMM
- **Used By**: MD workflows

### Analysis Layer

**`modules/trajectory_analyzer.py`** - Post-process simulations
- **Purpose**: Analyze MD trajectories
- **Key Classes**:
  - Analysis (core analysis methods)
  - Universe, poly_Universe, bio_oil_Universe (specialized)
- **Key Operations**:
  - Radius of gyration (ROG)
  - End-to-end distance
  - Persistence length
  - Free volume
  - Glass transition temperature (Tg)
  - Diffusion coefficients
- **Dependencies**: MDAnalysis
- **Used By**: Analysis workflows

### Support Modules

**`modules/complex_fluid_models.py`** - Complex mixture modeling
- **Purpose**: Model complex fluid systems
- **Key Classes**:
  - ComplexFluidModel
  - ComplexFluidModels
  - ComplexFluidModelBuilder
- **Supports**: 5 model types
- **Dependencies**: Packmol, AMBER
- **Used By**: Bio-oil and mixture simulations

**`modules/input_generator.py`** - Generate input files
- **Purpose**: Create software input files
- **Key Classes**: DFTInputGenerator
- **Supports**: ORCA DFT calculations
- **Used By**: Quantum chemistry workflows

**`modules/decorators.py`** - Utility decorators
- **Purpose**: Reusable function decorators
- **Key Classes**: CustomDecorators
- **Used By**: Other modules as needed

## Data Flow Patterns

### Pattern 1: Molecule Creation Workflow
```
SMILES string
    ↓
smiles_to_pdb() [molecule_builder]
    ↓
PDB file (3D structure)
    ↓
has_heteroatoms(), has_rings() [molecule_builder]
    ↓
Molecular properties
```

### Pattern 2: System Building Workflow
```
PDB monomer files
    ↓
BuildSystems.generate_residue_codes() [system_builder]
    ↓
Residue code database (filepath_manager)
    ↓
BuildAmberSystems.gen_3_3_array() [system_builder]
    ↓
AMBER parameter files (.prmtop, .rst7)
    ↓
BuildSimulation [simulation_engine]
    ↓
Trajectory files (.nc, .dcd)
```

### Pattern 3: Analysis Workflow
```
Trajectory files
    ↓
Analysis() [trajectory_analyzer]
    ↓
calculate_roi(), calculate_tg() [trajectory_analyzer]
    ↓
Analysis results
    ↓
Plots and statistics
```

## Class Hierarchy

```
FileManagement:
  ├─ PolySimManage (main coordinator)
  │  └─ PolyDataDirs
  │  └─ BioOilDirs
  │  └─ DFTManager
  └─ ComplexModelDirs

SystemBuilding:
  ├─ BuildSystems (base)
  └─ BuildAmberSystems (extends)
     └─ PrepPackmolForAmber

Simulation:
  ├─ BuildSimulation (base)
  ├─ AmberSimulation (extends)
  ├─ ANISimulation (extends)
  ├─ GromacsSimulation
  ├─ TopologyML
  ├─ PositionsML
  └─ AcrylateReact

Analysis:
  ├─ Universe (base)
  ├─ poly_Universe (extends)
  ├─ bio_oil_Universe (extends)
  └─ Analysis
```

## Configuration & Naming

- **Module Names**: `snake_case` across the board
- **Class Names**: `CamelCase` for all classes
- **Function Names**: `snake_case` for all functions
- **Private Methods/Functions**: Prefix with `_`
- **Constants**: `UPPER_CASE`

## Backward Compatibility

Original `sw_*.py` modules are maintained as import shims:
- `sw_basic_functions.py` → imports from `molecule_builder.py`
- `sw_directories.py` → imports from `filepath_manager.py`
- (etc. for all 9 refactored modules)

This allows existing code to work unchanged while new code uses modern names.

## Entry Points for New Users

1. **Simple analysis**: Use `molecule_builder` directly
2. **Basic simulation**: Use `examples/` scripts
3. **Medium workflows**: Use `system_builder` + `simulation_engine`
4. **Advanced workflows**: Combine multiple modules with `filepath_manager`
5. **Analysis**: Use `trajectory_analyzer` with results

## Testing & Validation

No automated test suite exists yet. Manual validation includes:
1. All modules import without errors
2. Public APIs work as documented
3. Tutorials execute successfully
4. Examples run without errors

## Performance Considerations

- Molecule embedding: Uses RDKit (inherent limitations)
- System building: Limited by AmberTools/Packmol speed
- MD simulations: OpenMM performance depends on hardware
- Analysis: MDAnalysis efficiency depends on trajectory size

## Future Enhancements

- Unit test suite
- Performance testing/profiling
- Additional force field support
- GPU acceleration
- Distributed compute support
- Web interface/API

---

**Architecture Version**: 1.1 (refactored)
**Last Updated**: April 4, 2026
**Status**: Production ready for simulations
