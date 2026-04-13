"""
iPHAsimulator - Core Modules

This package contains all core functionality for iPHAsimulator — a toolkit
for building PHA (polyhydroxyalkanoate) polymer structures and setting up
DFT calculations or MD simulations.

MODULE OVERVIEW:
    molecule_builder      - Build 3D structures from SMILES; calculate molecular properties
    filepath_manager      - Organise project directories and locate simulation files
    system_builder        - Convert SMILES to PDB, parameterise with AMBER, build polymer arrays
    simulation_engine     - Run OpenMM MD simulations (minimise, NVT, NPT, thermal ramp)
    trajectory_analyzer   - Analyse MD trajectories (ROG, Tg, diffusion coefficients)
    charge_calculator     - Calculate atomic partial charges (GAFF, GAFF2, NAGL, MBIS)
    quantum_calculator    - Store and load ORCA DFT results
    input_generator       - Generate ORCA DFT input files
    decorators            - Internal utility decorators
    complex_fluid_models  - Model complex fluid mixtures for bio-oil simulations
    config                - Configure paths to external tools (Packmol, AMBER, ORCA)

QUICK START:
    # Step 1: Set up your project directory
    from modules.filepath_manager import PolySimManage
    manager = PolySimManage('/path/to/my_project')

    # Step 2: Build a PHA structure from a SMILES string
    from modules.system_builder import BuildAmberSystems
    builder = BuildAmberSystems(manager)
    builder.SmilesToPDB_GenResCode(smiles='CC(O)CC(=O)O', name='3HB')

    # Step 3: Parameterise with AMBER
    builder.parameterize_mol(name='3HB', charge=0)

    # Step 4: Run an MD simulation
    from modules.simulation_engine import AmberSimulation
    sim = AmberSimulation(manager, '3HB.prmtop', '3HB.inpcrd')
    sim.minimize_energy()
    sim.basic_NVT(total_steps=500_000, temp=298.15)

BACKWARD COMPATIBILITY:
    Old imports using 'sw_' names still work via the compat/ package:
        from compat.sw_basic_functions import vol_from_smiles   # old style
        from modules.molecule_builder import vol_from_smiles     # new style (preferred)

    See /legacy/MIGRATION_GUIDE.md for full migration instructions.

DOCUMENTATION:
    See README.md for installation and step-by-step usage guide.
    See ARCHITECTURE.md for system design overview.
    See /examples/ for runnable example scripts.
    See /tutorials/ for comprehensive worked examples.
"""
