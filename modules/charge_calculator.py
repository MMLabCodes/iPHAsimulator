"""
iPHAsimulator - Atomic Partial Charge Calculator.

This module calculates and compares atomic partial charges using several
methods. Accurate partial charges are essential for producing a correct
AMBER force field parameterisation of your PHA molecule.

Supported Charge Models:
    GAFF / GAFF2 with BCC  - Standard AMBER semi-empirical charge method
    NAGL                    - Machine-learning charge model (OpenFF)
    MBIS                    - Quantum theory of atoms in molecules charges
    MULLIKEN                - Charges from ORCA DFT calculations

The ChargeCalculator class requires a PolySimManage object (project directory
manager) along with the molecule name and its SMILES string.

Example::

    from modules.filepath_manager import PolySimManage
    from modules.charge_calculator import ChargeCalculator

    manager = PolySimManage('/path/to/my_project')

    calc = ChargeCalculator(
        manager=manager,
        molecule_name='3HB',
        smiles='CC(O)CC(=O)O'
    )

    # Calculate BCC charges via GAFF and GAFF2
    calc.calculate_all_semi_charge()

    # Optionally calculate ML-based NAGL charges
    calc.calculate_nagl_charge()

    # Save all charge sets to a CSV and generate a comparison plot
    calc.save_charges_to_csv()
    calc.plot_charges()

Note:
    NAGL requires the OpenForceField toolkit (openff-toolkit).
    MBIS requires an additional external script configured via modules.config.
"""

import os
import csv
import subprocess
import warnings
from typing import Optional, List, Tuple, Dict, Any

import matplotlib.pyplot as plt
import itertools

warnings.filterwarnings("ignore", category=UserWarning, module="naglmbis.utils")

try:
    from openff.toolkit.topology import Molecule
    from openff.units import unit
    from openff.toolkit.utils.toolkits import NAGLToolkitWrapper
except ImportError:
    Molecule = None
    unit = None
    NAGLToolkitWrapper = None

try:
    from rdkit import Chem
except ImportError:
    Chem = None

try:
    from modules.filepath_manager import PolySimManage
    from modules.sw_build_systems import BuildAmberSystems
except ImportError:
    PolySimManage = None
    BuildAmberSystems = None

__all__ = [
    'ChargeCalculator',
    'benchmark_charges',  # Legacy alias
    'extract_mol2_charges',
    'extract_nagl_charges',
    'extract_naglmbis_charges',
]


# ============================================================================
# ChargeCalculator Class
# ============================================================================

class ChargeCalculator:
    """
    Calculator for atomic partial charges using multiple computational methods.

    Manages charge calculations across different force fields and machine
    learning models, handles file I/O, and provides visualization tools.

    Attributes:
        molecule_name (str): Name/identifier of the molecule.
        manager (PolySimManage): Directory manager for file organization.
        benchmarking_dir (str): Directory for benchmark output files.
        builder (BuildAmberSystems): System builder for parameterization.
        pdb_file (str): Path to PDB structure file.
        smiles (str): SMILES string for the molecule.
        forcefields (List[str]): Force fields to use for charge calculation.
        charge_models (List[str]): Charge models to apply.
        charge_paths (List[str]): Paths to all charge calculation files.
    """

    def __init__(
        self,
        manager: Optional[Any] = None,
        molecule_name: Optional[str] = None,
        smiles: Optional[str] = None
    ) -> None:
        """
        Initialize ChargeCalculator.

        Args:
            manager: PolySimManage directory manager instance.
            molecule_name: Name of the molecule to calculate charges for.
            smiles: SMILES string for the molecule (used if PDB not found).

        Raises:
            Exception: If neither PDB file nor valid SMILES is provided.
        """
        if BuildAmberSystems is None or PolySimManage is None:
            raise RuntimeError("Required modules (BuildAmberSystems, PolySimManage) not available")

        self.molecule_name: str = molecule_name
        self.manager: Any = manager
        self.benchmarking_dir: str = os.path.join(
            self.manager.molecules_dir, molecule_name, "charge_benchmarking"
        )
        self.builder: Any = BuildAmberSystems(self.manager)
        self.pdb_file: Optional[str] = self.manager.load_pdb_filepath(molecule_name)
        self.forcefields: List[str] = ["GAFF", "GAFF2"]
        self.charge_models: List[str] = ["bcc"]
        self.charge_paths: List[str] = [
            os.path.join(self.benchmarking_dir, f)
            for f in os.listdir(self.benchmarking_dir)
            if os.path.isfile(os.path.join(self.benchmarking_dir, f))
            and not f.lower().endswith((".png", ".csv"))
        ]

        self.base_labels: Optional[List[str]] = None

        # Get paths from configuration (user must set these via environment variables)
        # See: modules/config.py for configuration details
        try:
            from modules.config import get_config
            config = get_config()
            self.mbis_script_path: str = config.get('mbis_script_path', None)
            self.naglmbis_dir: str = config.get('naglmbis_dir', None)
            if not self.mbis_script_path:
                print("Warning: IPHSIMULATOR_MBIS environment variable not set")
            if not self.naglmbis_dir:
                print("Warning: NAGLMBIS_DIR environment variable not set")
        except ImportError:
            self.mbis_script_path: str = None
            self.naglmbis_dir: str = None

        if self.pdb_file is None:
            try:
                self.pdb_file = self.builder.smiles_to_pdb_gen_res_code(smiles, molecule_name)
            except Exception as e:
                print(f"Please ensure you have provided both the molecule name and its SMILES string")
                print("")
                print(f"The error can be found below:\n{e}")

        try:
            self.smiles: str = self.manager.load_smiles(self.molecule_name)
        except Exception as e:
            print(f"No smiles found for {molecule_name}\nThe error can be found below:\n{e}")
            return

        if not os.path.exists(self.benchmarking_dir):
            os.makedirs(self.benchmarking_dir)

    def calculate_all_semi_charge(self) -> None:
        """
        Calculate charges using all configured force field and charge model combinations.

        Iterates through all force fields and charge models, calling parameterize_mol
        for each combination and storing the resulting MOL2 files.
        """
        for i in range(len(self.forcefields)):
            for j in range(len(self.charge_models)):
                benchmark_output: str = os.path.join(
                    self.benchmarking_dir,
                    f"{self.forcefields[i]}_{self.charge_models[j]}"
                )
                self.builder.parameterize_mol(
                    molecule_name=self.molecule_name,
                    forcefield=self.forcefields[i],
                    charge_model=self.charge_models[j],
                    benchmarking_charges=True,
                    benchmark_output=benchmark_output
                )
                self.charge_paths.append(f"{benchmark_output}.mol2")

    def calculate_nagl_charge(self, mol2_file: Optional[str] = None) -> None:
        """
        Calculate charges using NAGL machine learning model.

        Uses the OpenForceField NAGL toolkit to assign partial charges based
        on molecule structure. Supports both direct SDF conversion or PDB/SMILES
        combined approach.

        Args:
            mol2_file: Optional MOL2 file to convert to SDF first.

        Example:
            >>> calculator.calculate_nagl_charge()
            >>> # Or from existing MOL2 file:
            >>> calculator.calculate_nagl_charge(mol2_file='mol.mol2')
        """
        if Molecule is None or NAGLToolkitWrapper is None:
            raise RuntimeError("OpenForceField toolkit not available")

        if self.pdb_file is None or self.smiles is None:
            print(f"""pdb_file = {self.pdb_file}
smiles = {self.smiles}

Please ensure both a pdb file and the smiles exist for {self.molecule_name}.""")
            return

        if mol2_file is not None:
            try:
                subprocess.run(["obabel", mol2_file, "-O", "output.sdf"])
                mol = Molecule.from_file("output.sdf")
            except Exception as e:
                print(f"Error was:\n{e}")
        else:
            # Load molecule from pdb and smiles
            mol = Molecule.from_pdb_and_smiles(
                self.pdb_file, self.smiles, allow_undefined_stereo=True
            )

        # Initialize NAGL
        nagl = NAGLToolkitWrapper()

        # Use latest NAGL model
        method: str = list(nagl.supported_charge_methods)[-1]
        nagl.assign_partial_charges(mol, partial_charge_method=method)

        # Write to nagl.nagl file
        nagl_path: str = os.path.join(self.benchmarking_dir, "nagl.nagl")
        with open(nagl_path, "w") as f:
            for i, charge in enumerate(mol.partial_charges):
                f.write(f"Atom {i}: {charge.m:.6f} e\n")

        self.charge_paths.append(nagl_path)

    def calculate_mbis_charge(self) -> None:
        """
        Calculate charges using MBIS (Minimal Basis Iterative Subspace) method.

        Runs an external MBIS calculation script and stores the results.

        Raises:
            subprocess.CalledProcessError: If MBIS script execution fails.
        """
        filename: str = os.path.join(self.benchmarking_dir, "mbis.mbis")

        try:
            result = subprocess.run(
                ["bash", self.mbis_script_path, filename, self.smiles],
                check=True,
                text=True,
                capture_output=True
            )
            print("Script output:\n", result.stdout)
            if result.stderr:
                print("Script errors:\n", result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"Error while running {self.mbis_script_path}: {e}")
            print("stderr:\n", e.stderr)

        self.charge_paths.append(filename)

    @staticmethod
    def extract_mol2_charges(filename: str) -> Tuple[List[str], List[float]]:
        """
        Extract atomic charges and labels from MOL2 file.

        Args:
            filename: Path to MOL2 file.

        Returns:
            Tuple of (atom_labels, charges) where labels are "id:type" format.

        Example:
            >>> labels, charges = ChargeCalculator.extract_mol2_charges('mol.mol2')
            >>> print(labels[0], charges[0])
        """
        atom_labels: List[str] = []
        charges: List[float] = []

        with open(filename, 'r') as f:
            inside_atoms: bool = False
            for line in f:
                if line.startswith("@<TRIPOS>ATOM"):
                    inside_atoms = True
                    continue
                elif line.startswith("@<TRIPOS>") and inside_atoms:
                    break
                elif inside_atoms:
                    parts: List[str] = line.split()
                    if len(parts) >= 9:
                        try:
                            atom_id: str = parts[0]
                            atom_type: str = parts[5]
                            charge: float = float(parts[8])
                            atom_labels.append(f"{atom_id}:{atom_type}")
                            charges.append(charge)
                        except (ValueError, IndexError):
                            pass

        return atom_labels, charges

    @staticmethod
    def extract_nagl_charges(filename: str) -> List[float]:
        """
        Extract charges from NAGL .nagl file.

        Args:
            filename: Path to NAGL output file.

        Returns:
            List of partial charges in eV.

        Example:
            >>> charges = ChargeCalculator.extract_nagl_charges('nagl.nagl')
        """
        charges: List[float] = []

        with open(filename, "r") as f:
            for line in f:
                if line.startswith("Atom"):
                    parts: List[str] = line.replace("e", "").split()
                    try:
                        charge: float = float(parts[-1])
                        charges.append(charge)
                    except ValueError:
                        pass

        return charges

    @staticmethod
    def extract_naglmbis_charges(filename: str) -> List[float]:
        """
        Extract charges from NAGL-MBIS text file (one charge per line).

        Args:
            filename: Path to MBIS output file.

        Returns:
            List of partial charges.

        Example:
            >>> charges = ChargeCalculator.extract_naglmbis_charges('mbis.mbis')
        """
        charges: List[float] = []

        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        charges.append(float(line))
                    except ValueError:
                        pass

        return charges

    def plot_charges(self, show_plot: bool = True) -> None:
        """
        Generate comparison plot of charges from different methods.

        Creates a multi-series line plot comparing atomic charges calculated
        by different methods, saved as PNG image.

        Args:
            show_plot: If True, display the plot in addition to saving.

        Example:
            >>> calculator.plot_charges(show_plot=False)
            Plot saved to: .../molecule_charges.png
        """
        title: str = f"Comparison of Atomic Charges for {self.molecule_name}"
        output_file: str = os.path.join(
            self.benchmarking_dir, f"{self.molecule_name}_charges.png"
        )

        plt.figure(figsize=(12, 6))

        # Marker cycle for each series
        marker_cycle = itertools.cycle(['o', 's', 'd', '^', 'v', '<', '>', 'p', '*', 'h', 'H', '+', 'x'])
        line_width: float = 1.0

        self.charge_paths.sort(key=lambda f: f.rsplit('.', 1)[-1].lower())

        for infile in self.charge_paths:
            print(infile)
            marker_style: str = next(marker_cycle)

            labels: Optional[List[str]] = None
            charges: Optional[List[float]] = None
            linestyle: str = '-'

            if infile.endswith(".mol2"):
                labels, charges = self.extract_mol2_charges(infile)
                linestyle = '-'
            elif infile.endswith(".nagl"):
                charges = self.extract_nagl_charges(infile)
                labels = self.base_labels
                linestyle = '--'
            elif infile.endswith(".mbis"):
                charges = self.extract_naglmbis_charges(infile)
                labels = self.base_labels
                linestyle = '--'
            else:
                print(f"Unsupported file format: {infile}")
                continue

            if self.base_labels is None and labels is not None:
                self.base_labels = labels

            if labels is None or charges is None:
                print(f"Skipping {infile}: missing labels or charges.")
                continue

            plt.plot(
                labels, charges,
                marker=marker_style,
                linestyle=linestyle,
                linewidth=line_width,
                label=(infile.split("/")[-1]).split(".")[0]
            )

        plt.title(title)
        plt.xlabel("Atom (Index:Type)")
        plt.ylabel("Partial Charge (e)")
        plt.xticks(rotation=90)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300)

        if show_plot:
            plt.show()

        plt.close()
        print(f"Plot saved to {output_file}")

    def save_charges_to_csv(self) -> None:
        """
        Extract all charge data and save to CSV file.

        Creates a CSV file with columns: atom_index, atom_label, method, charge
        One row per atom per method, allowing easy comparison across methods.

        Example:
            >>> calculator.save_charges_to_csv()
            ✅ Charge data saved to: .../molecule_charges.csv
        """
        output_csv: str = os.path.join(
            self.benchmarking_dir,
            f"{self.molecule_name}_charges.csv"
        )

        rows: List[Dict[str, Any]] = []

        # Sort input files by extension
        self.charge_paths.sort(key=lambda f: f.rsplit('.', 1)[-1].lower())

        for infile in self.charge_paths:
            method_name: str = os.path.splitext(os.path.basename(infile))[0]

            labels: Optional[List[str]] = None
            charges: Optional[List[float]] = None

            if infile.endswith(".mol2"):
                labels, charges = self.extract_mol2_charges(infile)
            elif infile.endswith(".nagl"):
                charges = self.extract_nagl_charges(infile)
                labels = self.base_labels
            elif infile.endswith(".mbis"):
                charges = self.extract_naglmbis_charges(infile)
                labels = self.base_labels
            else:
                print(f"Skipping unsupported format: {infile}")
                continue

            if labels is None or charges is None:
                print(f"Skipping {infile}: missing labels or charges")
                continue

            # Store each atom as a row
            for idx, (label, charge) in enumerate(zip(labels, charges)):
                rows.append({
                    "atom_index": idx,
                    "atom_label": label,
                    "method": method_name,
                    "charge": charge
                })

        # Write CSV
        with open(output_csv, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["atom_index", "atom_label", "method", "charge"]
            )
            writer.writeheader()
            writer.writerows(rows)

        print(f"✅ Charge data saved to: {output_csv}")


# Legacy alias for backward compatibility
benchmark_charges = ChargeCalculator


# ============================================================================
# Deprecated Utility Functions
# ============================================================================

def extract_mol2_charges(filename: str) -> Tuple[List[str], List[float]]:
    """Deprecated: Use ChargeCalculator.extract_mol2_charges instead."""
    return ChargeCalculator.extract_mol2_charges(filename)


def extract_nagl_charges(filename: str) -> List[float]:
    """Deprecated: Use ChargeCalculator.extract_nagl_charges instead."""
    return ChargeCalculator.extract_nagl_charges(filename)


def extract_naglmbis_charges(filename: str) -> List[float]:
    """Deprecated: Use ChargeCalculator.extract_naglmbis_charges instead."""
    return ChargeCalculator.extract_naglmbis_charges(filename)
