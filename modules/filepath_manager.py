"""
iPHAsimulator - Project Directory and File Manager.

This module provides the PolySimManage class, which is the central organiser
for every iPHAsimulator workflow. All other modules receive a PolySimManage
instance so they know where to read and write files.

The manager creates and tracks a structured folder layout:

    <your_project_dir>/
    ├── pdb_files/
    │   ├── molecules/   <- 3D PDB structure files for individual molecules
    │   ├── systems/     <- assembled polymer systems for MD simulations
    │   └── residue_codes.csv  <- database of molecule codes
    └── python_scripts/      <- a convenient place for your own scripts

Additional Manager Classes:
    PolyDataDirs    - Extended manager with CSV data handling
    BioOilDirs      - Manager for bio-oil / complex mixture workflows
    ComplexModelDirs- Manager for complex fluid model data
    DFTManager      - Manager for DFT quantum chemistry job directories

Example::

    from modules.filepath_manager import PolySimManage

    # Initialise the project — creates all subdirectories automatically
    manager = PolySimManage('/path/to/my_pha_project')

    # Discover available structure files
    pdb_files = manager.pdb_files_avail()
    mol2_files = manager.mol2_files_avail()

    # Access key paths
    print(manager.pdb_file_dir)    # .../my_pha_project/pdb_files/
    print(manager.molecules_dir)   # .../my_pha_project/pdb_files/molecules/

Note:
    All other iPHAsimulator classes (BuildAmberSystems, AmberSimulation, etc.)
    should be initialised with a PolySimManage instance. This keeps all project
    files in one organised location.
"""

import os
import csv
import ast
import time
import re
import subprocess
import shutil
from typing import Optional, List, Tuple, Dict, Any
from pathlib import Path

# Try to import dependencies, but don't fail if missing
try:
    import pandas as pd
    import numpy as np
    import ipywidgets as widgets
    from IPython.display import display
except ImportError:
    pd = None
    np = None
    widgets = None
    display = None

try:
    from modules.input_generator import DFTInputGenerator
except ImportError:
    DFTInputGenerator = None

try:
    from modules.sw_basic_functions import get_homo_lumo_from_xyz
except ImportError:
    get_homo_lumo_from_xyz = None

__all__ = [
    'PolySimManage',
    'PolyDataDirs',
    'BioOilDirs',
    'ComplexModelDirs',
    'DFTManager',
]

# ============================================================================
# Constants
# ============================================================================

DEFAULT_MAX_DFT_JOBS: int = 8
DEFAULT_DFT_NPROCS: int = 10
DEPRECATED_DIR_NAME: str = 'depreceated'

# NOTE: Packmol path is now configured via modules.config
# See: modules/config.py for configuration details


# ============================================================================
# PolySimManage Class
# ============================================================================

class PolySimManage:
    """
    Core directory manager for polymer simulation workflows.

    Initializes and manages directory structures for polymer simulations,
    including organizing molecular files, system files, and supporting data.
    Creates and manages subdirectories such as pdb_files, molecules, systems,
    and python_scripts.

    Attributes:
        main_dir (str): Root directory for the simulation project.
        python_script_dir (str): Directory for Python scripts.
        pdb_file_dir (str): Directory for PDB files.
        csv_to_pdb_dir (str): Directory for CSV to PDB conversions.
        residue_code_csv (str): Path to residue codes CSV file.
        molecules_dir (str): Directory for individual molecule files.
        systems_dir (str): Directory for system files (for MD simulations).

    Note:
        Packmol path is configured via modules.config module.
        See: modules/config.py for configuration details.
    """

    def __init__(self, main_dir: str) -> None:
        """
        Initialize PolySimManage object.

        Creates necessary directory structure for polymer simulation setup,
        including subdirectories for PDB files, molecules, systems, and scripts.

        Args:
            main_dir: Root directory path for the simulation project.
                     Must be an existing directory.
                     Example: '/path/to/main/dir/'

        Raises:
            FileNotFoundError: If main_dir does not exist.

        Example:
            >>> dirs = PolySimManage('/home/user/my_simulation')
            >>> print(dirs.pdb_file_dir)
            '/home/user/my_simulation/pdb_files'
        """
        if not os.path.exists(main_dir):
            raise FileNotFoundError(f"The specified main directory '{main_dir}' does not exist.")

        self.main_dir: str = main_dir

        # Initialize python_scripts directory
        self.python_script_dir: str = os.path.join(main_dir, 'python_scripts')
        if not os.path.exists(self.python_script_dir):
            os.makedirs(self.python_script_dir)

        # Initialize pdb_files directory
        self.pdb_file_dir: str = os.path.join(main_dir, 'pdb_files')
        if not os.path.exists(self.pdb_file_dir):
            os.makedirs(self.pdb_file_dir)

        # Initialize csvs_to_pdb directory
        self.csv_to_pdb_dir: str = os.path.join(main_dir, 'csvs_to_pdb')
        if not os.path.exists(self.csv_to_pdb_dir):
            os.makedirs(self.csv_to_pdb_dir)

        # Initialize residue_codes.csv file
        self.residue_code_csv: str = os.path.join(self.pdb_file_dir, 'residue_codes.csv')
        if not os.path.exists(self.residue_code_csv):
            with open(self.residue_code_csv, 'w') as file:
                pass  # Create empty file

        # Initialize molecules directory
        self.molecules_dir: str = os.path.join(self.pdb_file_dir, 'molecules')
        if not os.path.exists(self.molecules_dir):
            os.makedirs(self.molecules_dir)

        # Initialize systems directory
        self.systems_dir: str = os.path.join(self.pdb_file_dir, 'systems')
        if not os.path.exists(self.systems_dir):
            os.makedirs(self.systems_dir)

    # ========================================================================
    # File Discovery Methods
    # ========================================================================

    def mol2_files_avail(self) -> List[str]:
        """
        Get list of all available MOL2 files in the project.

        Recursively searches through the pdb_file_dir for all MOL2 files,
        excluding deprecated directories.

        Returns:
            List of absolute paths to MOL2 files found.

        Example:
            >>> dirs = PolySimManage('/path/to/sim')
            >>> mol2_list = dirs.mol2_files_avail()
            >>> print(f"Found {len(mol2_list)} MOL2 files")
        """
        mol2_avail: List[str] = []
        for root, dirs, files in os.walk(self.pdb_file_dir):
            dirs[:] = [d for d in dirs if d != DEPRECATED_DIR_NAME]
            for file in files:
                if file.endswith(".mol2"):
                    mol2_filepath: str = os.path.join(root, file)
                    mol2_avail.append(mol2_filepath)
        return mol2_avail

    def load_mol2_filepath(self, molecule_name: Optional[str] = None) -> Optional[str]:
        """
        Retrieve the file path for a specific MOL2 molecule.

        Searches for a MOL2 file matching the given molecule name.

        Args:
            molecule_name: Name of the molecule (without extension).
                          Example: 'ethane' (searches for 'ethane.mol2')

        Returns:
            Absolute path to the MOL2 file if found, None otherwise.

        Example:
            >>> mol2_path = dirs.load_mol2_filepath('ethane')
            >>> if mol2_path:
            ...     print(f"Found MOL2: {mol2_path}")
        """
        if molecule_name is None:
            print("Please provide the name of the system you are retrieving files as follows: 'mol2_file = directories.load_mol2_filepath('ethane')")
            print("Change ethane for the name of the desired system")
            print("NOTE: The mol2 file of the requested molecule must be generated with tleap prior to use of this function")
            return None

        for root, dirs, files in os.walk(self.pdb_file_dir):
            dirs[:] = [d for d in dirs if d != DEPRECATED_DIR_NAME]
            for file in files:
                if file.endswith(".mol2"):
                    if (molecule_name + ".mol2") == file:
                        mol2_file_path: str = os.path.join(root, file)
                        return mol2_file_path

        return None

    def pdb_files_avail(self) -> List[str]:
        """
        Get list of all available PDB files in the project.

        Recursively searches through the pdb_file_dir for all PDB files,
        excluding deprecated directories.

        Returns:
            List of absolute paths to PDB files found.

        Example:
            >>> pdb_list = dirs.pdb_files_avail()
            >>> print(f"Found {len(pdb_list)} PDB files")
        """
        pdb_avail: List[str] = []
        for root, dirs, files in os.walk(self.pdb_file_dir):
            dirs[:] = [d for d in dirs if d != DEPRECATED_DIR_NAME]
            for file in files:
                if file.endswith(".pdb"):
                    pdb_filepath: str = os.path.join(root, file)
                    pdb_avail.append(pdb_filepath)
        return pdb_avail

    def load_pdb_filepath(self, molecule_name: Optional[str] = None) -> Optional[str]:
        """
        Retrieve the file path for a specific PDB molecule.

        Searches for a PDB file matching the given molecule name.

        Args:
            molecule_name: Name of the molecule (without extension).
                          Example: 'ethane' (searches for 'ethane.pdb')

        Returns:
            Absolute path to the PDB file if found, None otherwise.

        Example:
            >>> pdb_path = dirs.load_pdb_filepath('ethane')
            >>> if pdb_path:
            ...     print(f"Found PDB: {pdb_path}")
        """
        if molecule_name is None:
            print("Please provide the name of the system you are retrieving files as follows: 'pdb_file = directories.load_pdb_filepath('ethane')")
            print("Change ethane for the name of the desired system")
            print("NOTE: If requesting a system for molecular dynamics - PDB files of a system must be generated using tleap prior to this step")
            return None

        for root, dirs, files in os.walk(self.pdb_file_dir):
            dirs[:] = [d for d in dirs if d != DEPRECATED_DIR_NAME]
            for file in files:
                if file == (molecule_name + ".pdb"):
                    pdb_file_path: str = os.path.join(root, file)
                    return pdb_file_path

        return None

    def pckml_files_avail(self) -> List[str]:
        """
        Get list of all available PCKML (PACKMOL) input files.

        Recursively searches through the pdb_file_dir for all PCKML files,
        excluding deprecated directories.

        Returns:
            List of absolute paths to PCKML files found.

        Example:
            >>> pckml_list = dirs.pckml_files_avail()
        """
        pckml_avail: List[str] = []
        for root, dirs, files in os.walk(self.pdb_file_dir):
            dirs[:] = [d for d in dirs if d != DEPRECATED_DIR_NAME]
            for file in files:
                if file.endswith(".pckml"):
                    pckml_filepath: str = os.path.join(root, file)
                    pckml_avail.append(pckml_filepath)
        return pckml_avail

    def load_pckml_filepath(self, system_name: Optional[str] = None) -> Optional[str]:
        """
        Retrieve the file path for a specific PCKML (PACKMOL) input file.

        Args:
            system_name: Name of the system (without extension).

        Returns:
            Absolute path to the PCKML file if found, None otherwise.

        Example:
            >>> pckml_path = dirs.load_pckml_filepath('pb_ph_41')
        """
        if system_name is None:
            print("Please provide the name of the system you are retrieving files as follows: 'pckml_file = directories.load_pckml_filepath('pb_ph_41')")
            print("NOTE: Packmol input files must be written manually.")
            return None

        for root, dirs, files in os.walk(self.pdb_file_dir):
            dirs[:] = [d for d in dirs if d != DEPRECATED_DIR_NAME]
            for file in files:
                if file.endswith(".pckml"):
                    if (system_name + ".pckml") == file:
                        pckml_file_path: str = os.path.join(root, file)
                        return pckml_file_path

        return None

    def ac_files_avail(self) -> List[str]:
        """
        Get list of all available AC (ANTECHAMBER) files in the project.

        Returns:
            List of absolute paths to AC files found.
        """
        ac_avail: List[str] = []
        for root, dirs, files in os.walk(self.pdb_file_dir):
            dirs[:] = [d for d in dirs if d != DEPRECATED_DIR_NAME]
            for file in files:
                if file.endswith(".ac"):
                    ac_filepath: str = os.path.join(root, file)
                    ac_avail.append(ac_filepath)
        return ac_avail

    # ========================================================================
    # AMBER File Methods
    # ========================================================================

    def amber_systems_avail(self) -> Optional[List[str]]:
        """
        Get list of available AMBER system files (topology and coordinate files).

        Searches for AMBER PRMTOP and RST7 files in the systems directory.

        Returns:
            List of file paths if found, None otherwise.

        Note:
            Both .prmtop and .rst7 files are required to run a simulation.
        """
        has_amber: bool = False
        amber_system_avail: List[str] = []

        for root, dirs, files in os.walk(self.systems_dir):
            dirs[:] = [d for d in dirs if d != DEPRECATED_DIR_NAME]
            for file in files:
                if file.endswith(".prmtop"):
                    has_amber = True
                    prmtop_filepath: str = os.path.join(root, file)
                    amber_system_avail.append(prmtop_filepath)
                elif file.endswith(".rst7"):
                    has_amber = True
                    rst7_filepath: str = os.path.join(root, file)
                    amber_system_avail.append(rst7_filepath)

        if has_amber:
            print("")
            print("Remember you need both .prmtop and .rst7 files to run a simulation")
            return amber_system_avail
        else:
            print("No parametrized molecules.")
            return None

    def load_amber_filepaths(self, system_name: Optional[str] = None) -> Optional[Tuple[str, str]]:
        """
        Retrieve AMBER topology and coordinate file paths for a system.

        Args:
            system_name: Name of the system (without extension).

        Returns:
            Tuple of (topology_path, coordinate_path) if both found, None otherwise.

        Example:
            >>> top_file, crd_file = dirs.load_amber_filepaths('ethane')
        """
        prmtop_file_path: Optional[str] = None
        coord_file_path: Optional[str] = None

        if system_name is None:
            print("Please provide the name of the system you are retrieving files as follows: 'topology_file, coordinate_file = directories.retrieve_top_crds('ethane')")
            print("Change ethane for the name of the desired system")
            print("NOTE: Amber files must be generated using tleap prior to this step")
            return None

        for root, dirs, files in os.walk(self.systems_dir):
            dirs[:] = [d for d in dirs if d != DEPRECATED_DIR_NAME]
            for file in files:
                if file == (system_name + ".prmtop"):
                    prmtop_file_path = os.path.join(root, file)
                elif file == (system_name + ".rst7") or file == (system_name + ".inpcrd"):
                    coord_file_path = os.path.join(root, file)

        if (prmtop_file_path is not None) and (coord_file_path is not None):
            return (prmtop_file_path, coord_file_path)
        else:
            print("Files not found. Check name of molecule/system and if files have been generated.")
            return None

    # ========================================================================
    # GROMACS File Methods
    # ========================================================================

    def load_itp_filepath(self, system_name: Optional[str] = None) -> Optional[str]:
        """
        Retrieve GROMACS ITP topology file path for a system.

        Args:
            system_name: Name of the system (without extension).

        Returns:
            Absolute path to the ITP file if found, None otherwise.
        """
        itp_file_path: Optional[str] = None

        if system_name is None:
            print("Please provide a system name.")
            return None

        for root, dirs, files in os.walk(self.systems_dir):
            dirs[:] = [d for d in dirs if d != DEPRECATED_DIR_NAME]
            for file in files:
                if file == (system_name + ".itp"):
                    itp_file_path = os.path.join(root, file)

        if itp_file_path is not None:
            return itp_file_path
        else:
            print("Files not found. Check name of molecule/system and if files have been generated.")
            return None

    def load_gro_filepath(self, system_name: Optional[str] = None) -> Optional[str]:
        """
        Retrieve GROMACS GRO coordinate file path for a system.

        Args:
            system_name: Name of the system (without extension).

        Returns:
            Absolute path to the GRO file if found, None otherwise.
        """
        gro_file_path: Optional[str] = None

        if system_name is None:
            print("Please provide a system name.")
            return None

        for root, dirs, files in os.walk(self.systems_dir):
            dirs[:] = [d for d in dirs if d != DEPRECATED_DIR_NAME]
            for file in files:
                if file == (system_name + ".gro"):
                    gro_file_path = os.path.join(root, file)

        if gro_file_path is not None:
            return gro_file_path
        else:
            print("Files not found. Check name of molecule/system and if files have been generated.")
            return None

    def load_gromacs_filepaths(self, system_name: Optional[str] = None) -> Optional[Tuple[str, str]]:
        """
        Retrieve GROMACS topology and coordinate file paths for a system.

        Args:
            system_name: Name of the system (without extension).

        Returns:
            Tuple of (topology_path, coordinate_path) if both found, None otherwise.

        Example:
            >>> top_file, gro_file = dirs.load_gromacs_filepaths('ethane')
        """
        top_file_path: Optional[str] = None
        gro_file_path: Optional[str] = None

        if system_name is None:
            print("Please provide the name of the system you are retrieving files as follows: 'topology_file, coordinate_file = directories.retrieve_top_crds('ethane')")
            print("Change ethane for the name of the desired system")
            print("NOTE: Amber files must be generated using tleap prior to this step")
            return None

        for root, dirs, files in os.walk(self.systems_dir):
            dirs[:] = [d for d in dirs if d != DEPRECATED_DIR_NAME]
            for file in files:
                if file == (system_name + ".top"):
                    top_file_path = os.path.join(root, file)
                elif file == (system_name + ".gro"):
                    gro_file_path = os.path.join(root, file)

        if (top_file_path is not None) and (gro_file_path is not None):
            return (top_file_path, gro_file_path)
        else:
            print("Files not found. Check name of molecule/system and if files have been generated.")
            return None

    # ========================================================================
    # MD Analysis Methods
    # ========================================================================

    def retrieve_files_for_mdanalysis(self, system_name: Optional[str] = None) -> Optional[Tuple[Optional[str], List[str], List[str], List[str]]]:
        """
        Retrieve simulation files needed for molecular dynamics analysis.

        Collects AMBER topology files and trajectory files (DCD, PDB) organized
        by simulation phase (anneal, equilibration, production).

        Args:
            system_name: Name of the system to retrieve files for.

        Returns:
            Tuple of (topology_file, anneal_files, equilib_files, prod_files)
            or None if system_name is not provided.

        Example:
            >>> top, anneal, equil, prod = dirs.retrieve_files_for_mdanalysis('system1')
        """
        prmtop_file_path: Optional[str] = None

        if system_name is None:
            print("Please provide the name of the system you are retrieving files for.")
            return None

        for root, dirs, files in os.walk(self.systems_dir):
            dirs[:] = [d for d in dirs if d != DEPRECATED_DIR_NAME]
            for file in files:
                if file == (system_name + ".prmtop"):
                    prmtop_file_path = os.path.join(root, file)

        folders: List[str] = os.listdir(self.systems_dir)
        anneal_files: List[str] = []
        equili_files: List[str] = []
        prod_files: List[str] = []

        for folder in folders:
            if folder == system_name:
                print(folder)
                folder_path: str = os.path.join(self.systems_dir, folder)
                folder_contents: List[str] = os.listdir(folder_path)

                for item in folder_contents:
                    item_path: str = os.path.join(folder_path, item)
                    if os.path.isdir(item_path):
                        output_contents: List[str] = os.listdir(item_path)
                        for file in output_contents:
                            print(item_path)
                            if ".dcd" in file or ".pdb" in file:
                                if "anneal" in file:
                                    anneal_files.append(os.path.join(item_path, file))
                                if "atm" in file:
                                    equili_files.append(os.path.join(item_path, file))
                                if "prod" in file:
                                    prod_files.append(os.path.join(item_path, file))

        return (prmtop_file_path, anneal_files, equili_files, prod_files)

    def simulations_avail(self, system_name: str) -> Optional[List[str]]:
        """
        Get list of available simulations for a given system.

        Args:
            system_name: Name of the system to check.

        Returns:
            List of simulation directory paths if found, None otherwise.

        Example:
            >>> sims = dirs.simulations_avail('system1')
            >>> print(f"Found {len(sims)} simulations")
        """
        simulation_dir: str = os.path.join(self.systems_dir, system_name)
        avail_sims: List[str] = []

        for item in os.listdir(simulation_dir):
            item_path: str = os.path.join(simulation_dir, item)
            if os.path.isdir(item_path):
                avail_sims.append(item_path)

        if avail_sims == []:
            print("No simulations found for the system.")
            print("")
            print("Please ensure simulation files are available and system name is correct.")
            return None
        else:
            print("Output contains paths to simulation directories.")
            return avail_sims

    # ========================================================================
    # Utility Methods
    # ========================================================================

    def load_smiles(self, molecule_name: Optional[str] = None) -> Optional[str]:
        """
        Load SMILES string for a molecule from the residue codes CSV.

        Args:
            molecule_name: Name of the molecule to look up.

        Returns:
            SMILES string for the molecule if found, None otherwise.

        Raises:
            ValueError: If molecule name is not found in the CSV.
        """
        if molecule_name is None:
            print(f"Please provide a molecule name to this function")
            return None

        df: pd.DataFrame = pd.read_csv(
            self.residue_code_csv,
            sep=None,
            engine="python",
            header=None,
            names=["name", "smiles", "rescode"]
        )

        row: pd.DataFrame = df.loc[df["name"] == molecule_name]

        if not row.empty:
            return row.iloc[0]["smiles"]
        else:
            raise ValueError(f"Molecule name '{molecule_name}' not found in {self.residue_code_csv}")

    @staticmethod
    def unpack_csv(csv_with_mol_info: str) -> Tuple[List[str], List[str]]:
        """
        Unpack molecule names and SMILES from a CSV file.

        Args:
            csv_with_mol_info: Path to CSV file with molecule data.

        Returns:
            Tuple of (names_list, smiles_list).

        Example:
            >>> names, smiles = PolySimManage.unpack_csv('/path/to/data.csv')
        """
        names: List[str] = []
        smiles: List[str] = []

        with open(csv_with_mol_info, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if len(row) >= 2:
                    names.append(row[0])
                    smiles.append(row[1])

        return names, smiles

    def retrieve_polymeric_rescodes(self, molecule_name: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Retrieve residue codes for polymeric molecules (head, mainchain, tail).

        Args:
            molecule_name: Name of the polymeric molecule.

        Returns:
            Tuple of (head_code, mainchain_code, tail_code).
        """
        head_code: Optional[str] = None
        mainchain_code: Optional[str] = None
        tail_code: Optional[str] = None

        with open(self.residue_code_csv, 'r') as file:
            for line in file:
                parts: str = (line.strip().split('\t'))[0]
                split_parts: List[str] = parts.split(",")

                if len(split_parts) >= 3:
                    if split_parts[0] == ("head_" + molecule_name):
                        head_code = split_parts[2]
                    elif split_parts[0] == ("mainchain_" + molecule_name):
                        mainchain_code = split_parts[2]
                    elif split_parts[0] == ("tail_" + molecule_name):
                        tail_code = split_parts[2]

        return (head_code, mainchain_code, tail_code)

    def retrieve_rescode(self, molecule_name: str) -> Optional[str]:
        """
        Retrieve residue code for a molecule.

        Args:
            molecule_name: Name of the molecule.

        Returns:
            Residue code if found, None otherwise.
        """
        rescode: Optional[str] = None

        with open(self.residue_code_csv, 'r') as file:
            for line in file:
                parts: str = (line.strip().split('\t'))[0]
                split_parts: List[str] = parts.split(",")

                if len(split_parts) >= 3 and split_parts[0] == molecule_name:
                    rescode = split_parts[2]

        return rescode


# ============================================================================
# PolyDataDirs Class
# ============================================================================

class PolyDataDirs(PolySimManage):
    """
    Extended directory manager for polymer data with CSV storage.

    Extends PolySimManage to add functionality for managing polymer data
    stored in CSV files, including identifiers and parameters.

    Attributes:
        poly_data (str): Path to polymer data CSV file.
        data (pd.DataFrame): Loaded polymer data.
        available_identifiers (List[str]): List of available system identifiers.
    """

    def __init__(self, main_dir: str, *args: Any, **kwargs: Any) -> None:
        """
        Initialize PolyDataDirs object.

        Args:
            main_dir: Root directory for the simulation project.
            *args: Additional positional arguments for parent class.
            **kwargs: Additional keyword arguments for parent class.

        Raises:
            FileNotFoundError: If main_dir does not exist.
        """
        super().__init__(main_dir, *args, **kwargs)

        if not os.path.exists(main_dir):
            raise FileNotFoundError

        self.poly_data: str = os.path.join(self.systems_dir, "poly_data.csv")
        if not os.path.exists(self.poly_data):
            with open(self.poly_data, 'w') as file:
                file.write("Name\n")  # Create first column for pandas

        self.data: pd.DataFrame = pd.read_csv(self.poly_data)
        self.available_identifiers: List[str] = self.load_available_identifiers()

    @staticmethod
    def parse_list(value: Any) -> Any:
        """
        Convert string representation of a list to Python list of floats.

        Used for returning parameters from CSV files where lists are stored
        as strings.

        Args:
            value: Value to parse.

        Returns:
            Parsed list of floats if value is a string list representation,
            otherwise returns value unchanged.
        """
        if isinstance(value, str):
            cleaned: str = re.sub(r"[\[\]]", "", value).strip()
            return [float(x) for x in cleaned.split()]
        return value

    def load_available_identifiers(self) -> List[str]:
        """
        Load stored available identifiers from CSV or set defaults.

        Returns:
            List of available identifiers.
        """
        if "Available Identifiers" in self.data.columns:
            try:
                return ast.literal_eval(self.data["Available Identifiers"].dropna().iloc[0])
            except (ValueError, IndexError, SyntaxError):
                pass

        return []

    def save_available_identifiers(self) -> None:
        """
        Save updated available identifiers list to CSV.
        """
        if "Available Identifiers" not in self.data.columns:
            self.data["Available Identifiers"] = ""

        self.data.loc[0, "Available Identifiers"] = str(self.available_identifiers)
        self.data.to_csv(self.poly_data, index=False)

    def assign_identifiers(self, system_name: str) -> None:
        """
        Launch interactive widget to assign identifiers to a system.

        Creates a Jupyter widget interface for multi-select identifier assignment
        with custom identifier input capability.

        Args:
            system_name: Name of the system to assign identifiers to.

        Note:
            This method only works in Jupyter notebook environments.
        """
        df: pd.DataFrame = pd.read_csv(self.poly_data)

        if system_name not in df["Name"].values:
            print(f"System '{system_name}' not found in CSV.")
            return

        multi_select = widgets.SelectMultiple(
            options=self.available_identifiers,
            description="Identifiers:",
            disabled=False
        )

        custom_text = widgets.Text(
            placeholder="Enter custom identifiers (comma-separated)...",
            description="Custom:"
        )

        clear_checkbox = widgets.Checkbox(
            value=False,
            description="Clear all identifiers",
            indent=False
        )

        def on_button_click(b: Any) -> None:
            """Save selected identifiers to DataFrame and update available list."""
            if clear_checkbox.value:
                df.loc[df["Name"] == system_name, "Identifiers"] = "[]"
                print(f"Cleared all identifiers for '{system_name}'.")
            else:
                # Retrieve existing identifiers
                existing_identifiers: Any = df.loc[df["Name"] == system_name, "Identifiers"].values
                if existing_identifiers and isinstance(existing_identifiers[0], str):
                    try:
                        existing_identifiers = ast.literal_eval(existing_identifiers[0])
                        if not isinstance(existing_identifiers, list):
                            existing_identifiers = []
                    except (ValueError, SyntaxError):
                        existing_identifiers = []
                else:
                    existing_identifiers = []

                # Get new selections
                selected_identifiers: List[str] = list(multi_select.value)
                if custom_text.value:
                    new_custom_identifiers: List[str] = [
                        id.strip() for id in custom_text.value.split(",") if id.strip()
                    ]
                    selected_identifiers.extend(new_custom_identifiers)

                    # Add new custom identifiers to dropdown list
                    for identifier in new_custom_identifiers:
                        if identifier not in self.available_identifiers:
                            self.available_identifiers.append(identifier)

                # Remove duplicates and update CSV
                updated_identifiers: List[str] = list(set(existing_identifiers + selected_identifiers))
                df.loc[df["Name"] == system_name, "Identifiers"] = str(updated_identifiers)

                print(f"Updated '{system_name}' with identifiers: {updated_identifiers}")

            # Save changes
            df.to_csv(self.poly_data, index=False)
            self.data = pd.read_csv(self.poly_data)
            self.save_available_identifiers()

        button = widgets.Button(description="Apply Identifiers")
        button.on_click(on_button_click)

        display(multi_select, custom_text, clear_checkbox, button)

    def get_poly_param(
        self,
        name: str,
        column: str,
        index: Optional[int] = None,
        condition: Optional[callable] = None
    ) -> Any:
        """
        Retrieve a parameter from the polymer CSV for a given molecule.

        Args:
            name: Molecule name to look up.
            column: Column name to retrieve data from.
            index: If provided, return the i-th item from a list value.
            condition: Optional function to apply to the result.

        Returns:
            The retrieved value (full list, element, or condition output), or None.

        Example:
            >>> value = dirs.get_poly_param('ethane', 'density')
            >>> first_val = dirs.get_poly_param('ethane', 'energies', index=0)
        """
        try:
            df: pd.DataFrame = pd.read_csv(self.poly_data)

            if "Name" not in df.columns or column not in df.columns:
                print("Requested column or 'Name' column does not exist.")
                return None

            value: Any = df.loc[df["Name"] == name, column]

            if value.empty:
                print("No entry found for this molecule.")
                return None

            value = value.iloc[0]

            try:
                value = ast.literal_eval(value)
            except (ValueError, SyntaxError):
                pass  # Leave as-is

            if index is not None and isinstance(value, list):
                return value[index] if index < len(value) else None

            if condition is not None and callable(condition):
                return condition(value)

            return value

        except Exception as e:
            print(f"Error reading CSV: {e}")
            return None

    def update_poly_csv(
        self,
        name: str,
        column: str,
        value: Any,
        overwrite: bool = False
    ) -> None:
        """
        Update polymer data CSV with new values.

        Args:
            name: Molecule name.
            column: Column name to update.
            value: Value to add/update.
            overwrite: If True, replace existing value; if False, append to list.

        Example:
            >>> dirs.update_poly_csv('ethane', 'density', 0.789)
            >>> dirs.update_poly_csv('ethane', 'energies', 100.5, overwrite=True)
        """
        file_path: str = self.poly_data

        # Load or initialize DataFrame
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            df = pd.read_csv(file_path)
        else:
            df = pd.DataFrame(columns=["Name"])

        # Ensure 'Name' column exists
        if "Name" not in df.columns:
            df["Name"] = ""

        # Add new row if needed
        if name not in df["Name"].values:
            new_row = pd.DataFrame({"Name": [name]})
            df = pd.concat([df, new_row], ignore_index=True)

        # Ensure the column exists
        if column not in df.columns:
            df[column] = ""

        # Get current value (if any)
        current_value: Any = df.loc[df["Name"] == name, column].values[0]

        # Convert from string to list if needed
        if not overwrite and pd.notna(current_value) and current_value != "":
            try:
                current_list: List[Any] = eval(current_value)
                if not isinstance(current_list, list):
                    current_list = [current_list]
            except:
                current_list = [current_value]
        else:
            current_list = []

        # Append or overwrite
        if overwrite:
            new_value: List[Any] = [value] if not isinstance(value, list) else value
        else:
            if isinstance(value, list):
                new_value = current_list + value
            else:
                new_value = current_list + [value]

        # Store as string
        df.loc[df["Name"] == name, column] = str(new_value)

        # Save and update internal data
        df.to_csv(file_path, index=False)
        print(f"Updated {file_path} successfully!")

        self.data = pd.read_csv(self.poly_data)


# ============================================================================
# BioOilDirs Class
# ============================================================================

class BioOilDirs(PolySimManage):
    """
    Extended directory manager for bio-oil modeling projects.

    Extends PolySimManage to add directories and methods specific to
    bio-oil research, including GC data and model-specific subdirectories.

    Attributes:
        bio_oil_dir (str): Root directory for bio-oil data.
        bio_oil_GC_data (str): Directory for gas chromatography data.
        bio_oil_models_dir (str): Directory for model data.
    """

    def __init__(self, main_dir: str, *args: Any, **kwargs: Any) -> None:
        """
        Initialize BioOilDirs object.

        Args:
            main_dir: Root directory for the simulation project.
            *args: Additional positional arguments for parent class.
            **kwargs: Additional keyword arguments for parent class.

        Raises:
            FileNotFoundError: If main_dir does not exist.
        """
        super().__init__(main_dir, *args, **kwargs)

        if not os.path.exists(main_dir):
            raise FileNotFoundError

        self.bio_oil_dir: str = os.path.join(main_dir, 'bio_oil')
        if not os.path.exists(self.bio_oil_dir):
            os.makedirs(self.bio_oil_dir)

        self.bio_oil_GC_data: str = os.path.join(self.bio_oil_dir, 'GC_data')
        if not os.path.exists(self.bio_oil_GC_data):
            os.makedirs(self.bio_oil_GC_data)

        self.bio_oil_models_dir: str = os.path.join(self.bio_oil_dir, 'models')
        if not os.path.exists(self.bio_oil_models_dir):
            os.makedirs(self.bio_oil_models_dir)

    def gc_data_avail(self) -> None:
        """
        List and validate available GC data CSV files.

        Walks through GC data directory and prints status of each CSV file,
        indicating whether data is complete or incomplete.
        """
        for root, dirs, files in os.walk(self.bio_oil_GC_data):
            # Exclude deprecated directories
            dirs[:] = [d for d in dirs if d != DEPRECATED_DIR_NAME]

            for file in files:
                if file.endswith(".csv"):
                    csv_file_path: str = os.path.join(root, file)
                    csv_file: str = os.path.basename(csv_file_path)

                    try:
                        df: pd.DataFrame = pd.read_csv(csv_file_path)
                        # Drop unnamed columns
                        df = df.loc[:, ~df.columns.str.startswith('Unnamed')]

                        # Check for null values
                        if df.isnull().any().any():
                            print(f"{csv_file} - Incomplete")
                        else:
                            print(csv_file)
                    except Exception as e:
                        print(f"Error reading {csv_file}: {e}")


# ============================================================================
# ComplexModelDirs Class
# ============================================================================

class ComplexModelDirs(BioOilDirs):
    """
    Directory manager for complex fluid modeling.

    Extends BioOilDirs to add directories and methods for complex fluid
    simulations, including DFT calculations, PACKMOL setup, and AMBER files.

    Attributes:
        complex_model_dir (str): Root directory for the specific complex model.
        dft_input_dir (str): Directory for DFT input files.
        packmol_dir (str): Directory for PACKMOL-related files.
        packmol_inputs (str): Directory for PACKMOL input scripts.
        packmol_systems (str): Directory for PACKMOL-generated PDB files.
        output_files (str): Directory for output files.
        amber (str): Directory for AMBER files.
    """

    def __init__(self, main_dir: str, model_name: str, *args: Any, **kwargs: Any) -> None:
        """
        Initialize ComplexModelDirs object.

        Args:
            main_dir: Root directory for the simulation project.
            model_name: Name of the complex fluid model.
            *args: Additional positional arguments for parent class.
            **kwargs: Additional keyword arguments for parent class.
        """
        super().__init__(main_dir, *args, **kwargs)

        self.complex_model_dir: str = os.path.join(self.bio_oil_models_dir, model_name)
        if not os.path.exists(self.complex_model_dir):
            os.makedirs(self.complex_model_dir)

        self.dft_input_dir: str = os.path.join(self.complex_model_dir, "DFT_inputs")
        if not os.path.exists(self.dft_input_dir):
            os.makedirs(self.dft_input_dir)

        self.packmol_dir: str = os.path.join(self.complex_model_dir, "packmol")
        if not os.path.exists(self.packmol_dir):
            os.makedirs(self.packmol_dir)

        self.packmol_inputs: str = os.path.join(self.packmol_dir, "packmol_inputs")
        if not os.path.exists(self.packmol_inputs):
            os.makedirs(self.packmol_inputs)

        self.packmol_systems: str = os.path.join(self.packmol_dir, "packmol_pdbs")
        if not os.path.exists(self.packmol_systems):
            os.makedirs(self.packmol_systems)

        self.output_files: str = os.path.join(self.complex_model_dir, "output_files")
        if not os.path.exists(self.output_files):
            os.makedirs(self.output_files)

        self.amber: str = os.path.join(self.complex_model_dir, "amber")
        if not os.path.exists(self.amber):
            os.makedirs(self.amber)

    def packmol_systems_avail(self) -> List[str]:
        """
        Get list of all available PACKMOL-generated PDB systems.

        Returns:
            List of absolute paths to PDB files generated by PACKMOL.
        """
        avail_files: List[str] = []

        for root, dirs, files in os.walk(self.packmol_systems):
            dirs[:] = [d for d in dirs if d != DEPRECATED_DIR_NAME]
            for file in files:
                if file.endswith(".pdb"):
                    pdb_file_path: str = os.path.join(root, file)
                    avail_files.append(pdb_file_path)

        return avail_files


# ============================================================================
# DFTManager Class
# ============================================================================

class DFTManager(PolySimManage):
    """
    Manager for DFT quantum chemistry calculation workflows.

    Extends PolySimManage to add functionality for managing DFT calculations
    using ORCA, including job submission, tracking, and result processing.

    Attributes:
        max_jobs (int): Maximum number of simultaneous jobs.
        nprocs (int): Number of processors per job.
        dft_manager_dir (str): Directory for DFT management files.
        submitted_jobs_file (str): Path to submitted jobs tracking file.
        processed_jobs_file (str): Path to processed jobs tracking file.
        queue_file (str): Path to job queue file.
        job_paths_file (str): Path to job paths tracking file.
        error_jobs_file (str): Path to error jobs tracking file.
    """

    max_jobs: int = DEFAULT_MAX_DFT_JOBS
    nprocs: int = DEFAULT_DFT_NPROCS
    runorca_path: str = "/scratch/scw1976/dan/iPHAsimulator-main/bin/runorca.sh"
    fukui_path: str = "/scratch/scw1976/dan/iPHAsimulator-main/bin/fukui.sh"
    running_path: str = "/scratch/s.983045"
    orbital_editor: str = "/scratch/s.983045/bio_oil_modelling/scripts/orbital_cube_editor.py"
    orca_resubmission_handler: str = "/scratch/s.983045/bio_oil_modelling/scripts/job_resubmitter.py"
    orca_data_collater: str = "/scratch/s.983045/bio_oil_modelling/scripts/orca_data_collater.py"

    def __init__(self, main_dir: str, *args: Any, **kwargs: Any) -> None:
        """
        Initialize DFTManager object.

        Creates directory structure and job tracking files for DFT workflows.

        Args:
            main_dir: Root directory for the simulation project.
            *args: Additional positional arguments for parent class.
            **kwargs: Additional keyword arguments for parent class.

        Raises:
            FileNotFoundError: If main_dir does not exist.
        """
        super().__init__(main_dir, *args, **kwargs)

        if not os.path.exists(main_dir):
            raise FileNotFoundError(f"Main directory {main_dir} does not exist.")

        self.dft_manager_dir: str = os.path.join(main_dir, "dft_manage_dir")
        os.makedirs(self.dft_manager_dir, exist_ok=True)

        self.submitted_jobs_file: str = self._create_empty_file("submitted_jobs.txt")
        self.processed_jobs_file: str = self._create_empty_file("processed_jobs.txt")
        self.queue_file: str = self._create_empty_file("job_queue.txt")
        self.job_paths_file: str = self._create_empty_file("job_paths.txt")
        self.error_jobs_file: str = self._create_empty_file("job_errors.txt")

    def _create_empty_file(self, filename: str) -> str:
        """
        Create an empty file if it doesn't exist.

        Args:
            filename: Name of the file to create.

        Returns:
            Absolute path to the created file.
        """
        filepath: str = os.path.join(self.dft_manager_dir, filename)
        if not os.path.exists(filepath):
            open(filepath, "w").close()
        return filepath

    def job_queuer(self, input_directory: str, output_directory: str) -> None:
        """
        Add jobs from input directory to the job queue.

        Args:
            input_directory: Directory containing input files.
            output_directory: Directory for output files.
        """
        jobs_to_queue: List[str] = []

        for file in os.listdir(input_directory):
            if os.path.isfile(os.path.join(input_directory, file)):
                filename: str = os.path.splitext(file)[0]
                job_entry: str = f"{input_directory} {filename} {output_directory}"
                if job_entry not in jobs_to_queue:
                    jobs_to_queue.append(job_entry)

        with open(self.queue_file, "a") as file:
            for job in jobs_to_queue:
                file.write(job + "\n")

    def check_and_submit_jobs(self) -> None:
        """
        Main job submission loop.

        Continuously checks running jobs and submits new jobs from queue,
        respecting the max_jobs limit. Periodically checks job status.

        Note:
            This is a blocking operation that should be run in background.
        """
        while True:
            running_jobs: int = self.get_running_jobs_count()

            if running_jobs < self.max_jobs:
                job_queue: List[str] = self.read_job_queue()
                if job_queue:
                    job: str = job_queue.pop(0)
                    inp_dir, xyz, inp, out_dir = self.inputs_from_queue(job)
                    job_number: Optional[str] = self.submit_job(inp_dir, inp, xyz, self.nprocs)

                    if job_number:  # Ensure job was submitted successfully
                        job_name: str = xyz.split(".")[0]
                        self.move_to_submitted_jobs(inp_dir, out_dir, job_name, job_number)
                        self.write_job_queue(job_queue)

                if len(job_queue) == 0:
                    self.check_submitted_jobs()
                    time.sleep(60)

            else:
                self.check_submitted_jobs()
                print("Job queue full. Processing...")
                time.sleep(60)

    def get_running_jobs_count(self) -> int:
        """
        Get number of currently running DFT jobs.

        Returns:
            Number of running jobs.
        """
        try:
            result = subprocess.run(
                ["squeue", "-u", "s.983045", "-h", "-t", "RUNNING,PENDING", "-p", "s_compute_chem"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            output: str = result.stdout.decode("utf-8").strip()
            return len(output.splitlines())
        except Exception as e:
            print(f"Error fetching running jobs: {e}")
            return 0

    def read_job_queue(self) -> List[str]:
        """
        Read job queue from file.

        Returns:
            List of job entries from queue file.
        """
        with open(self.queue_file, "r") as file:
            return file.readlines()

    def write_job_queue(self, job_queue: List[str]) -> None:
        """
        Write job queue to file.

        Args:
            job_queue: List of job entries to write.
        """
        with open(self.queue_file, "w") as file:
            file.writelines(job_queue)

    def inputs_from_queue(self, job_from_queue: str) -> Tuple[str, str, str, str]:
        """
        Parse job entry from queue.

        Args:
            job_from_queue: Job entry string from queue.

        Returns:
            Tuple of (input_dir, xyz_name, inp_name, output_dir).
        """
        input_dir, job_name, output_dir = job_from_queue.split(" ")
        xyz_name: str = f"{job_name}.xyz"
        inp_name: str = f"{job_name}.inp"
        return input_dir, xyz_name, inp_name, output_dir

    def submit_job(
        self,
        input_dir: str,
        inp_path: str,
        xyz_path: str,
        nprocs: Optional[int] = None
    ) -> Optional[str]:
        """
        Submit a DFT job to the queue.

        Args:
            input_dir: Directory containing input files.
            inp_path: Name of ORCA input file.
            xyz_path: Name of XYZ coordinate file.
            nprocs: Number of processors (defaults to self.nprocs).

        Returns:
            Job number if submitted successfully, None otherwise.
        """
        nprocs = nprocs or self.nprocs

        try:
            os.chdir(input_dir)
            process = subprocess.Popen(
                ["bash", self.runorca_path, inp_path, xyz_path, str(nprocs)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = process.communicate()
            stdout_str: str = stdout.decode("utf-8").strip()
            stderr_str: str = stderr.decode("utf-8").strip()

            if stderr_str:
                raise RuntimeError(f"Error during job submission: {stderr_str}")

            match = re.search(r"Submitted batch job (\d+)", stdout_str)
            if match:
                return match.group(1)
            else:
                raise ValueError("No job number found in the submission output.")

        except Exception as e:
            print(f"Failed to submit job: {e}")
            return None
        finally:
            os.chdir(self.main_dir)

    def move_to_submitted_jobs(
        self,
        inp_dir: str,
        out_dir: str,
        job_name: str,
        job_number: str
    ) -> None:
        """
        Log submitted job and its paths.

        Args:
            inp_dir: Input directory path.
            out_dir: Output directory path.
            job_name: Name of the job.
            job_number: Job ID assigned by scheduler.
        """
        timestamp: str = time.strftime("%Y-%m-%d %H:%M:%S")

        with open(self.submitted_jobs_file, "a") as file:
            file.write(f"{timestamp} Job number: {job_number} Job name: {job_name}\n")

        with open(self.job_paths_file, "a") as file:
            job_path: str = os.path.join(inp_dir, job_number)
            job_entry: str = f"{job_path} {out_dir}".strip()
            if job_entry:
                file.write(job_entry + "\n")

    def check_submitted_jobs(self) -> None:
        """
        Check status of submitted jobs and process results.

        Classifies jobs into finished, running, or errored based on .out file
        content. Updates tracking files accordingly.
        """
        with open(self.job_paths_file, "r") as file:
            lines: List[str] = file.readlines()

        finished_jobs: List[str] = []
        running_jobs: List[str] = []
        error_jobs: List[str] = []

        for line in lines:
            line = line.strip()
            if not line:  # Skip blank lines
                continue

            try:
                # Parse job and output directories
                job_path, out_path = line.split(" ", 1)
                print(f"Job path is: {job_path}")
                print(f"Out path is: {out_path}")

                # Check if job directory exists
                if not os.path.isdir(job_path):
                    print(f"Job path not found, assuming still running: {job_path}")
                    running_jobs.append(line)
                    continue

                # Look for .out files in the job directory
                out_files: List[str] = [file for file in os.listdir(job_path) if file.endswith(".out")]
                if not out_files:
                    print(f"No `.out` files found in {job_path}, assuming still running.")
                    running_jobs.append(line)
                    continue

                # Process .out files
                for out_file in out_files:
                    out_file_path: str = os.path.join(job_path, out_file)
                    print(f"Output filepath {out_file_path}")

                    try:
                        with open(out_file_path, "r") as f:
                            content: str = f.read()

                            # Check if job terminated normally
                            if "ORCA TERMINATED NORMALLY" in content:
                                molecule_name: str = out_file.replace(".out", "")
                                print(f"Processing result for {molecule_name} in {job_path}")
                                self.process_result(molecule_name, job_path, out_path)
                                finished_jobs.append(line)
                            else:
                                print(f"Job error detected in {out_file_path}")
                                error_jobs.append(line)

                    except Exception as e:
                        print(f"Error reading or processing file {out_file_path}: {e}")
                        error_jobs.append(line)

            except ValueError as e:
                print(f"Error parsing job line '{line}': {e}")
                continue

        # Update the jobs file with new classifications
        self._update_jobs_files(running_jobs, finished_jobs, error_jobs)

    def _update_jobs_files(
        self,
        running_jobs: List[str],
        finished_jobs: List[str],
        error_jobs: List[str]
    ) -> None:
        """
        Update job tracking files with classified jobs.

        Args:
            running_jobs: List of currently running jobs.
            finished_jobs: List of completed jobs.
            error_jobs: List of jobs with errors.
        """
        with open(self.job_paths_file, "w") as file:
            file.writelines(f"{job}\n" for job in running_jobs)

        with open(self.error_jobs_file, "a") as file:
            file.writelines(f"{job}\n" for job in error_jobs)

        with open(self.processed_jobs_file, "a") as file:
            file.writelines(f"{job}\n" for job in finished_jobs)

    def process_result(self, molecule_name: str, job_path: str, out_path: str) -> None:
        """
        Process DFT calculation results and extract data.

        Extracts energies, orbitals, and properties from ORCA output files,
        generates Fukui maps, and organizes results.

        Args:
            molecule_name: Name of the molecule calculated.
            job_path: Path to job working directory.
            out_path: Path for output files.
        """
        output_filename: str = os.path.join(job_path, f"{molecule_name}.out")
        xyz_filename: str = os.path.join(job_path, f"{molecule_name}.xyz")
        fukui_filename: str = f"{molecule_name}.fukui.cube"

        # Prepare destination directories
        fukui_destination: str = os.path.join(out_path, "final_fukuis")
        os.makedirs(fukui_destination, exist_ok=True)
        output_destination: str = os.path.join(out_path, "output_files")
        os.makedirs(output_destination, exist_ok=True)
        results_file: str = os.path.join(output_destination, "DFT_results.csv")

        if not os.path.exists(results_file):
            with open(results_file, "w", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=[
                    'Molecule',
                    'Total energy (eV)',
                    'HOMO (eV)',
                    'LUMO (eV)',
                    'Chemical hardness',
                    'Dipole moment',
                    'Polarizability'
                ])
                writer.writeheader()

        # Locate HOMO and LUMO files
        homo_path: Optional[str] = None
        lumo_path: Optional[str] = None
        for file in os.listdir(job_path):
            if file.endswith(".homo.cube"):
                homo_path = os.path.join(job_path, file)
            if file.endswith(".lumo.cube"):
                lumo_path = os.path.join(job_path, file)

        # Extract data from ORCA output
        scf_energy: Optional[float] = self.extract_scf_energy(output_filename)
        homo: Optional[int] = None
        lumo: Optional[int] = None

        try:
            homo, lumo = get_homo_lumo_from_xyz(xyz_filename)
        except Exception as e:
            print(f"Error in homo lumo: {homo} {lumo}")

        homo_energy, lumo_energy, chem_hardness = self.extract_orbital_energies_and_hardness(
            output_filename, homo, lumo
        )
        polar: Optional[str] = self.extract_polarizability(output_filename)
        dipole_moment: Optional[str] = self.extract_dipole(output_filename)

        final_dat_dict: Dict[str, Any] = {
            'Molecule': molecule_name,
            'Total energy (eV)': scf_energy,
            'HOMO (eV)': homo_energy,
            'LUMO (eV)': lumo_energy,
            'Chemical hardness': chem_hardness,
            'Dipole moment': dipole_moment,
            'Polarizability': polar
        }

        with open(results_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=final_dat_dict.keys())
            writer.writerow(final_dat_dict)

        # Process orbital cubes
        if homo_path:
            subprocess.run(["python3", self.orbital_editor, homo_path], check=True)
        if lumo_path:
            subprocess.run(["python3", self.orbital_editor, lumo_path], check=True)

        # Generate Fukui file
        if homo_path and lumo_path:
            subprocess.run(["bash", self.fukui_path, homo_path, lumo_path, molecule_name], check=True)

        # Move the Fukui file
        fukui_path: str = os.path.join(fukui_filename)
        if os.path.exists(fukui_path):
            shutil.move(fukui_path, fukui_destination)

        shutil.move(output_filename, output_destination)

    def extract_scf_energy(self, output_filename: str) -> Optional[float]:
        """
        Extract SCF energy from ORCA output file.

        Args:
            output_filename: Path to ORCA .out file.

        Returns:
            SCF energy in eV.

        Raises:
            ValueError: If SCF energy not found in file.
        """
        search_string: str = "TOTAL SCF ENERGY"
        energy_in_ev: Optional[str] = None
        scf_lines: List[str] = []

        with open(output_filename, "r") as file:
            lines: List[str] = file.readlines()

            for i in range(len(lines)):
                if "TOTAL SCF ENERGY" in lines[i]:
                    print(lines[i + 3])
                    scf_lines.append(lines[i + 3])

            print(f"SCF lines: {scf_lines}")
            if scf_lines:
                energy_in_ev = (scf_lines[-1].split("eV")[0]).split()[-1]
                print(f"Final energy is: {energy_in_ev}")

        if energy_in_ev is None:
            raise ValueError(f"'{search_string}' not found in the file.")

        return float(energy_in_ev)

    def extract_orbital_energies_and_hardness(
        self,
        output_filename: str,
        homo: Optional[int],
        lumo: Optional[int]
    ) -> Tuple[float, float, str]:
        """
        Extract HOMO/LUMO energies and chemical hardness from ORCA output.

        Args:
            output_filename: Path to ORCA .out file.
            homo: HOMO orbital index.
            lumo: LUMO orbital index.

        Returns:
            Tuple of (homo_energy, lumo_energy, chemical_hardness).
        """
        search_string: str = "ORBITAL ENERGIES"
        file_obj = open(output_filename, "r")
        flag: int = 0
        index: int = 0
        line_list: List[int] = []

        for line in file_obj:
            index += 1
            if search_string in line:
                flag = 1
                line_list.append(index)

        file_obj.close()

        file_obj = open(output_filename, "r")
        content: List[str] = file_obj.readlines()
        lines_to_read: int = line_list[len(line_list) - 1]
        homo_line: int = lines_to_read + homo + 3
        lumo_line: int = homo_line + 1

        new_line: str = (content[homo_line])
        new_line_2: str = (' '.join(new_line.split()))
        new_line_3: str = new_line_2.replace(" ", "#")
        homo_energy: float = float(new_line_3.split("#")[3])

        new_line = (content[lumo_line])
        new_line_2 = (' '.join(new_line.split()))
        new_line_3 = new_line_2.replace(" ", "#")
        lumo_energy: float = float(new_line_3.split("#")[3])

        chem_hardness: str = format(((lumo_energy - homo_energy) / 2), ".4f")

        file_obj.close()

        return (homo_energy, lumo_energy, chem_hardness)

    def extract_polarizability(self, output_filename: str) -> Optional[str]:
        """
        Extract isotropic polarizability from ORCA output.

        Args:
            output_filename: Path to ORCA .out file.

        Returns:
            Polarizability value as string.
        """
        search_string: str = "Isotropic polarizability"
        file_obj = open(output_filename, "r")
        polarizability: Optional[str] = None

        for line in file_obj:
            if search_string in line:
                new_line: str = (' '.join(line.split()))
                polarizability = new_line.split(":")[1]

        file_obj.close()
        return polarizability

    def extract_dipole(self, output_filename: str) -> Optional[str]:
        """
        Extract dipole moment from ORCA output.

        Args:
            output_filename: Path to ORCA .out file.

        Returns:
            Dipole moment value as string.
        """
        search_string: str = "Magnitude (Debye)"
        file_obj = open(output_filename, "r")
        dipole_moment: Optional[str] = None

        for line in file_obj:
            if search_string in line:
                new_line: str = (' '.join(line.split()))
                dipole_moment = new_line.split(":")[1]

        file_obj.close()
        return dipole_moment
