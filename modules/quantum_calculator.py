"""
Quantum chemistry molecule representation and utilities.

This module provides classes and utilities for representing and processing
molecules with quantum chemical properties calculated using ORCA. It includes
a molecule class with properties like energy, orbital energies, and polarizability,
plus utilities for loading molecule data from CSV files.

Example:
    Working with quantum chemistry data::

        from modules.quantum_calculator import OrcaMolecule, csv_to_orca_molecules

        # Create a molecule from ORCA data
        mol = OrcaMolecule(
            name='ethane',
            smiles='CC',
            mw=30.07,
            peak_area=1000,
            total_energy=-79.5,
            homo_lumo_gap=8.5,
            chemical_hardness=4.25,
            dipole_moment=0.0,
            polarizability=11.5,
            volume=100.0
        )

        # Load molecules from CSV file
        molecules = csv_to_orca_molecules('/path/to/data.csv')

Note:
    This module requires RDKit for SMILES processing and volume calculations.
"""

import csv
from typing import List, Optional
from dataclasses import dataclass

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem
except ImportError:
    Chem = None
    AllChem = None

try:
    from modules.sw_basic_functions import vol_from_smiles
except ImportError:
    vol_from_smiles = None

__all__ = [
    'OrcaMolecule',
    'csv_to_orca_molecules',
    'orca_molecule',  # Legacy alias
    'csv_to_orca_class',  # Legacy alias
]


# ============================================================================
# OrcaMolecule Class
# ============================================================================

@dataclass
class OrcaMolecule:
    """
    Representation of a molecule with quantum chemical properties from ORCA.

    Stores molecular structure, spectroscopy data, and quantum chemical
    properties calculated using ORCA DFT calculations.

    Attributes:
        name (str): Name or identifier of the molecule.
        smiles (str): SMILES string representing the molecular structure.
        mw (float): Molecular weight in g/mol.
        peak_area (float): Peak area from spectroscopy data (concentration/amount).
        total_energy (float): Total electronic energy from ORCA in eV or Hartree.
        homo_lumo_gap (float): Energy gap between HOMO and LUMO in eV.
        chemical_hardness (float): Chemical hardness (typically HOMO-LUMO gap / 2) in eV.
        dipole_moment (float): Dipole moment in Debye.
        polarizability (float): Isotropic polarizability in Angstrom^3.
        volume (float): Molecular volume in Angstrom^3.

    Example:
        >>> mol = OrcaMolecule(
        ...     name='methane',
        ...     smiles='C',
        ...     mw=16.04,
        ...     peak_area=500,
        ...     total_energy=-40.2,
        ...     homo_lumo_gap=13.5,
        ...     chemical_hardness=6.75,
        ...     dipole_moment=0.0,
        ...     polarizability=2.6,
        ...     volume=35.5
        ... )
        >>> print(f"{mol.name}: {mol.homo_lumo_gap} eV gap")
        methane: 13.5 eV gap
    """

    name: str
    smiles: str
    mw: float
    peak_area: float
    total_energy: float
    homo_lumo_gap: float
    chemical_hardness: float
    dipole_moment: float
    polarizability: float
    volume: float


# Legacy alias for backward compatibility
orca_molecule = OrcaMolecule


# ============================================================================
# CSV Processing Functions
# ============================================================================

def csv_to_orca_molecules(csv_file: str) -> List[OrcaMolecule]:
    """
    Load molecule data from CSV file and create OrcaMolecule objects.

    Reads a CSV file containing quantum chemical data and creates
    OrcaMolecule instances. Calculates molecular volume from SMILES strings.

    Expected CSV format (with header row):
        name, mw, peak_area, smiles, total_energy, homo, lumo, homo_lumo_gap,
        chemical_hardness, dipole_moment, polarizability

    Args:
        csv_file: Path to the CSV file containing molecule data.

    Returns:
        List of OrcaMolecule objects populated with data from the CSV file.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        IndexError: If CSV has fewer columns than expected.
        ValueError: If SMILES string is invalid or HOMO/LUMO indices cannot be parsed.

    Example:
        >>> molecules = csv_to_orca_molecules('/data/molecules.csv')
        >>> for mol in molecules:
        ...     print(f"{mol.name}: {mol.mw} g/mol")
    """
    if vol_from_smiles is None:
        raise RuntimeError("vol_from_smiles function not available")

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        molecules: List[list] = []
        for molecule in reader:
            molecules.append(molecule)

    orca_molecules: List[OrcaMolecule] = []

    for i in range(len(molecules)):
        if i == 0:
            continue  # Skip header row

        try:
            molecule_name: str = molecules[i][0].strip()
            molecular_weight: float = round(float(molecules[i][1]), 2)
            peak_area: str = molecules[i][2]
            smiles: str = molecules[i][3]
            tot_energy: str = molecules[i][4]
            homo: str = molecules[i][5]
            lumo: str = molecules[i][6]
            homo_lumo_gap: str = molecules[i][7]
            chemical_hardness: str = molecules[i][8]
            dipole_moment: str = molecules[i][9]
            polarizability: str = molecules[i][10]

            # Calculate volume from SMILES
            volume: float = vol_from_smiles(smiles)

            # Create OrcaMolecule object
            mol: OrcaMolecule = OrcaMolecule(
                name=molecule_name,
                smiles=smiles,
                mw=molecular_weight,
                peak_area=peak_area,
                total_energy=tot_energy,
                homo_lumo_gap=homo_lumo_gap,
                chemical_hardness=chemical_hardness,
                dipole_moment=dipole_moment,
                polarizability=polarizability,
                volume=volume
            )

            orca_molecules.append(mol)

        except (IndexError, ValueError) as e:
            print(f"Error processing row {i}: {e}")
            continue

    return orca_molecules


# Legacy alias for backward compatibility
csv_to_orca_class = csv_to_orca_molecules
